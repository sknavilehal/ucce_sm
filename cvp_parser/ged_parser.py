import re

def check_icmss_ivrss(msg):
    if msg["from"] == "ICM_SS" and msg["to"] == "IVR_SS" or msg["from"] == "IVR_SS" and msg["to"] == "ICM_SS":
        return True
    else: return False

def check_icm_icmss(msg):
    if msg["from"] == "ICM" and msg["to"] == "ICM_SS" or msg["from"] == "ICM_SS" and msg["to"] == "ICM":
        return True
    else: return False

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

def parse_label(line):
    label = line.split("Label=")[1].split()[0]
    if label[-1] == ",": label = label[:-1]
    return label

def parse_status(line):
    parts = re.split(r'[\[\]]', line)
    if "process" in parts[3].lower() or "publish" in parts[3].lower():
        status = parts[5]
    else:
        status = parts[3]
    if status == "CONNECT": status += " " + parse_label(line)
    return status

def rename_ucce(msg):
    if msg["to"] == "UCCE": msg["to"] = "ICM"
    if msg["from"] == "UCCE": msg["from"] = "ICM"

def parse_dialogid(msg):
    id = msg.lower().split("dialogid=")[1].split()[0]
    return id

def parse_ged_msg(filename,ged_msg):
    msg = {}
    msg["guid"] = parse_guid(ged_msg)
    msg["file"]=filename
    if "publishing to " in ged_msg.lower():
        msg["to"] = parse_tofro(ged_msg)
        msg["from"] = parse_ss(ged_msg)
    elif "processing from " in ged_msg.lower():
        msg["to"] = parse_ss(ged_msg)
        msg["from"] = parse_tofro(ged_msg)
        if check_icmss_ivrss(msg): return {}

    msg["status"] = parse_status(ged_msg)
    rename_ucce(msg)

    if check_icm_icmss(msg): msg["status"] += " : " + parse_dialogid(ged_msg)

    msg["text"] = ged_msg
    msg["type"] = "ged"
    msg["text"] = ged_msg

    return msg
