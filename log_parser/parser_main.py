from .GUIDS import GUIDS
from .sequence import sequence
from .callMapping import callMapping
from .constants import CVP, UNKNOWN, device_map, devices

def preliminary_run(contents, alerts):
    device = UNKNOWN
    sig_matches = []
    delimeters = [": //", ": %CVP_", ": %CCBU"]

    time_data = ["", ""]
            
    for content in contents:
        for sig in alerts:
            if sig not in sig_matches and sig in content:
                sig_matches.append(sig)
        for delimeter in delimeters:
            if device == UNKNOWN and delimeter in content:
                device = device_map[delimeter]
    
    if device == CVP:
        time_data[0] = contents[0].split(": ")[2].split('-')[0].strip()
        time_data[1] = contents[-1].split(": ")[2].split('-')[0].strip()
    
    alerts = [sig for sig in sig_matches]
    return (alerts, device, time_data)

def parser_main(filename, contents, alerts=[]):
    contents = contents.getvalue().decode('latin1').splitlines()
    
    alerts, device, time_data = preliminary_run(contents, alerts)
    if device == UNKNOWN: return ("Unknown", {})
    callmapping, msgs = callMapping(device, contents)
    guids = GUIDS(device, callmapping, msgs)
    sequence(device, filename, guids)

    return (devices[device], guids, alerts, time_data)