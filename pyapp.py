import os
import csv
import logging
import traceback
from db import mongo
from io import BytesIO
from zipfile import ZipFile
from threading import Thread
from datetime import datetime
from natsort import natsorted
from bson.objectid import ObjectId
from plantweb.render import render
from query_parser import query_parser
from log_parser.parser_main import parser_main
from flask import jsonify, Blueprint, render_template, request, Response, current_app, send_file

bp = Blueprint("bp", __name__)

@bp.before_request
def eventLogging():
    filePath = os.path.join(current_app.instance_path, 'eventLog.log')
    eventLog = open(filePath, 'a', newline='')
    writer = csv.writer(eventLog, quoting=csv.QUOTE_ALL)

    endpoint = request.endpoint.split('.')[1]
    ignored_endpoints = ["index", "signatures_page", "call_summary", "get_files","diagram_page"]
    if endpoint in ignored_endpoints: return None
    if endpoint == 'upload_files':
        writer.writerow([str(datetime.now()), endpoint, request.files['file'].filename])
    elif request.method == 'GET':
        writer.writerow([str(datetime.now()), endpoint, str(request.view_args)])
    elif request.method == 'POST':
        writer.writerow([str(datetime.now()), endpoint, str(request.get_json())])

    eventLog.close()
    return None

def writeToDB(guids):
    for guid in guids.keys():
        mongo.db.GUIDs.insert_one(guids[guid]["doc"])
        for msg in guids[guid]["msgs"]:
            mongo.db.msgs.insert_one(msg)

def threaded_task(app, filename, contents):
    mongo.db.files.insert_one({"_id":filename,"device":"unknown", "status": "Processing..."})
    try:
        device, guids = parser_main(filename, contents)
        result = mongo.db.files.update({"_id":filename},  {"$set": {"status": "Processed", "device": device}})
        writeToDB(guids)
    except Exception:
        app.logger.error(traceback.format_exc())
        result = mongo.db.files.update({"_id":filename}, {"$set": {"status": "Failed"}})

    return result

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/call-summary/<filename>")
def call_summary(filename):
    return render_template("details.html",filename=filename)

@bp.route("/signatures-page")
def signatures_page():
    return render_template("signatures.html")

@bp.route("/get-calls/<string:filename>")
def get_calls(filename):
    cursor = mongo.db.GUIDs.find({"_id.filename":filename})
    GUIDs = [[res["_id"]["guid"], res["from"], res["to"]] for res in cursor]
    return jsonify(GUIDs),200

@bp.route("/ladder-diagram/<string:filename>/<string:guid>")
def ladder_diagram(filename, guid):
    _id = {"filename":filename, "guid":guid}
    sequence = mongo.db.GUIDs.find_one({"_id":_id},{"sequence":1})
    sequence = sequence["sequence"]
    svg = render(sequence, engine="plantuml", format="svg")
    svg = svg[0].decode('utf-8')

    return {"svg":svg},200

@bp.route("/message/<string:id>")
def get_message(id):
    msg_text = mongo.db.msgs.find_one({"_id.oid": id}, {"text":1})
    msg_text = msg_text["text"]
    return {"msg_text": msg_text}

@bp.route("/uploads", methods=["POST"])
def upload_files():
    file = request.files['file']

    contents = BytesIO()
    if file.filename.endswith('.zip'):
        zipfile = ZipFile(file)
        names = natsorted(zipfile.namelist(), key=lambda x: x.lower())
        for name in names:
            contents.write(zipfile.read(name))
    elif file.filename.endswith('.log') or file.filename.endswith('.txt'):
        contents.write(file.read())
    else:
        return "Invalid file type", 400

    unique_files=mongo.db.GUIDs.distinct("_id.filename")
    if ( file.filename in unique_files):
        return "Exists",400

    app = current_app._get_current_object()
    thread = Thread(target=threaded_task, args=(app, file.filename, contents))
    thread.daemon = True
    thread.start()
    
    #   parser_main(file.filename, contents)
    return render_template("index.html"), 200

@bp.route('/diagram-page/<string:filename>/<string:ID>',methods=["GET"])
def diagram_page(filename,ID):
    return render_template("diagram.html", filename=filename, guid=ID)

@bp.route("/files")
def get_files():
    cursor = mongo.db.files.find({})
    files = [[res["_id"], res["device"], res["status"]] for res in cursor]
    return jsonify(files),200

@bp.route("/call-filter", methods=["POST"])
def call_filter():
    call_filter = request.get_json()["filter"]
    filename = request.get_json()["filename"]
    filename=filename.split(",")[0]
    query = query_parser(call_filter)
    if not query:
        return "Invalid call filter", 400
    query["_id.filename"] = filename
    guids = mongo.db.msgs.distinct("guid",query)
    cursor = mongo.db.GUIDs.find({"_id.guid": {"$in":guids}})
    GUIDs = [[res["_id"]["guid"], res["from"], res["to"]] for res in cursor]

    return jsonify(GUIDs), 200

@bp.route("/post-signature", methods=["POST"])
def post_signature():
    signature = request.get_json()["signature"]
    description = request.get_json()["description"]
    try:
        id = mongo.db.signatures.insert_one({"_id":signature, "description":description})
    except Exception:
        return "signature already exists", 400
    return id.inserted_id, 200

@bp.route("/get-signatures")
def get_signatures():
    cursor = mongo.db.signatures.find({})
    result = [[res["_id"], res["description"]] for res in cursor]

    return jsonify(result)

@bp.route("/match-signatures/<string:filename>/", defaults={"guid":None})
@bp.route("/match-signatures/<string:filename>/<string:guid>")
def match_signtures(filename, guid):
    signatures = []
    cursor = mongo.db.signatures.find({})
    filters = [(res["_id"],res["description"]) for res in cursor]
    for call_filter in filters:
        query = query_parser(call_filter[0])
        if not query: continue
        if guid is not None:
            query["guid"] = guid
        query["_id.filename"] = filename
        if mongo.db.msgs.find_one(query, {"_id":1}):
            signatures.append(call_filter[1])
    return {"signatures": signatures}

@bp.route("/delete/<filename>")
def delete_file(filename):
    mongo.db.files.delete_one({"_id": filename})
    mongo.db.GUIDs.delete_many({"_id.filename":filename})  
    mongo.db.msgs.delete_many({"_id.filename":filename})
    unique_files=mongo.db.GUIDs.distinct("_id.filename")
    return jsonify(unique_files),200

@bp.route("/logAccess", methods=["POST"])
def generateDownloadLink():
    parts = request.get_json()
    filename = parts["filename"]
    from_date = datetime.strptime(parts["from_date"], "%Y-%m-%dT%H:%M")
    to_date = datetime.strptime(parts["to_date"], "%Y-%m-%dT%H:%M")

    cursor = mongo.db.msgs.find({"_id.filename":filename, "datetime": {"$gt": from_date, "$lt": to_date}}, {"text":1}).sort("count",1)
    file = BytesIO()
    if cursor.count() == 0:
        file.write("No messages found within date range".encode('latin1'))
        filename = "404.txt"
    for res in cursor:
        file.write(res["text"].encode('latin1'))
    file.seek(0)
    return send_file(file, attachment_filename=filename, mimetype='text/plain', as_attachment=True)