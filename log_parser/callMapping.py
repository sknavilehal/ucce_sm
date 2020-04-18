import re
from .constants import CUBE,CVP,FINESSE,SIP,GED125,GED188

filtered_cvp_logs = {"Sending", "BEGINING PROCESSING NEW MESSAGE"}
filtered_finesse_logs = {"DECODED_MESSAGE_FROM_CTI_SERVER:", "XMPP_PUBLISH_ASYNCHRONOUS:"}
ignored_finesse_logs = {"CTIQuerySkillGroupStatisticsConf", "Payload=BEFORE PUBLISH"}

def parse_ids(line):
    idx = line.lower().find("guid")
    guid = line[idx:].split('=')[1].strip().split()[0]
    guid = guid.split(',')[0]
    idx = line.lower().find("legid")
    legid = line[idx:].split('=')[1].strip().split()[0].split('@')[0]
    legid = legid.split(',')[0]
    return guid,legid

def parse_call_id(line):
    call_id = line.split()[1].split('@')[0]
    return call_id

def parse_callid(line):
    callid = line.split('callId=')[1].split(',')[0]
    return callid

def parse_agent_ext(line):
    ext = line.split('dnis=')[1].split(',')[0]
    return ext

def isDelimeter(device, line):
    if device == CVP:
        return ": %" in line and line.split("%")[1].split()[0][-1]==":"
    elif device == CUBE:
        return ": //" in line
    elif device == FINESSE:
        return ": %CCBU"in line
    else: return False

def callMapping(device, lines):
    msg=""
    count = 0
    messages=[]
    callmapping = {}
    call_id = None; ccapi = None; ignore_ged125_msg = ignore_sip_msg = ignore_ged188_msg = True

    for line in lines:
        if isDelimeter(device, line):
            if call_id and not ignore_sip_msg:
                messages.append((SIP, msg.strip(), count))
            elif not ignore_ged125_msg:
                messages.append((GED125, msg.strip(), count))
            elif not ignore_ged188_msg:
                messages.append((GED188, msg.strip(), count))
            msg=""
            count += 1
            call_id = ccapi = None
            ignore_ged125_msg = ignore_sip_msg = ignore_ged188_msg = True

        if device == CVP:
            if "guid" in line.lower() and "legid" in line.lower():
                guid, legid = parse_ids(line)
                callmapping[legid] = guid
            if "publishing to " in line.lower() or "processing from " in line.lower():
                ignore_ged125_msg = False
            for log in filtered_cvp_logs:
                if log in line: ignore_sip_msg = False
        elif device == CUBE:
            if "ccsipDisplayMsg:" in line:
                match = re.search(r'/([A-Z0-9]{12})/', line)
                if match and match.group(1) != "000000000000": 
                    ccapi = match.group(1)
                    ignore_sip_msg = False
                elif not match:
                    ignore_sip_msg = False
        elif device == FINESSE:
            if " callId=" in line and " dnis=" in line and "dnis=null" not in line:
                callid = line.split(' callId=')[1].split(',')[0]
                agent_ext = line.split(' dnis=')[1].split(',')[0]
                if agent_ext != '': callmapping[callid] = agent_ext
            if " agentExtension=" in line and " agentID=" in line:
                agent_id = line.split(' agentID=')[1].split(',')[0]
                agent_ext = line.split(' agentExtension=')[1].split(',')[0]
                callmapping[agent_id] = agent_ext
            
            for log in filtered_finesse_logs:
                if log in line: ignore_ged188_msg = False
            for log in ignored_finesse_logs:
                if log in line: ignore_ged188_msg = True
        
        if "Call-ID: " in line:
            call_id = parse_call_id(line)
            if ccapi:
                callmapping[call_id] = ccapi

        msg=msg+"\n"+line
    
    return callmapping, messages