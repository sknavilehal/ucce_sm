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

def legToGuid(lines):
    messages=[]
    msg=""
    call_id = None; ignore_ged_msg = ignore_sip_msg = True
    legtoguid = {}
    #ignored_logs = {"UserCB:", "TransactionManagement:"} 
    filtered_logs = {"Sending", "BEGINING PROCESSING NEW MESSAGE"}
    for line in lines:
        if " %" in line and line.split("%")[1].split()[0][-1]==":":
            if call_id and not ignore_sip_msg:
                messages.append(("sip", msg.strip()))
            elif not ignore_ged_msg:
                messages.append(("ged", msg.strip()))
            msg=""
            call_id = None
            ignore_ged_msg = ignore_sip_msg = True

        if "guid" in line.lower() and "legid" in line.lower():
            guid, legid = parse_ids(line)
            legtoguid[legid] = guid
        
        if "Call-ID: " in line:
            call_id = parse_callid(line)
        for log in filtered_logs:
            if log in line:
                ignore_sip_msg = False
        
        if "publishing to " in line.lower() or "processing from " in line.lower():
            ignore_ged_msg = False

        msg=msg+"\n"+line
    
    return legtoguid, messages