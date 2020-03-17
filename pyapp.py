import os
import logging
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from cvp_parser.parser_main import parser_main
from cvp_parser.query_parser import query_parser
from flask import Flask, jsonify, Blueprint, render_template, request, Response
from plantweb.render import render
from datetime import date,datetime

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/CVP"
mongo = PyMongo(app)
CORS(app)

#gunicorn_logger = logging.getLogger('gunicorn.error')
#app.logger.handlers = gunicorn_logger.handlers
#app.logger.setLevel(gunicorn_logger.level)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/statistics/<filename>")
def statistics(filename):
    print(filename)
    return render_template("statistics.html",filename=filename)

@app.route("/files")
def files():
    return render_template("files.html")

@app.route("/api/GUIDs/<string:filename>")
def get_GUIDs(filename):
    cursor = mongo.db.GUIDs.find({"filename":filename})
    CCAPIs = [[res["_id"]] for res in cursor]
    return jsonify(CCAPIs),200

@app.route("/api/GUID/<string:id>")
def get_GUID(id):
    sequence = mongo.db.GUIDs.find_one({"_id":id},{"sequence":1})
    sequence = sequence["sequence"]
    svg = render(sequence, engine="plantuml", format="svg")
    svg = svg[0].decode('utf-8')

    return {"svg":svg},200

@app.route("/api/message/<string:id>")
def get_message(id):
    print(id)
    msg_text = mongo.db.msgs.find_one({"_id": ObjectId(id)}, {"text":1})
    msg_text = msg_text["text"]
    print(msg_text)
    return {"msg_text": msg_text}

@app.route("/uploads", methods=["POST"])
def uploads():
    file = request.files['file']
    # Textual month, day and year
    today = date.today()	
    d2 = today.strftime("%B %d, %Y")
    #print("d2 =", d2)
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    #print("Current Time =", current_time)
    time1=d2+" "+current_time
    unique_files=mongo.db.GUIDs.distinct("filename")
    if ( file.filename in unique_files):
        return "Exists",400
    parser_main(file)
    return render_template("index.html"), 200

@app.route('/diagram/<string:ID>',methods=["GET"])
def diagram(ID):
    return render_template("diagram.html", guid=ID)

@app.route("/api/files")
def getfilenames():
    unique_files=mongo.db.GUIDs.distinct("filename")
    print(unique_files)
    return jsonify(unique_files),200

@app.route("/api/filter", methods=["POST"])
def callFilter():
    filter = request.get_json()["filter"]
    query = query_parser(filter)
    print(query)
    guids = mongo.db.msgs.distinct("guid",query)

    return {"guids": guids, "query":str(query)}

@app.route("/api/signature", methods=["POST"])
def signatureEntry():
    call_filter = request.get_json()["filter"]
    signature = request.get_json()["signature"]
    try:
        id = mongo.db.signatures.insert_one({"_id":signature, "filter":call_filter})
    except Exception:
        return "signature already exists", 400
    return id.inserted_id, 200

@app.route("/api/delete/<filename>")
def deleteFile(filename):
    x=mongo.db.GUIDs.remove({"filename":filename})
    y=mongo.db.msgs.remove({"file":filename})
    unique_files=mongo.db.GUIDs.distinct("filename")
    return jsonify(unique_files),200