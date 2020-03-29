from .GUIDS import GUIDS
from .callMapping import callMapping
from .sequence import sequence
from .constants import CVP, UNKNOWN, device_map, devices

def parse_cvp_addr(line):
    cvp = line.split()[1]
    cvp = cvp[:-1]
    return cvp

def detect_device(contents):
    delimeters = [": //", ": %CVP_", ": %CCBU"]

    for content in contents:
        for delimeter in delimeters:
            if delimeter in content:
                return device_map[delimeter]
    
    return UNKNOWN

def parser_main(filename, contents):
    contents = contents.getvalue().decode('latin1').splitlines()
    
    cvp = None
    device = detect_device(contents)
    if device == CVP:
        cvp = parse_cvp_addr(contents[0])
    elif device == UNKNOWN:
        return device
    callmapping, msgs = callMapping(device, contents)
    guids = GUIDS(callmapping, msgs)
    sequence(filename,cvp, guids)

    return (devices[device], guids)