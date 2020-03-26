import os
from pymongo import MongoClient
from .mappings import r_to_color
from bson.objectid import ObjectId
from plantweb.render import render

client = MongoClient("mongodb://localhost:27017/")
db = client["CVP"]

def create_sequence(device, filename,cvp, guids):
    for guid in guids.keys():
        doc = {}
        doc["from"] = '-'
        doc["to"] = '-'
        src = dest = text = ""
        doc["_id"] = {"filename":filename, "guid":guid}
        sequence = "@startuml\nskinparam sequence {\nLifeLineBorderColor black\nParticipantBorderColor #00bceb\nParticipantBackgroundColor white\nParticipantFontName Consolas\nParticipantFontSize 17\nParticipantFontColor black\n}\n"
        for msg in guids[guid]:
            if msg["type"] == "sip":
                text = msg["exchange"]["text"]
                if msg["exchange"]["type"] == "request":
                    try:
                        src, dest = msg["via"][0]["addr"], msg["to"]["addr"]
                    except IndexError:
                        src, dest = msg["from"]["addr"], msg["to"]["addr"]
                else:
                    try:
                        src, dest = msg["to"]["addr"], msg["via"][0]["addr"]
                    except IndexError:
                        src, dest = msg["to"]["addr"], msg["from"]["addr"]
                if "sdp" in msg.keys():
                    text = text + " W/ SDP"

                if msg["exchange"]["text"] == "ACK": dest = msg["exchange"]["addr"]
                if src == cvp: src = "SIP_SS"
                if dest == cvp: dest = "SIP_SS"
                src = src.replace('-', '_')
                dest = dest.replace('-', '_')

            else:
                src, dest = msg["from"], msg["to"]
                text = msg["status"]
            
            if doc["from"] == '-' and doc["to"] == '-' and device == "cvp" and "DNIS" in msg and "ANI" in msg:
                doc["from"] = msg["ANI"]
                doc["to"] = msg["DNIS"]
            if doc["from"] == '-' and device == "cube" and msg["exchange"]["type"] == "request" and not msg["sent"]:
                doc["from"] = msg["from"]["ext"] + "@" + msg["from"]["addr"]
            if doc["to"] == '-' and device == "cube" and msg["exchange"]["type"] == "request" and msg["sent"]:
                doc["to"] = msg["exchange"]["ext"] + "@" + msg["exchange"]["addr"]

            code = text[0]
            oid = str(ObjectId())
            msg["_id"] = {"filename":os.path.basename(filename), "oid":oid}
            db.msgs.insert_one(msg)
            text = " : [[{"+oid+"} " + text + "]]\n"
            sequence += src + r_to_color.get(code," -[#black]> ") + dest +text  
        
        sequence += "@enduml"

        doc["sequence"] = sequence
        db.GUIDs.insert_one(doc)


