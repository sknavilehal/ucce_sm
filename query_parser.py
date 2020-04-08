import re
import ast

def query_parser(query):
    parts = query.split(' or ')
    output = {"$or": []}

    for part in parts:
        ands = part.split(' and ')
        field = {}
        for _and in ands:
            ops = re.split(r'(?:==|!=)', _and)
            try:
                key, value = ops[0].strip(), ops[1].strip()
                idx = key.find('.')+1
                key = key[idx:]
            except IndexError:
                return {}
            if "==" in _and:
                field[key] = value
            elif "!=" in _and:
                field[key] = {"$ne": value}
            else: return {}    

        output["$or"].append(field)
        
    return output
