from .GUIDS import GUIDS
from .sequence import sequence
from .callMapping import callMapping
from .constants import CVP, UNKNOWN, device_map, devices

def preliminary_run(contents, prelim_sigs):
    device = UNKNOWN
    sig_matches = []
    delimeters = [": //", ": %CVP_", ": %CCBU"]
            
    for content in contents:
        for sig in prelim_sigs:
            if sig not in sig_matches and sig in content:
                sig_matches.append(sig)
        for delimeter in delimeters:
            if device == UNKNOWN and delimeter in content:
                device = device_map[delimeter]
    
    prelim_sigs = [sig for sig in sig_matches]
    return (prelim_sigs, device)

def parser_main(filename, contents, prelim_sigs=[]):
    contents = contents.getvalue().decode('latin1').splitlines()
    
    prelim_sigs, device = preliminary_run(contents, prelim_sigs)
    if device == UNKNOWN: return ("Unknown", {})
    callmapping, msgs = callMapping(device, contents)
    guids = GUIDS(device, callmapping, msgs)
    sequence(device, filename, guids)

    return (devices[device], guids, prelim_sigs)