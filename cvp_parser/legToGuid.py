import re

def parse_ids(line):
    idx = line.lower().find("guid")
    guid = line[idx:].split('=')[1].strip().split()[0]
    if guid[-1] == ',':
        guid = guid[:-1]
    idx = line.lower().find("legid")
    legid = line[idx:].split('=')[1].strip().split()[0].split('@')[0]
    if legid[-1] == ',':
        legid = legid[:-1]
    return guid,legid

def parse_callid(line):
    call_id = line.split()[1].split('@')[0]
    return call_id

def isDelimeter(device, line):
    if device == "cvp":
        return ": %" in line and line.split("%")[1].split()[0][-1]==":"
    elif device == "cube":
        return ": //" in line
    else: return False

def legToGuid(device, lines):
    msg=""
    messages=[]
    legtoguid = {}
    call_id = None; ccapi = None; ignore_ged_msg = ignore_sip_msg = True
    #ignored_logs = {"UserCB:", "TransactionManagement:"} 
    filtered_logs = {"Sending", "BEGINING PROCESSING NEW MESSAGE"}
    for line in lines:
        if isDelimeter(device, line):
            if call_id and not ignore_sip_msg:
                messages.append(("sip", msg.strip()))
            elif not ignore_ged_msg:
                messages.append(("ged", msg.strip()))
            msg=""
            call_id = ccapi = None
            ignore_ged_msg = ignore_sip_msg = True

        if device == "cvp":
            if "guid" in line.lower() and "legid" in line.lower():
                guid, legid = parse_ids(line)
                legtoguid[legid] = guid
            if "publishing to " in line.lower() or "processing from " in line.lower():
                ignore_ged_msg = False
            for log in filtered_logs:
                if log in line:
                    ignore_sip_msg = False
        elif device == "cube":
            if "ccsipDisplayMsg:" in line:
                match = re.search(r'/([A-Z0-9]{12})/', line)
                if match and match.group(1) != "000000000000": 
                    ccapi = match.group(1)
                    ignore_sip_msg = False
                elif not match:
                    ignore_sip_msg = False
        
        if "Call-ID: " in line:
            call_id = parse_callid(line)
            if ccapi:
                legtoguid[call_id] = ccapi

        msg=msg+"\n"+line
    
    return legtoguid, messages