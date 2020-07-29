from builderv2.Parser.Python.Flask.Extractor import extractTokensFromTemplates
from builderv2.Templates.Python.Flask import *

def insertTokensIntoTemplate(template, **kwargs):
    neededTokenValues = extractTokensFromTemplates(template)

    for key,value in kwargs.items():
        if key in neededTokenValues:
            neededTokenValues.remove(key)
            template = template.replace("<" + key + ">", value)

    if len(neededTokenValues) > 0:
        raise ValueError

    return template



if __name__ == "__main__":
    print insertTokensIntoTemplate(HEADING, **{'object_name':'TestObject'})
    print insertTokensIntoTemplate(RUN_CODE, **{'port_number': '127.0.0.1'})
    print insertTokensIntoTemplate(CRUD_POST_READ, **{'supported_methods':'"POST"',
                                                 'object_name':'TestObject',
                                                 'route_name':'readTestObject',
                                                 'object_id':'1'})
