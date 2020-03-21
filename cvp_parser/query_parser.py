import re
import ast

def query_parser(query):
    parts = query.split(' or ')
    output = "{ '$or': ["

    for part in parts:
        ands = part.split(' and ')
        output += "{"
        for _and in ands:
            ops = re.split(r'(?:==|!=)', _and)
            try:
                key, value = ops[0].strip(), ops[1].strip()
            except IndexError:
                return {}
            if "==" in _and:
                output += key + ":" + value
            elif "!=" in _and:
                output += key + ":" + "{'$ne':" + value + "}"
            else: return {}    
            output += ","

        output += "},"
        
    output += "]}"
    return ast.literal_eval(output)
