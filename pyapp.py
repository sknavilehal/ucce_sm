import os
import csv
import logging
import traceback
from io import BytesIO
from zipfile import ZipFile
from threading import Thread
from datetime import datetime
from natsort import natsorted
from pymongo import MongoClient
from bson.objectid import ObjectId
from plantweb.render import render
from query_parser import query_parser
from log_parser.parser_main import parser_main
from flask import jsonify, Blueprint, render_template, request, Response, current_app, send_file, session, g, redirect

bp = Blueprint("bp", __name__)

client = MongoClient("mongodb://localhost:27017")

@bp.route('/setSession/<string:username>')
def setSession(username):
    # username here is name of the database
    session["username"] = username

    return "Session set", 200
    
@bp.route('/clearSession')
def clearSession():
    session.pop("username")

    return "",200

@bp.before_request
def before_request():
    #Before a request is made get username from session and store database connection in g object
    username = session.get("username", "Guest")
    g.db = client[username] # Gets reset after a request and has to be set again
    endpoint = request.endpoint.split('.')[1]
    
    #Event logging
    endpoints = ['setSession', 'clearSession', 'download_eventlog']
    if session.get("username", None) is None and endpoint not in endpoints:
        return render_template('login.html')

    filePath = os.path.join(current_app.instance_path, 'event_log.csv')
    eventLog = open(filePath, 'a', newline='')
    writer = csv.writer(eventLog)

    # Only endpoints in this list are logged to eventLog.log
    important_endpoints = ["get_calls", "ladder_diagram", "get_message", "upload_files","call_filter", "post_signature", "match_signtures", "delete_file", "delete_signature"]
    if endpoint not in important_endpoints: return None

    parts = request.path.split('/')
    category, action = parts[1], parts[2]
    row = [str(datetime.now()), username, category, action]

    if endpoint == 'upload_files':
        row.append(request.files['file'].filename)
        writer.writerow(row)
    elif request.method == 'GET':
        for param in request.args.keys():
            if param == "_": continue
            row.append(request.args.get(param))
        writer.writerow(row)
    elif request.method == 'POST':
        for key in request.get_json().keys():
            row.append(request.get_json()[key])
        writer.writerow(row)

    eventLog.close()

    return None

def threaded_task(_g, app, filename, contents):
    # _g and app are flask objects required for threaded task running outside application context
    _g.db.files.insert_one({"_id":filename,"device":"unknown", "status": "Processing..."})
    try:
        device, guids = parser_main(filename, contents)
        _g.db.files.update({"_id":filename},  {"$set": {"status": "Processed", "device": device}})
        
        for guid in guids.keys():
            _g.db.GUIDs.insert_one(guids[guid]["doc"])
            for msg in guids[guid]["msgs"]:
                _g.db.msgs.insert_one(msg)
    except Exception:
        app.logger.error(traceback.format_exc())
        _g.db.files.update({"_id":filename}, {"$set": {"status": "Failed"}})

@bp.route("/")
def login():
    return render_template("login.html")

@bp.route("/home")
def home():
    return render_template("index.html")

@bp.route("/call-summary")
def call_summary():
    filename = request.args.get('filename', None)
    return render_template("details.html",filename=filename)

@bp.route("/signatures-page")
def signatures_page():
    return render_template("signatures.html")

@bp.route("/Files-History/analyze")
def get_calls():
    filename = request.args.get('filename', None)
    cursor = g.db.GUIDs.find({"_id.filename":filename})
    GUIDs = [[res["_id"]["guid"], res["from"], res["to"]] for res in cursor]
    return jsonify(GUIDs),200

@bp.route("/Call-Summary/details")
def ladder_diagram():
    filename = request.args.get('filename', None)
    guid = request.args.get('guid', None)
    _id = {"filename":filename, "guid":guid}
    sequence = g.db.GUIDs.find_one({"_id":_id},{"sequence":1})
    sequence = sequence["sequence"]
    try:
        svg = render(sequence, engine="plantuml", format="svg")
        svg = svg[0].decode('utf-8')
    except Exception as e:
        return str(e), 403

    return {"svg":svg},200

@bp.route("/Call-Summary/message")
def get_message():
    oid = request.args.get('oid', None)
    msg_text = g.db.msgs.find_one({"_id.oid": oid}, {"text":1})
    msg_text = msg_text["text"]
    return {"msg_text": msg_text}

@bp.route("/Files-History/upload", methods=["POST"])
def upload_files():
    file = request.files['file']
    app = current_app._get_current_object()
    _g = g._get_current_object()
    files=g.db.files.distinct("_id")
    
    if file.filename.endswith('.zip'):
        names_container = {}
        zipfile = ZipFile(file)
        filenames = natsorted(zipfile.namelist(), key=lambda x: x.lower())

        for filename in filenames:
            basename = os.path.basename(filename)
            dirname = os.path.dirname(filename)
            if basename.endswith('.log') and basename.startswith('CVP.'):
                if dirname not in names_container: names_container[dirname] = []
                names_container[dirname].append(filename)
        
        for _dir, _files in names_container.items():
            contents = BytesIO()
            if _dir in files:
                return "Exists",400
            for _file in _files:
                contents.write(zipfile.read(_file))
            filename = file.filename + '/' + _dir
            Thread(target=threaded_task, args=(_g, app, filename, contents)).start()

    elif file.filename.endswith('.log') or file.filename.endswith('.txt'):
        contents = BytesIO()
        contents.write(file.read())
        if ( file.filename in files):
            return "Exists",400
        Thread(target=threaded_task, args=(_g, app, file.filename, contents)).start()
    else:
        return "Invalid file type", 400
    
    return render_template("index.html"), 200

@bp.route('/diagram-page',methods=["GET"])
def diagram_page():
    filename = request.args.get('filename', None)
    guid = request.args.get('guid', None)
    return render_template("diagram.html", filename=filename, guid=guid)

@bp.route("/files")
def get_files():
    cursor = g.db.files.find({})
    files = [[res["_id"], res["device"], res["status"]] for res in cursor]
    return jsonify(files),200

@bp.route("/Call-Summary/filter", methods=["POST"])
def call_filter():
    filter = request.get_json()["filter"]
    filename = request.get_json()["filename"]
    filename=filename.split(",")[0]
    query = query_parser(filter)
    if not query:
        return "Invalid call filter", 400
    query["_id.filename"] = filename
    guids = g.db.msgs.distinct("guid",query)
    cursor = g.db.GUIDs.find({"_id.guid": {"$in":guids}, "_id.filename":filename})
    GUIDs = [[res["_id"]["guid"], res["from"], res["to"]] for res in cursor]

    return jsonify(GUIDs), 200

@bp.route("/Signatures/new-sig", methods=["POST"])
def post_signature():
    signature = request.get_json()["signature"]
    description = request.get_json()["description"]
    try:
        id = g.db.signatures.insert_one({"_id":signature, "description":description})
    except Exception:
        return "signature already exists", 400
    return id.inserted_id, 200

@bp.route("/Signatures/delete-sig")
def delete_signature():
    signature = request.args.get("signature", None)
    g.db.signatures.delete_one({"_id":signature})

    return "Signature deleted", 200

@bp.route("/get-signatures")
def get_signatures():
    cursor = g.db.signatures.find({})
    result = [[res["_id"], res["description"]] for res in cursor]

    return jsonify(result)

@bp.route("/Files-History/signature")
@bp.route("/Call-Summary/signature")
def match_signtures():
    signatures = []
    filename = request.args.get("filename", None)
    guid = request.args.get("guid", None)
    cursor = g.db.signatures.find({})
    filters = [(res["_id"],res["description"]) for res in cursor]
    for filter in filters:
        query = query_parser(filter[0])
        if not query: continue
        if guid is not None:
            query["guid"] = guid
        query["_id.filename"] = filename
        if g.db.msgs.find_one(query, {"_id":1}):
            signatures.append(filter[1])
    return {"signatures": signatures}

@bp.route("/Files-History/delete")
def delete_file():
    filename = request.args.get('filename', None)
    g.db.files.delete_one({"_id": filename})
    g.db.GUIDs.delete_many({"_id.filename":filename})  
    g.db.msgs.delete_many({"_id.filename":filename})
    unique_files=g.db.GUIDs.distinct("_id.filename")
    return jsonify(unique_files),200

@bp.route("/download-file")
def download_file():
    filename = request.args.get("filename", None)
    cursor = g.db.msgs.find({"_id.filename":filename}, {"text":1}).sort("count",1)
    file = BytesIO()
    for res in cursor:
        file.write(res["text"].encode('latin1'))
    file.seek(0)
    return send_file(file, attachment_filename=os.path.basename(filename), mimetype='text/plain', as_attachment=True)

@bp.route("/download-eventlog")
def download_eventlog():
    file = os.path.join(current_app.instance_path, 'event_log.csv')

    return send_file(file, attachment_filename=os.path.basename(file), mimetype='text/plain', as_attachment=True)