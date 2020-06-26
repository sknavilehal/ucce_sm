from .GUIDS import GUIDS
from .sequence import sequence
from .callMapping import callMapping
from .constants import CVP, UNKNOWN, device_map, devices

def preliminary_run(contents, alerts):
    device = UNKNOWN
    sig_matches = {}
    delimeters = [": //", ": %CVP_", ": %CCBU"]

    time_data = ["-", "-"]
 
    for content in contents:
        content = content.decode('latin1')
        for sig in alerts:
            if sig in content:
                if sig not in sig_matches: sig_matches[sig] = []
                sig_matches[sig].append(contents.tell() - len(content))
        for delimeter in delimeters:
            if device == UNKNOWN and delimeter in content:
                device = device_map[delimeter]
    contents.seek(0)
    for content in contents:
        content = content.decode('latin1')
        if device == CVP and ": %" in content:
            if time_data[0] == '-':
                time_data[0] = content.split(": ")[2].split('-')[0].split('+')[0].strip()
            time_data[1] = content.split(": ")[2].split('-')[0].split('+')[0].strip()

    return (sig_matches, device, time_data)

def parser_main(filename, contents, alerts=[]):
    contents.seek(0)
    sig_matches, device, time_data = preliminary_run(contents, alerts); contents.seek(0)
    contents = contents.getvalue().decode('latin1').splitlines()
    
    #sig_matches, device, time_data = preliminary_run(contents, alerts)
    if device == UNKNOWN: return ("Unknown", {})
    callmapping, msgs = callMapping(device, contents)
    guids = GUIDS(device, callmapping, msgs)
    sequence(device, filename, guids)

    return (devices[device], guids, sig_matches, time_data)