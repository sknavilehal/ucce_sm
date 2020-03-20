import os
import logging
from db import mongo
from bson.objectid import ObjectId
from plantweb.render import render
from cvp_parser.parser_main import parser_main
from cvp_parser.query_parser import query_parser
from flask import jsonify, Blueprint, render_template, request, Response

bp = Blueprint("bp", __name__)

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/statistics/<filename>")
def statistics(filename):
    print(filename)
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
    GUIDs = [[res["_id"]["guid"]] for res in cursor]
    return jsonify(GUIDs),200

@bp.route("/api/GUID/<string:id>")
def get_GUID(id):
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

    unique_files=mongo.db.GUIDs.distinct("_id.filename")
    if ( file.filename in unique_files):
        return "Exists",400
    parser_main(file)
    return render_template("index.html"), 200

@bp.route('/diagram/<string:ID>',methods=["GET"])
def diagram(ID):
    return render_template("diagram.html", guid=ID)


@bp.route("/api/files")
def getfilenames():
    unique_files=mongo.db.GUIDs.distinct("_id.filename")
    print(unique_files)
    return jsonify(unique_files),200

@bp.route("/api/filter", methods=["POST"])
def callFilter():
    call_filter = request.get_json()["filter"]
    filename = request.get_json()["filename"]
    query = query_parser(call_filter)
    query["_id.filename"] = filename
    if not query:
        return "Invalid filter condition", 400
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

@bp.route("/api/match")
def matchSigntures():
    signatures = []
    ID = request.args.get("ID", None)
    filename = request.args.get("filename", None)
    cursor = mongo.db.signatures.find({})
    filters = [(res["_id"],res["filter"]) for res in cursor]
    for call_filter in filters:
        query = query_parser(call_filter[1])
        query["guid"] = ID
        query["_id.filename"] = filename
        if mongo.db.msgs.find_one(query, {"_id":1}):
            signatures.append(call_filter[0])
    return jsonify(signatures)

@bp.route("/api/delete/<filename>")
def deleteFile(filename):
    mongo.db.GUIDs.remove({"_id.filename":filename})  
    mongo.db.msgs.remove({"_id.filename":filename})
    unique_files=mongo.db.GUIDs.distinct("_id.filename")
    return jsonify(unique_files),200

@bp.route('/filters/<filename>',methods=["GET"])
def filter(filename):
    return render_template("filter.html",filename=filename)