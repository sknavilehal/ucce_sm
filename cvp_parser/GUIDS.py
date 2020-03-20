from .sip_parser import parse_sip_msg
from .ged_parser import parse_ged_msg

def GUIDS(legtoguid, msgs):
    guids = {}
    guid_set = set(legtoguid.values())
    for guid in guid_set:
        guids[guid] = []
    for msg in msgs:
        if msg[0] == "sip":
            parsed_msg = parse_sip_msg(msg[1])
            call_id = parsed_msg["call_id"]
            if call_id in legtoguid.keys():
                guid = legtoguid[call_id]
                parsed_msg["guid"] = guid
                guids[guid].append(parsed_msg)
        else:
            parsed_msg = parse_ged_msg(msg[1])
            if parsed_msg and parsed_msg["guid"] in guid_set:
                guid = parsed_msg["guid"]
                guids[guid].append(parsed_msg)

    return guids
