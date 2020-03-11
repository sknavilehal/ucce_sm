from pprint import pprint
from .GUIDS import GUIDS
from .legToGuid import legToGuid
from .create_sequence import create_sequence

def parse_cvp_addr(line):
    cvp = line.split()[1]
    cvp = cvp[:-1]
    return cvp

def parser_main(file):
    contents = file.read().decode('latin1').splitlines()
    cvp = parse_cvp_addr(contents[0])
    legtoguid, msgs = legToGuid(contents)
    guids = GUIDS(legtoguid, msgs)
    create_sequence(file.filename, cvp, guids)