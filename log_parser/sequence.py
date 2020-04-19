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

def sequence_line_sip(msg):
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
    src = src.replace('-', '_')
    dest = dest.replace('-', '_')

    return src,dest,text

def sequence(device, filename, guids):
    for guid in guids.keys():
        doc = {}
        doc["from"] = '-'
        doc["to"] = '-'
        src = dest = text = ""
        doc["_id"] = {"filename":filename, "guid":guid}
        if device == FINESSE:
            doc["agent_name"] = '-'
            doc["agent_id"] = '-'

        sequence = "@startuml\nskinparam sequence {\nLifeLineBorderColor black\nParticipantBorderColor #00bceb\nParticipantBackgroundColor white\nParticipantFontName Consolas\nParticipantFontSize 17\nParticipantFontColor black\n}\n"
        for msg in guids[guid]["msgs"]:
            if msg["type"] == "sip":
                src,dest,text = sequence_line_sip(msg)
                if device == CVP:
                    if src == guids[guid]["cvp"]: src = "SIP_SS"
                    if dest == guids[guid]["cvp"]: dest = "SIP_SS"

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
                text = msg["message"]
                try: 
                    agent_name = msg["xmltodict"]["Update"]["data"]["user"]["firstName"]
                    agent_id = msg["agent_id"]
                    if doc["agent_name"] == '-':
                        doc["agent_name"] = agent_name
                    if doc["agent_id"] == '-':
                        doc["agent_id"] = agent_id
                except KeyError as e:
                    print("Key Error: ", str(e))

            code = text[0]
            oid = str(ObjectId())
            msg["_id"] = {"filename":filename, "oid":oid}
            text = " : [[{"+oid+"} " + text + "]]\n"
            sequence += src + r_to_color.get(code," -[#black]> ") + dest +text  
        
        sequence += "@enduml"

        doc["sequence"] = sequence
        guids[guid]["doc"] = doc