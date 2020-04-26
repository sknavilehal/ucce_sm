import xmltodict
import pprint
import json
import re

def parse_agent_id(ged_msg):
    node_text = ged_msg.split()[8].split(']')[0]
    m = re.search(r'%\[NodeId=/finesse/api/User/(\d+)', node_text)
    return m.group(1)

def parse_attributes(ged_msg, msg):
    words = ged_msg.split()

    for word in words :

        #Checking for words which have "key=value" format. 
        #Note: If the value is an empty string then adding it the same way it exists.
        if "=" in word:
            attribute = word.split("=")  #attribute[0] becomes key and attribute[1] becomes value

            #Error case where value is ending with a ',' or '}'
            if attribute[1] != '' and attribute[1][-1] in [',','}']  :
                attribute[1]=attribute[1][:-1]

            #Error case where key is starting a '{'
            if attribute[0][0] in ['{','_']:
                attribute[0] = attribute[0][1:]

            #Error case where splitting by ' ' wasn't sufficient and gave the format - 'randomtext,key=value'
            if ',' in attribute[0]:
                attribute[0] = attribute[0].split(',')[-1]

            #If the attribute is not in the dictionary then add it 
            if attribute[0] not in msg.keys():
                msg[attribute[0]] = attribute[1]

def add_event_data(key, event, msg):
    if key not in msg: return None
    msg["message"] += event + msg[key]

def parse_ged188_msg(ged_msg):
    msg = {}
    msg["type"] = "ged188"
    msg["text"] = ged_msg
    msg["agent_id"] = msg["callid"] = msg["agent_name"] = '-'

    if "FROM_CTI_SERVER:" in ged_msg:
        parse_attributes(ged_msg, msg)
        msg["from"] = "CTI_SERVER"
        msg["to"] = "FINESSE"
        msg["message"] = ged_msg.split('cti_message=')[1].split()[0]
        if "agentState=" in ged_msg:
            idx = ged_msg.index("agentState=")
            try:
                msg["message"] += ", State: " + re.split(r'[\(\)]', ged_msg[idx:])[1]
            except: pass
        add_event_data("eventReasonCode", ", Code: ", msg)
        add_event_data("skillGroupNumber", ", SG: ", msg)

        if " callId=" in ged_msg in ged_msg:
            msg["callid"] = ged_msg.split(' callId=')[1].split(',')[0]
        if " agentID=" in ged_msg in ged_msg:
            msg["agent_id"] = ged_msg.split(' agentID=')[1].split(',')[0]
    elif "%[NodeId=/finesse/api/User/" in ged_msg:
        msg["from"] = "FINESSE"
        msg["to"] = "Agent_Desktop"
        msg["message"] = ' '.join(ged_msg.split()[2:6])
        msg["agent_id"] = parse_agent_id(ged_msg)
        xml = ged_msg.split('[Payload=')[1].split(']: Publishing')[0]
        xml = xml.replace('&lt;', '<')
        xml = xml.replace('&gt;', '>')
        msg["xmltodict"] = xmltodict.parse(xml)
        state = '-'
        try:
            state = msg["xmltodict"]["Update"]["data"]["user"]["state"]
        except: pass
        try:
            state = msg["xmltodict"]["Update"]["data"]["dialogs"]["Dialog"]["participants"]["Participant"][0]["state"]
        except: pass
        try:
            state = msg["xmltodict"]["Update"]["data"]["dialogs"]["Dialog"]["participants"]["Participant"]["state"]
        except: pass
        try:
            state = msg["xmltodict"]["Update"]["data"]["dialog"]["participants"]["Participant"]["state"]
        except: pass
        try:
            state = msg["xmltodict"]["Update"]["data"]["dialog"]["participants"]["Participant"][0]["state"]
        except: pass
        if state != '-':
            msg["message"] += ", State: " + state
            
        msg["text"] = json.dumps(xmltodict.parse(xml), indent=2)
    else: return {}

    return msg