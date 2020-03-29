from .constants import SIP, GED125, GED125
from .sip_parser import parse_sip_msg
from .ged_parser import parse_ged_msg

def GUIDS(callmapping, msgs):
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
                parsed_msg["guid"] = guid
                parsed_msg["count"] = msg[2]
                guids[guid]["msgs"].append(parsed_msg)
        elif msg[0] == GED125:
            parsed_msg = parse_ged_msg(msg[1])
            if parsed_msg and parsed_msg["guid"] in guid_set:
                parsed_msg["count"] = msg[2]
                guid = parsed_msg["guid"]
                guids[guid]["msgs"].append(parsed_msg)

    return guids
