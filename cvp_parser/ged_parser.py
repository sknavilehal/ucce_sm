import re

def parse_guid(line):
    idx = line.lower().find("guid")
    guid = line[idx:].split('=')[1].strip().split()[0]
    if guid[-1] == ',':
        guid = guid[:-1]
    return guid

def parse_tofro(line):
    idx = line.lower().find("publish")
    idx = max(line.lower().find("process"), idx)
    system = line[idx:].split()[2]
    if system[-1] == "]": system = system[:-1]
    return system

def parse_ss(line):
    subsystem=re.search(r'%CVP_\d{1,2}_\d{1,2}_([A-Z]+)\-\d{1,2}\-[A-Z]+:', line)
    ss = subsystem.group(1) + "_SS"
    return ss

def parse_status(line):
    parts = re.split(r'[\[\]]', line)
    if "process" in parts[3].lower() or "publish" in parts[3].lower():
        status = parts[5]
    else:
        status = parts[3]
    return status

def rename_ucce(msg):
    if msg["to"] == "UCCE": msg["to"] = "ICM"
    if msg["from"] == "UCCE": msg["from"] = "ICM"

def filter_msg(msg):
    if msg["from"] == "ICM_SS" and msg["to"] == "IVR_SS" or msg["from"] == "IVR_SS" and msg["to"] == "ICM_SS":
        return True
    else: return False

def parse_ged_msg(ged_msg):
    msg = {}
    msg["guid"] = parse_guid(ged_msg)
    if "publishing to " in ged_msg.lower():
        msg["to"] = parse_tofro(ged_msg)
        msg["from"] = parse_ss(ged_msg)
    elif "processing from " in ged_msg.lower():
        msg["to"] = parse_ss(ged_msg)
        msg["from"] = parse_tofro(ged_msg)
        if filter_msg(msg): return {}
    
    rename_ucce(msg)
    msg["status"] = parse_status(ged_msg)
    msg["text"] = ged_msg
    msg["type"] = "ged"
    msg["text"] = ged_msg

    return msg
