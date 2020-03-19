import re
import ast
import json
def query_parser(query):
    parts = query.split(' or ')
    output = "{ '$or': ["

    for part in parts:
        ands = part.replace(' and ', ',')
        output += "{"
        output += ands
        output += "},"
        
    output += "]}"
    print(output)
    return ast.literal_eval(output)
