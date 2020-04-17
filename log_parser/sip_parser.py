import re
from .constants import SIP
from datetime import datetime
from flask import current_app as app, abort
from .sdp_parser import sdp_parser

def parse_from(line):
    m = re.search(r'sip:(\*?[@0-9a-zA-Z\.\-]+)',line)
    parts = m.group(1).split('@')

    return {"ext":parts[0], "addr":parts[-1]}

def parse_to(line):
    m = re.search(r'sip:(\*?[@0-9a-zA-Z\.\-]+)', line)
    parts = m.group(1).split('@')

    return {"ext":parts[0], "addr":parts[-1]}

def parse_via(line):
    via = line.split()
    proto = via[1].split('/')[2]
    parts = re.split(r'[:;=]', via[2])
    return {"addr":parts[0], "port":parts[1], "branch":parts[-1], "proto":proto}

def parse_callid(line):
    parts = line.split()
    call_id = parts[1].split('@')[0]

    return call_id

def parse_exchange(line):
    match = re.search(r'SIP/2.0 ([1-6]\d\d .+)', line)
    if match:
        return {"type": "response", "text":match.group(1)}
    else:
        m = re.search(r'([A-Z]+) sip:(?:;[a-z0-9\.=]+;)?(\*?[@\d\.a-zA-Z\-]+)', line)
        request = m.group(1)
        parts = m.group(2).split('@')

        ext = parts[0]
        addr = parts[-1]
        return {"type": "request", "text":request,"ext":ext,"addr":addr}
    
def parse_cseq(line):
    parts = line.split()    
    return {"seq":parts[1], "method":parts[2]}

def parse_contact(line):
    uri = line.split()[1][5:-1].split('@')
    ext, addr = uri[0],uri[-1]
    return {"ext":ext, "addr":addr}

def parse_error_code(line):
    m = re.search(r'[3-5]\d\d', line)
    if m: return int(m.group(0))
    else: return 0

def parse_datetime(line):
    _format = re.compile(r'\w{3}\s+\d{1,2}\s+\d\d:\d\d:\d\d.\d{3}')
    match = re.search(r'\w{3}\s+\d{1,2}\s+\d{4}\s+\d\d:\d\d:\d\d.\d{3}', line)
    if match:
        match = ' '.join(match.group().split())
        d = datetime.strptime(match, "%b %d %Y %H:%M:%S.%f")
    elif _format.search(line):
        match = _format.search(line).group()
        match = ' '.join(match.split())
        d = datetime.strptime(match, "%b %d %H:%M:%S.%f")
    else: return None
    return datetime(d.year, d.month, d.day, d.hour, d.minute, d.second, d.microsecond)

def parse_sip_msg(sip_msg):
    line = '\n'.join(sip_msg.splitlines()[0:3])
    msg = {}
    via = []
    msg["sent"] = False
    msg["exchange"] = parse_exchange(line)
    lines = sip_msg.splitlines()
    #msg["datetime"] = parse_datetime(lines[0])
    #msg["error_code"] = 0

    for line in lines:
        if "Via:" in line: via.append(parse_via(line))
        if "From:" in line: msg["from"] = parse_from(line)
        if "Call-ID:" in line: msg["call_id"] = parse_callid(line)
        if "To:" in line: msg["to"] = parse_to(line)
        if "Max-Forwards:" in line: msg["maxfrwrd"] = line.split()[1]
        if "CSeq:" in line and line.index("CSeq:")==0: msg["cseq"] = parse_cseq(line)
        if "User-Agent:" in line: msg["usr_agent"] = line.split()[1]
        if "Content-Type:" in line: msg["cont_type"] = line.split()[1]
        if "Cisco-Guid:" in line: msg["cisco-guid"] = line.split()[1]
        if "Contact:" in line: msg["Contact"] = parse_contact(line)
        if "Date:" in line: msg["DateFmt"] = line.split()[-1]
        if "Content-Length:" in line:
            content_len = int(line.split()[1])
    
    msg["type"] = "sip"
    msg["Via"] = via
    msg["text"] = sip_msg
    msg["error_code"] = parse_error_code(msg["exchange"]["text"])
    if "Sent" in lines[1] or "Sending" in lines[0]: msg["sent"] = True

    if content_len > 0:
        sdp_body = sip_msg.split('\n\n')[1:]
        sdp_body = '\n'.join(sdp_body).strip()
        sdp = sdp_parser(sdp_body)
        if sdp: msg["sdp"] = sdp
    return msg