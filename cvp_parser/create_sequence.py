import hashlib
import os
from pymongo import MongoClient
from plantweb.render import render

client = MongoClient("mongodb://localhost:27017/")
db = client["CVP"]

def create_sequence(filename, cvp, guids):
    for guid in guids.keys():

        sequence = "@startuml\n"
        src = dest = text = ""
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

                if src == cvp: src = "SIP_SS"
                if dest == cvp: dest = "SIP_SS"

            else:
                src, dest = msg["from"], msg["to"]
                if src == "UCCE": src = "ICM"
                if dest == "UCCE": dest = "ICM"
                text = msg["status"]

            id = hashlib.sha1(msg["text"].encode()).hexdigest()
            text = " : [[{"+id+"} " + text + "]]\n"
            sequence += src + " -> " + dest +text

            msg["_id"] = id
            db.msgs.insert_one(msg)
        
        sequence += "@enduml"

        doc = {
            "_id": guid,
            "filename": os.path.basename(filename),
            "sequence": sequence
        }
        db.GUIDs.insert_one(doc)


