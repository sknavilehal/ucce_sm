from .constants import SIP, GED125, GED188, CVP
from .sip_parser import parse_sip_msg
from .ged125_parser import parse_ged125_msg
from .ged188_parser import parse_ged188_msg

def parse_cvp_addr(line):
    cvp = line.split()[1]
    cvp = cvp[:-1]
    return cvp

def GUIDS(device, callmapping, msgs):
    guids = {}
    guid_set = set(callmapping.values())
    for guid in guid_set:
        guids[guid] = {}
        guids[guid]["msgs"] = []
    for msg in msgs:
        if msg[0] == SIP:
            parsed_msg = parse_sip_msg(msg[1])
            call_id = parsed_msg["call_id"]
            if call_id in callmapping.keys():
                guid = callmapping[call_id]
                parsed_msg["GUID"] = guid
                parsed_msg["count"] = msg[2]
                guids[guid]["msgs"].append(parsed_msg)
        elif msg[0] == GED125:
            parsed_msg = parse_ged125_msg(msg[1])
            if parsed_msg and parsed_msg["GUID"] in guid_set:
                parsed_msg["count"] = msg[2]
                guid = parsed_msg["GUID"]
                guids[guid]["msgs"].append(parsed_msg)
        elif msg[0] == GED188:
            parsed_msg = parse_ged188_msg(msg[1])
            if not parsed_msg: continue
            callid = parsed_msg["callid"]
            agent_id = parsed_msg["agent_id"]
            if callid in callmapping.keys():
                guid = callmapping[callid]
            elif agent_id in callmapping.keys():
                guid = callmapping[agent_id]
                
            if guid in guid_set:
                parsed_msg["GUID"] = guid
                parsed_msg["count"] = msg[2]
                guids[guid]["msgs"].append(parsed_msg)
                if "finesse" not in guids[guid]:
                    guids[guid]["finesse"] = parse_cvp_addr(msg[1].splitlines()[0])
        if device == CVP:
            if "cvp" not in guids[guid]:
                guids[guid]["cvp"] = parse_cvp_addr(msg[1].splitlines()[0])
            
    return guids
