import re
import ast
import json
def query_parser(query):
    parts = query.split(' or ')
    #print(parts)
    output = "{ '$or': ["

    for part in parts:
        #print(json.dumps(part))
        ands = part.replace(' and ', ',')
        i=""
        t=ands.split(',')
        for j in range(0,len(t)):
            temp=t[j].split('==')
            temp=json.dumps(temp[0])+":"+json.dumps(temp[1])
            t[j]=temp
        ands=",".join(t)

        output += "{"
        
        output += ands
        output += "},"
        

    output += "]}"
    print(output)
    return ast.literal_eval(output)
