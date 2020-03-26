import os
import logging
import traceback
from db import mongo
from io import BytesIO
from zipfile import ZipFile
from threading import Thread
from natsort import natsorted
from bson.objectid import ObjectId
from plantweb.render import render
from cvp_parser.parser_main import parser_main
from cvp_parser.query_parser import query_parser
from flask import jsonify, Blueprint, render_template, request, Response, current_app

bp = Blueprint("bp", __name__)

def threaded_task(app, filename, contents):
    mongo.db.files.insert_one({"_id":filename,"device":"unknown", "status": "Processing..."})
    try:
        device = parser_main(filename, contents)
        result = mongo.db.files.update({"_id":filename},  {"$set": {"status": "Processed", "device": device}})
    except Exception:
        app.logger.error(traceback.format_exc())
        result = mongo.db.files.update({"_id":filename}, {"$set": {"status": "Failed"}})

    return result

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/statistics/<filename>")
def statistics(filename):
    return render_template("statistics.html",filename=filename)

@bp.route("/files")
def files():
    return render_template("files.html")

@bp.route("/signatures")
def signatures():
    return render_template("signatures.html")

@bp.route("/api/GUIDs/<string:filename>")
def get_GUIDs(filename):
    cursor = mongo.db.GUIDs.find({"_id.filename":filename})
    GUIDs = [[res["_id"]["guid"], res["from"], res["to"]] for res in cursor]
    return jsonify(GUIDs),200

@bp.route("/api/GUID/<string:id>")
def get_GUID(id):
    # BAD CODE: WHAT IF TWO LOG FILES HAVE SAME GUID
    sequence = mongo.db.GUIDs.find_one({"_id.guid":id},{"sequence":1})
    sequence = sequence["sequence"]
    svg = render(sequence, engine="plantuml", format="svg")
    svg = svg[0].decode('utf-8')

    return {"svg":svg},200

@bp.route("/api/message/<string:id>")
def get_message(id):
    msg_text = mongo.db.msgs.find_one({"_id.oid": id}, {"text":1})
    msg_text = msg_text["text"]
    return {"msg_text": msg_text}

@bp.route("/uploads", methods=["POST"])
def uploads():
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

@bp.route('/diagram/<string:ID>',methods=["GET"])
def diagram(ID):
    return render_template("diagram.html", guid=ID)

@bp.route("/api/files")
def getfilenames():
    cursor = mongo.db.files.find({})
    files = [[res["_id"], res["device"], res["status"]] for res in cursor]
    return jsonify(files),200

@bp.route("/api/filter", methods=["POST"])
def callFilter():
    call_filter = request.get_json()["filter"]
    filename = request.get_json()["filename"]
    query = query_parser(call_filter)
    if not query:
        return "Invalid call filter", 400
    query["_id.filename"] = filename
    guids = mongo.db.msgs.distinct("guid",query)

    return {"guids": guids, "query":str(query)}

@bp.route("/api/signature", methods=["POST"])
def storeSignatute():
    call_filter = request.get_json()["filter"]
    signature = request.get_json()["signature"]
    try:
        id = mongo.db.signatures.insert_one({"_id":signature, "filter":call_filter})
    except Exception:
        return "signature already exists", 400
    return id.inserted_id, 200

@bp.route("/api/signatures")
def getSignatures():
    cursor = mongo.db.signatures.find({})
    result = [[res["_id"], res["filter"]] for res in cursor]

    return jsonify(result)

@bp.route("/api/match/<string:ID>/<string:filename>")
def matchSigntures(ID=None, filename=None):
    signatures = []
    cursor = mongo.db.signatures.find({})
    filters = [(res["_id"],res["filter"]) for res in cursor]
    for call_filter in filters:
        query = query_parser(call_filter[1])
        if not query: continue
        query["guid"] = ID
        query["_id.filename"] = filename
        if mongo.db.msgs.find_one(query, {"_id":1}):
            signatures.append(call_filter[0])
    return {"signatures": signatures}

@bp.route("/api/delete/<filename>")
def deleteFile(filename):
    mongo.db.files.delete_one({"_id": filename})
    mongo.db.GUIDs.delete_many({"_id.filename":filename})  
    mongo.db.msgs.delete_many({"_id.filename":filename})
    unique_files=mongo.db.GUIDs.distinct("_id.filename")
    return jsonify(unique_files),200

@bp.route('/filters/<filename>',methods=["GET"])
def filter(filename):
    return render_template("filter.html",filename=filename)