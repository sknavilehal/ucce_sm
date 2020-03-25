from .GUIDS import GUIDS
from .mappings import device
from .legToGuid import legToGuid
from .create_sequence import create_sequence

def parse_cvp_addr(line):
    cvp = line.split()[1]
    cvp = cvp[:-1]
    return cvp

def detect_device(contents):
    delimeters = [": //", ": %CVP_", ": %_"]

    for content in contents:
        for delimeter in delimeters:
            if delimeter in content:
                return device[delimeter]
    
    return "unknown"

def parser_main(filename, contents):
    contents = contents.getvalue().decode('latin1').splitlines()
    
    cvp = None
    device = detect_device(contents)
    if device == "cvp":
        cvp = parse_cvp_addr(contents[0])
    elif device == "unkown":
        return device
    legtoguid, msgs = legToGuid(device, contents)
    guids = GUIDS(legtoguid, msgs)
    create_sequence(device, filename,cvp, guids)

    return device