import re
import ast

def query_parser(query):
    parts = query.split(' or ')

    output = "{ '$or': ["

    for part in parts:
        output += "{"
        ands = part.replace(' and ', ',')
        output += ands
        output += "},"

    output += "]}"

    return ast.literal_eval(output)
