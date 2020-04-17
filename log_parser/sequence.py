import os
from .constants import r_to_color
from bson.objectid import ObjectId
from plantweb.render import render
from .constants import GED125, SIP, GED188, FINESSE, CVP

#Function to add 'to' and 'from' for the call summary table using 'dnis' and 'ani' attributes
def add_dnis_and_ani(doc,msg):
    if "DNIS" in msg and "ANI" in msg:
        doc["from"] = msg["ANI"]
        doc["to"] = msg["DNIS"]

#Function to add 'to' and 'from' for the call summary table using first sip message
def add_to_and_from(doc, msg):
    if msg["exchange"]["type"] == "request":
        doc["from"] = msg["from"]["ext"] 
        doc["to"] = msg["exchange"]["ext"] 

def sequence(device, filename, guids):
    for guid in guids.keys():
        doc = {}
        doc["from"] = '-'
        doc["to"] = '-'
        src = dest = text = ""
        doc["_id"] = {"filename":filename, "guid":guid}
        if device == FINESSE:
            try:
                doc["agent_id"] = guids[guid]["agent_id"]
            except:
                doc["agent_id"] = '-'

        sequence = "@startuml\nskinparam sequence {\nLifeLineBorderColor black\nParticipantBorderColor #00bceb\nParticipantBackgroundColor white\nParticipantFontName Consolas\nParticipantFontSize 17\nParticipantFontColor black\n}\n"
        for msg in guids[guid]["msgs"]:
            if msg["type"] == "sip":
                text = msg["exchange"]["text"]
                if msg["exchange"]["type"] == "request":
                    try:
                        src, dest = msg["Via"][0]["addr"], msg["to"]["addr"]
                    except IndexError:
                        src, dest = msg["from"]["addr"], msg["to"]["addr"]
                else:
                    try:
                        src, dest = msg["to"]["addr"], msg["Via"][0]["addr"]
                    except IndexError:
                        src, dest = msg["to"]["addr"], msg["from"]["addr"]
                if "sdp" in msg.keys():
                    text = text + " W/ SDP"

                if msg["exchange"]["text"] == "ACK": dest = msg["exchange"]["addr"]
                if device == CVP:
                    if src == guids[guid]["cvp"]: src = "SIP_SS"
                    if dest == guids[guid]["cvp"]: dest = "SIP_SS"
                src = src.replace('-', '_')
                dest = dest.replace('-', '_')

                #Using the first sip message to get the 'to' and 'from' for the call summary table
                if doc["from"] == '-' and doc["to"] == '-':
                    add_to_and_from(doc, msg)
            elif msg["type"] == "ged125":
                src, dest = msg["from"], msg["to"]
                text = msg["status"]

                #If there are no sip messages, then using 'dnis' and 'ani' attributes to get 'to' and 'from' 
                if doc["from"] == '-' and doc["to"] == '-':
                    add_dnis_and_ani(doc,msg)
            elif msg["type"] == "ged188":
                src, dest = msg["from"], msg["to"]
                text = msg["event"]

            code = text[0]
            oid = str(ObjectId())
            msg["_id"] = {"filename":filename, "oid":oid}
            text = " : [[{"+oid+"} " + text + "]]\n"
            sequence += src + r_to_color.get(code," -[#black]> ") + dest +text  
        
        sequence += "@enduml"

        doc["sequence"] = sequence
        guids[guid]["doc"] = doc