import os
import logging
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from cvp_parser.parser_main import parser_main
from flask import Flask, jsonify, Blueprint, render_template, request
from plantweb.render import render

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
    msg_text = mongo.db.msgs.find_one({"_id": ObjectId(id)}, {"text":1})
    msg_text = msg_text["text"]

    return {"msg_text": msg_text}

@app.route("/uploads", methods=["POST"])
def uploads():
    file = request.files['file']
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
    return jsonify(unique_files),200
