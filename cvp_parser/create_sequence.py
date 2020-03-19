import os
from pymongo import MongoClient
from plantweb.render import render
from .mappings import r_to_color

client = MongoClient("mongodb://localhost:27017/")
db = client["CVP"]

def create_sequence(filename,cvp, guids):
    for guid in guids.keys():
        sequence = "@startuml\nskinparam sequence {\nLifeLineBorderColor black\nParticipantBorderColor #00bceb\nParticipantBackgroundColor white\nParticipantFontName Consolas\nParticipantFontSize 17\nParticipantFontColor black\n}\n"
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

                if msg["exchange"]["text"] == "ACK": dest = msg["exchange"]["addr"]
                if src == cvp: src = "SIP_SS"
                if dest == cvp: dest = "SIP_SS"
                src = src.replace('-', '_')
                dest = dest.replace('-', '_')

            else:
                src, dest = msg["from"], msg["to"]
                text = msg["status"]

            code = text[0]
            id = db.msgs.insert_one(msg)
            text = " : [[{"+str(id.inserted_id)+"} " + text + "]]\n"
            sequence += src + r_to_color.get(code," -[#black]> ") + dest +text  
            
        sequence += "@enduml"

        doc = {
            "_id": guid,
            "filename": os.path.basename(filename),
            "sequence": sequence,
            
        }
        db.GUIDs.insert_one(doc)


