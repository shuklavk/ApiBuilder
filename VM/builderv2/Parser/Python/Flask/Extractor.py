from builderv2.Templates.Python.Flask import *
import re

# Current formatting for tokens in <token_name>

def extractTokensFromTemplates(template):
    matches = re.findall(r"<+(\w+)+>", template)
    return set(matches)


if __name__ == "__main__":
    #print extractTokensFromTemplates(HEADING)
    #print extractTokensFromTemplates(CRUD_POST_READ)
    #print extractTokensFromTemplates(RUN_CODE)
    print extractTokensFromTemplates(OBJECT_CLASS_CODE)
    print extractTokensFromTemplates(CRUD_POST_DELETE)