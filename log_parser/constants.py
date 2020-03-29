# Device
CUBE = 0
CVP = 1
FINESSE = 2
UNKNOWN = -1

# Protocol
SIP = 10
GED125 = 11 
GED188 = 12

devices = ["CUBE", "CVP", "FINESSE"]

r_to_color = {
    '1': " -[#black]> ",
    '2': " -[#green]> ",
    '3': " -[#yellow]> ",
    '4': " -[#red]> ",
    'B': " -[#orange]> ",
    'I': " -[#blue]> ",
    'R': " -[#blue]> ",
    'P': " -[#blue]> ",
    'C': " -[#blue]> ",
    'O': " -[#blue]> ",
    'N': " -[#blue]> ",
    'S': " -[#blue]> ",
    'M': " -[#blue]> ",
    'U': " -[#blue]> ",
    'A': " -[#blue]> ",
    'E': " -[#blue]> ",
    'D': " -[#blue]> "
}

device_map = {
    ": //": CUBE,
    ": %CVP_": CVP,
    ": %CCBU": FINESSE
}
