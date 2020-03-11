import re

def parse_guid(line):
    idx = line.lower().find("guid")
    guid = line[idx:].split('=')[1].strip().split()[0]
    if guid[-1] == ',':
        guid = guid[:-1]
    return guid

def parse_system(line):
    idx = line.lower().find("publish")
    idx = max(line.lower().find("process"), idx)
    system = line[idx:].split()[2]
    if system[-1] == "]": system = system[:-1]
    return system

def parse_ss(line):
    subsystem=re.search(r'%CVP_\d{1,2}_\d{1,2}_([A-Z]+)\-\d{1,2}\-[A-Z]+:', line)
    ss = subsystem.group(1) + "_SS"
    return ss

def parse_cvp_addr(line):
    cvp = line.split()[1]
    cvp = cvp[:-1]
    return cvp

def parse_status(line):
    parts = re.split(r'[\[\]]', line)
    if parts[-2] == "0":
        status = parts[-4].upper()
    else:
        status = parts[-2].upper()
    return status

def parse_ged_msg(ged_msg):
    msg = {}
    #cvp = parse_cvp_addr(ged_msg)
    msg["guid"] = parse_guid(ged_msg)
    if "publishing to " in ged_msg.lower():
        msg["to"] = parse_system(ged_msg)
        msg["from"] = parse_ss(ged_msg)
    elif "processing from " in ged_msg.lower():
        msg["to"] = parse_ss(ged_msg)
        msg["from"] = parse_system(ged_msg)
    msg["status"] = parse_status(ged_msg)
    msg["text"] = ged_msg
    msg["type"] = "ged"
    msg["text"] = ged_msg

    return msg
