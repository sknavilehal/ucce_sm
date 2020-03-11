import re
from pprint import pprint

def parse_media(keys):
    codecs = {}
    medias = []
    for m in keys['m']:
        parts = m.split()
        media, port, protocol = parts[0], parts[1], parts[2]
        codes = parts[3:]
        for c in codes:
            codecs[c] = {}
        medias.append({"media":media, "port":port, "protocol":protocol, "codes":codes})

    return (medias, codecs)

def parse_codecs(keys, codecs):
    attrs= {}
    modes = []
    for attr in keys['a']:
        if "rtpmap" in attr:
            m = re.search(r'rtpmap:(\d+) ([a-zA-Z0-9\.\-]+)/(\d+)', attr)
            ptype = m.group(1); name = m.group(2); rate = m.group(3)
            codecs[ptype]["name"] = name
            codecs[ptype]["sample_rate"] = rate
        elif "fmtp" in attr:
            m = re.search(r'fmtp:(\d+) (\S+)\b', attr)
            ptype = m.group(1); params = m.group(2)
            codecs[ptype]["fmtp"] = params
        elif re.search(r'\w+:', attr):
            parts = attr.split(':')
            attrs[parts[0]] = parts[1]
        else:
            modes.append(attr)

    return (codecs, attrs, modes)

def parse_connection(keys):
    conn = keys['c'][0].split()

    return (conn[0],conn[1],conn[2])

def parse_origin(keys):
    parts = keys['o'][0].split()
    username, sess_version = parts[0],parts[2]
    return  (username,sess_version)

def sdp_parser(body):
    keys = {}
    for line in body.splitlines():
        if line.find("=") == 1:
            parts = line.split('=')
            key, value = parts[0],'='.join(parts[1:])
            if key not in keys: keys[key] = []
            keys[key].append(value)
    if not keys: return {}
    medias, codecs = parse_media(keys)
    codecs, attrs, modes = parse_codecs(keys, codecs)
    net_type, addr_type, addr = parse_connection(keys)
    username, sess_version = parse_origin(keys)

    for k,v in codecs.items():
        v["code"] = k
    codecs =[v for v in codecs.values()]
    
    sdp = \
    {
        "medias":medias,
        "codecs":codecs,
        "connection": {"addr_type":addr_type, "addr": addr},
        "username":username,
        "sess_version":sess_version,
        "modes": modes,
        "net_type": net_type
    }
    for attr in attrs.keys():
        sdp[attr] = attrs[attr]
    return sdp

multiline = """v=0
o=CiscoSystemsSIP-GW-UserAgent 5181 3975 IN IP4 10.106.122.150
s=SIP Call
c=IN IP4 10.106.122.150
t=0 0
m=audio 11634 RTP/AVP 0 8 18 101
c=IN IP4 10.106.122.150
a=rtpmap:0 PCMU/8000
a=rtpmap:8 PCMA/8000
a=rtpmap:18 G729/8000
a=fmtp:18 annexb=no
a=rtpmap:101 telephone-event/8000
a=fmtp:101 0-16
a=ptime:20
"""

if __name__ == "__main__":
    sdp = sdp_parser(multiline)
    pprint(sdp)
