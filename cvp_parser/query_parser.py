import re
import ast
import json

def en_quote(string):
    return "'" + string + "'"

def query_parser(query):
    parts = query.split(' or ')
    output = "{ '$or': ["

    for part in parts:
        ands = part.split(' and ')
        output += "{"
        for _and in ands:
            ops = re.split(r'(?:==|!=)', _and)
            try:
                key, value = ops[0], ops[1]
            except IndexError:
                return {}
            if "==" in _and:
                output += en_quote(key) + ":" + en_quote(value)
            elif "!=" in _and:
                output += en_quote(key) + ":" + "{'$ne':" + en_quote(value) + "}"
            else: return {}    
            output += ","

        output += "},"
        
    output += "]}"
    return ast.literal_eval(output)
