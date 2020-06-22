import re

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
    conns = []
    for con in keys['c']:
        parts = con.split()
        conns.append({"net_type":parts[0] ,"addr_type":parts[1], "addr": parts[2]})

    return conns

def parse_origin(keys):
    parts = keys['o'][0].split()
    username, sess_version = parts[0],parts[2]
    return  (username,sess_version)

def sdp_parser(body):
    keys = {}; attrs = {}; modes = []; codecs = {}; connections = []
    username = 'N/A'; sess_version = 'N/A'
    for line in body.splitlines():
        if line.find("=") == 1:
            parts = line.split('=')
            key, value = parts[0],'='.join(parts[1:])
            if key not in keys: keys[key] = []
            keys[key].append(value)
    if not keys: return {}
    medias, codecs = parse_media(keys)
    if 'a' in keys:
        codecs, attrs, modes = parse_codecs(keys, codecs)
    if 'c' in keys:
        connections = parse_connection(keys)
    if 'o' in keys:
        username, sess_version = parse_origin(keys)

    for k,v in codecs.items():
        v["code"] = k
    codecs =[v for v in codecs.values()]
    
    sdp = \
    {
        "medias":medias,
        "codecs":codecs,
        "connections": connections,
        "username":username,
        "sess_version":sess_version,
        "modes": modes,
    }
    for attr in attrs.keys():
        sdp[attr] = attrs[attr]
    return sdp

