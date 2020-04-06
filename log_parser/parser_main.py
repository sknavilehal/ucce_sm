from .GUIDS import GUIDS
from .callMapping import callMapping
from .sequence import sequence
from .constants import CVP, UNKNOWN, device_map, devices

def detect_device(contents):
    delimeters = [": //", ": %CVP_", ": %CCBU"]

    for content in contents:
        for delimeter in delimeters:
            if delimeter in content:
                return device_map[delimeter]
    
    return UNKNOWN

def parser_main(filename, contents):
    contents = contents.getvalue().decode('latin1').splitlines()
    
    device = detect_device(contents)
    if device == UNKNOWN: return ("Unknown", {})
    callmapping, msgs = callMapping(device, contents)
    guids = GUIDS(callmapping, msgs)
    sequence(filename, guids)

    return (devices[device], guids)