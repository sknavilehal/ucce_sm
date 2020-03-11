import re
from .sdp_parser import sdp_parser
from pprint import pprint

def parse_from(line):
    m = re.search(r'sip:([@0-9a-zA-Z\.]+)[>;:]?',line)
    parts = m.group(1).split('@')

    return {"ext":parts[0], "addr":parts[-1]}

def parse_to(line):
    m = re.search(r'sip:([@0-9a-zA-Z\.]+)[>;:]?', line)
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
    match = re.search(r'SIP/2.0 ([1-6]\d\d [a-zA-Z]+)', line)
    if match:
        return {"type": "response", "text":match.group(1)}
    else:
        m = re.search(r' ([A-Z]+) sip:([@\d\.a-zA-Z]+)', line)
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

def parse_sip_msg(sip_msg):
    line = ' '.join(sip_msg.splitlines()[0:2])
    msg = {}
    via = []
    msg["exchange"] = parse_exchange(line)
    lines = sip_msg.splitlines()
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
        if "contact:" in line: msg["contact"] = parse_contact(line)
        if "Content-Length:" in line:
            content_len = int(line.split()[1])
    
    msg["type"] = "sip"
    msg["via"] = via
    msg["text"] = sip_msg
    msg["text"] = sip_msg
    msg["error_code"] = parse_error_code(msg["exchange"]["text"])

    if content_len > 0:
        sdp_body = sip_msg.split('\n\n')[1:]
        sdp_body = '\n'.join(sdp_body).strip()
        sdp = sdp_parser(sdp_body)
        if sdp: msg["sdp"] = sdp
    return msg

sip_msg = """
4804: 10.127.235.157: feb 13 2020 23:26:53.466 -0800: %_usercb-6-com.dynamicsoft.dslibs.dsualibs.dssipllapi.llsm.client.usercb: invite sip:67803@10.127.235.157:5060 SIP/2.0
via: sip/2.0/tcp 10.127.235.157:5060;branch=z9hg4bksqlfguqppswwllrkxykwcq~~69
to: "testph1" <sip:2001@10.106.121.203>;tag=2a5add0-a5
from: <sip:67801@10.127.235.157>;tag=dsa9fcede4
call-id: 4d862955-4e2f11ea-810b8273-88689a65@10.106.121.203
cseq: 2 invite
content-length: 197
date: fri, 14 feb 2020 07:06:18 gmt
allow: invite, options, bye, cancel, ack, prack, update, refer, subscribe, notify, info, register
allow-events: telephone-event
remote-party-id: "testph1" <sip:2001@10.106.121.203>;party=called;screen=no;privacy=off
contact: <sip:2001@10.106.121.203:5060>
supported: replaces
supported: sdp-anat
supported: timer
server: cisco-sipgateway/ios-15.5.3.m3
session-expires: 1800;refresher=uas
require: timer
content-type: application/sdp

v=0
o=ciscosystemssip-gw-useragent 6175 8133 in ip4 10.106.121.203
s=sip call
c=in ip4 10.106.121.203
t=0 0
m=audio 16540 rtp/avp 0
c=in ip4 10.106.121.203
a=rtpmap:0 pcmu/8000
a=ptime:20
"""

if __name__ == "__main__":
    msg = parse_sip_msg(sip_msg)
    pprint(msg)
