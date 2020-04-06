import re
import ast

def enc_quotes(text):
    return "'" + text + "'"

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
                output += enc_quotes(key) + ":" + enc_quotes(value)
            elif "!=" in _and:
                output += enc_quotes(key) + ":" + "{'$ne':" + enc_quotes(value) + "}"
            else: return {}    
            output += ","

        output += "},"
        
    output += "]}"
    return ast.literal_eval(output)
