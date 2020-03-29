import re
from datetime import datetime

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

#Function to parse all the attributes from the ged message
def parse_attributes(ged_msg, msg):
    words = ged_msg.split(" ")

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

def parse_datetime(line):
    match = re.search(r'\w{3}\s+\d{1,2}\s+\d{4}\s+\d\d:\d\d:\d\d.\d{3}', line)
    if match:
        match = ' '.join(match.group().split())
        d = datetime.strptime(match, "%b %d %Y %H:%M:%S.%f")
        return datetime(d.year, d.month, d.day, d.hour, d.minute, d.second, d.microsecond)
    else: return None

def parse_ged_msg(ged_msg):
    msg = {}
    msg["guid"] = parse_guid(ged_msg)
    msg["datetime"] = parse_datetime(ged_msg.splitlines()[0])
    
    if "publishing to " in ged_msg.lower():
        msg["sent"] = True
        msg["to"] = parse_tofro(ged_msg)
        msg["from"] = parse_ss(ged_msg)
    elif "processing from " in ged_msg.lower():
        msg["sent"] = False
        msg["to"] = parse_ss(ged_msg)
        msg["from"] = parse_tofro(ged_msg)
        if check_icmss_ivrss(msg): return {}

    msg["event"] = parse_status(ged_msg)
    msg["status"] = parse_status(ged_msg)
    rename_ucce(msg)

    if check_icm_icmss(msg): msg["status"] += " : " + parse_dialogid(ged_msg)

    #Sending the ged message line to parse the attributes from it.
    parse_attributes(ged_msg, msg)

    msg["type"] = "ged"
    msg["text"] = ged_msg

    return msg
