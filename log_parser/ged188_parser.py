import xmltodict
import pprint
import json
import re

def parse_agent_id(ged_msg):
    #print('\n\n\n', ged_msg.splitlines()[0])
    node_text = ged_msg.split()[8].split(']')[0]
    m = re.search(r'%\[NodeId=/finesse/api/User/(\d+)', node_text)
    return m.group(1)

def parse_ged188_msg(ged_msg):
    msg = {}
    msg["type"] = "ged188"
    msg["text"] = ged_msg
    msg["agent_ext"] = msg["agent_id"] = msg["callid"] = None

    if "FROM_CTI_SERVER:" in ged_msg:
        msg["from"] = "CTI_SERVER"
        msg["to"] = "FINESSE"
        msg["event"] = "FROM_CTI_SERVER"
        if " callId=" in ged_msg in ged_msg:
            msg["callid"] = ged_msg.split(' callId=')[1].split(',')[0]
        if " agentID=" in ged_msg in ged_msg:
            msg["agent_id"] = ged_msg.split(' agentID=')[1].split(',')[0]
    elif "%[NodeId=/finesse/api/User/" in ged_msg:
        msg["from"] = "FINESSE"
        msg["to"] = "Agent_Desktop"
        msg["event"] = "XMPP_PUB_ASYNC"
        msg["agent_id"] = parse_agent_id(ged_msg)
        #    xml = ged_msg.split('[Payload=')[1].split(']: Publishing')[0]
        #xml = ged_msg.split('[Payload=')[1].split(']: Publishing')[0]
        #xml = xml.replace('&lt;', '<')
        #xml = xml.replace('&gt;', '>')
        #msg["text"] = json.dumps(xmltodict.parse(xml), indent=2)
        msg["text"] = ged_msg
    else: return {}

    return msg