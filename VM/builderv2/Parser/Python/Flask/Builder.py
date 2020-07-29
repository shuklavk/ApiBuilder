from builderv2.Parser.Python.Flask.Extractor import extractTokensFromTemplates
from builderv2.Parser.Python.Flask.Insertor import insertTokensIntoTemplate
from builderv2.Templates.Python.Flask import *
from zipfile import ZipFile
import shutil
import os
import json
from random import randint
from onAppRunConfig.logConfig import generalLogger
from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader('builderv2.Templates.Python.Flask', 'templates')
)

class Page(object):

    types_to_column = {
        # old map
        'int': 'Integer',
        'dec': 'Float',
        'string': 'String',
        'bool': 'Boolean',
        'datetime': 'DateTime',

        # new map
        'number': 'Integer',
        'decimal': 'Float',
        'word(s)': 'String',
        'true / false': 'Boolean',
        'date and time': 'DateTime'
    }

    ABTypes_to_jsonTypes = {
        'number': 'integer',
        'decimal': 'number',
        'word(s)': 'string',
        'true / false': 'boolean',
        'date and time': 'string'
    }
    
    python_to_js = {
        'Integer': 'number',
        'Float': 'number',
        'String': 'string',
        'Boolean': 'boolean',
        'DateTime': 'Date'
    }
    python_to_sequelize = {
        'Integer': 'INTEGER',
        'Float': 'FLOAT',
        'String': 'STRING',
        'Boolean': 'BOOLEAN',
        'DateTime': 'DATE'
    }
    def __init__(self, templates, token_dict, name):
        # You must send in the arguments to templates in
        # the order that you'd like for it to show on the page
        self.templates = templates
        self.token_dict = self.genTokens(token_dict)
        self.name = name


    def createPage(self):
        full_page = ""
        for template in self.templates:
            if self.token_dict:
                full_page += insertTokensIntoTemplate(template, **self.token_dict) + '\n'
            else:
                # We currently assume you just want the plain template. This design may change in the future
                full_page += insertTokensIntoTemplate(template)

        return full_page

    def extractPageTokens(self):
        tokens = set()
        for template in self.templates:
            [tokens.add(t) for t in extractTokensFromTemplates(template)]
        return tokens

    # This function gives you some tokens for free
    def genTokens(self, tokens):
        if not tokens:
            return
        if 'class_name' in tokens:
            tokens['object_name'] = 'obj_' + tokens['class_name']

        if 'all_class_names_list' in tokens:
            tokens['all_class_names'] = ', '.join(tokens['all_class_names_list'])
            tokens['blueprint_registrations'] = ''.join([BLUEPRINT_REGISTER.replace('<class_name>', c) for c in tokens['all_class_names_list']])
            tokens['class_blueprint_imports'] = ''.join([CLASS_BLUEPRINT_IMPORT.replace('<class_name>', c) for c in tokens['all_class_names_list']])
            tokens['node_class_blueprint_imports'] = ''.join([NODE_IMPORT_ROUTE.replace('<class_name>', c) for c in tokens['all_class_names_list']])

            if 'drop_root' in tokens and 'api_name' in tokens:
                tokens['db_imports'] = ''.join([DB_IMPORT.replace('<class_name>', c).
                                                          replace('<drop_root>',tokens['drop_root']).
                                                          replace('<api_name>', tokens['api_name'])
                                                          for c in tokens['all_class_names_list']])
        if not 'rand' in tokens:
            tokens['rand'] = str(randint(1,1000000))
        tokens['app_token_check'] = APP_TOKEN_CHECK

        if "all_class_details" in tokens:
            for class_details in tokens["all_class_details"]:
                for attr_name_and_type in class_details["attr_name_and_types"]:
                    attr_name_and_type["type"] = {
                        "AB": attr_name_and_type["type"],
                        "json": self.ABTypes_to_jsonTypes[attr_name_and_type["type"]]
                    }

        if 'object_params' in tokens and 'column_types' in tokens and \
            'column_primary_key_list' in tokens and 'column_nullable_list' in tokens and \
            'column_unique_list' in tokens:
            yieldParams = ""
            classFieldDeclerations = ""
            nodeClassFieldDeclarations = ""
            classFieldAssigns = ""
            kwordParamSet = ""
            objectParamsAsString = ""
            dataDictParams = ""
            req_attr_and_types = {}

            params = [p.strip() for p in tokens['object_params'].split(',')] #TODO: change to list
            param_types = [self.types_to_column[t] for t in tokens['column_types']]
            param_primary_key_bools = tokens['column_primary_key_list']
            param_nullable_key_bools = tokens['column_nullable_list']
            param_unique_key_bools = tokens['column_unique_list']

            # Someone sent in a malformed list for one or both of these
            if len(params) != len(param_types) or len(params) != len(param_primary_key_bools) or \
                    len(params) != len(param_nullable_key_bools) or len(params) != len(param_unique_key_bools):
                raise IndexError

            for param, param_type, is_primary, is_nullable, is_unique in zip(params, param_types, param_primary_key_bools, param_nullable_key_bools, param_unique_key_bools):
                yieldParams += YIELD_PARAM.replace('<param_name>', param)
                classFieldAssigns += CLASS_DB_FIELD_ASSIGNMENT.replace('<param_name>', param)
                kwordParamSet += KWORD_PARAM_SET.replace('<param_name>', param)
                objectParamsAsString += " '" + param + "'," #TODO this needs to be join
                dataDictParams += DATA_DICT_PARAM.replace('<param_name>', param)
                classFieldDeclerations += CLASS_DB_FIELD_DECLARATION.replace('<param_name>', param).\
                    replace('<column_type>', param_type).\
                    replace('<primary_key_bool>', str(is_primary).capitalize()).\
                    replace('<nullable_key_bool>', str(is_nullable).capitalize()).\
                    replace('<unique_key_bool>', str(is_unique).capitalize())
                if not param == 'id':
                    nodeClassFieldDeclarations += NODE_CLASS_DB_FIELD_DECLARATION.replace('<param_name>', param).\
                        replace('<nullable_key_bool>', str(is_nullable).lower()).\
                        replace('<sequelize_type>', self.python_to_sequelize[param_type])

                # Python to JS Library Param
                req_attr_and_types[param] = self.python_to_js[param_type]

            tokens['yield_params'] = yieldParams
            tokens['class_db_field_declerations'] = classFieldDeclerations
            tokens['node_class_db_field_declerations'] = nodeClassFieldDeclarations
            tokens['class_db_field_assignments'] = classFieldAssigns
            tokens['kword_param_set_group'] = kwordParamSet
            tokens['object_params_as_strings'] = objectParamsAsString
            tokens['data_dict_params'] = dataDictParams
            tokens['column_type_list'] = ", ".join(set(param_types))
            tokens['req_attr_and_types'] = json.dumps(req_attr_and_types)

        return tokens

class JinjaPage(Page):
    def __init__(self, token_dict, template, name, ext):
        super(JinjaPage, self).__init__(template, token_dict, name)
        self.ext = ext
    
    def createPage(self):
        template = env.get_template(self.templates)
        return template.render(self.token_dict)

class ObjectPage(Page):

    def __init__(self, token_dict, name):
        super(ObjectPage, self).__init__([OBJECT_CLASS_CODE], token_dict, name)

class NodeObjectPage(Page):
    def __init__(self, token_dict, name):
        super(NodeObjectPage, self).__init__([NODE_OBJECT_CLASS_CODE], token_dict, name)

class RoutePage(Page):
    def __init__(self, token_dict, name):
        super(RoutePage, self).__init__([HEADING,
                                         CRUD_POST_CREATE,
                                         CRUD_POST_READ,
                                         CRUD_POST_UPDATE,
                                         CRUD_POST_DELETE,
                                         RUN_CODE],
                                         token_dict,
                                         name)

class NodeRoutePage(Page):
    def __init__(self, token_dict, name):
        super(NodeRoutePage, self).__init__([NODE_HEADING, 
                                            NODE_CRUD_POST_CREATE, 
                                            NODE_CRUD_POST_READ, 
                                            NODE_CRUD_POST_UPDATE, 
                                            NODE_CRUD_POST_DELETE, 
                                            NODE_ROUTE_PAGE_ENDING],
                                         token_dict,
                                         name)

class RunnerPage(Page):
    def __init__(self, token_dict):
        super(RunnerPage, self).__init__([RUNNER_PAGE], token_dict, 'run')

class NodeRunnerPage(Page):
    def __init__(self, token_dict):
        super(NodeRunnerPage, self).__init__([NODE_RUNNER_PAGE], token_dict, 'index.js')

class DatabaseRoot(Page):
    def __init__(self, token_dict):
        super(DatabaseRoot, self).__init__([DATABASE_PAGE], token_dict, '__init__.py')

class NodeDatabaseRoot(Page):
    def __init__(self, token_dict):
        super(NodeDatabaseRoot, self).__init__([NODE_DATABASE_PAGE], token_dict, 'database.js')

class KitPage(Page):
    def __init__(self):
        super(KitPage, self).__init__([KIT_PAGE], None, '__init__.py')

class NodeKitPage(Page):
    def __init__(self):
        super(NodeKitPage, self).__init__([NODE_KIT_PAGE], None, 'Kit.js')
class RequirementsPage(Page):
    def __init__(self):
        super(RequirementsPage, self).__init__([REQUIREMENTS_PAGE], None, 'requirements.txt')

class JSLibraryPage(Page):
    def __init__(self, token_dict, name):
        super(JSLibraryPage, self).__init__([CLASS_BEGIN, REQUIRED_ATTR_AND_TYPES, JS_CLASS_CREATE_FUNCTION, JS_CLASS_READ_FUNCTION, JS_CLASS_UPDATE_FUNCTION, JS_CLASS_DELETE_FUNCTION, CLASS_END], token_dict, name)

class PackageJSONPage(Page):
    def __init__(self):
        super(PackageJSONPage, self).__init__([PACKAGE_JSON], None, 'package.json')

class ConfigPage(Page):
    def __init__(self, token_dict):
        super(ConfigPage, self).__init__([CONFIG_PAGE], token_dict, 'config')

class NodeConfigPage(Page):
    def __init__(self, token_dict):
        super(NodeConfigPage, self).__init__([NODE_CONFIG_PAGE], token_dict, 'config')

class Builder:

    def __init__(self, pages, outputName=None):
        # This will be a list of pages you would like to fill
        self.pages = pages
        self.outputName = "Test" if (outputName is None) else outputName
        #self.drop_location = "../../../../drop/" + self.outputName
        self.drop_location = "drop/" + self.outputName # When accessing from the server do like this #SERVERCODE

    def extractAllPageTokens(self):
        tokens = set()
        for page in self.pages:
            [tokens.add(t) for t in page.extractPageTokens()]
        return tokens

    def insertTokenValues(self):
        return [filledPage.createPage() for filledPage in self.pages]

    def createDropFolder(self):
        self.createFolder(self.drop_location, "")

    def createFolder(self, folderLoc, folderName):
        try:
            os.makedirs(folderLoc + folderName)
        except OSError:
            pass

    def outputFile(self, payload, location, filename, extension='.py'):
        file_page = open(location + '/' + filename + extension, 'w')
        file_page.write(payload)
        file_page.close()

    def outputFileJoin(self, payload, locAndFile):
        file_page = open(locAndFile, 'w')
        file_page.write(payload)
        file_page.close()

    def setUpDropFolderStructure(self):
        self.createDropFolder()

        #with open("../../../Templates/Python/Flask/FileStructureTemplate") as structure_template:
        with open("builderv2/Templates/Python/Flask/FileStructureTemplate") as structure_template: # SERVERCODE
            lines = structure_template.readlines()
            level3,level2, level1 = (None, None, None)
            for i,line in enumerate(lines):
                # There's a space here, so let's count how deep in the hierarchy to place this
                # CURRENTLY ONLY SUPPORT 3 levels

                # 3 levels
                '''
                if line[0:12].count(' ') is 12:
                    if level3 is None:
                        level3 = lines[i-1].strip()
                    if i > 2:
                        line = level3 + '/' + level2 + '/' + level1 + '/' + line.strip()
                '''

                # 2 levels
                if line[0:8].count(' ') is 8:
                    level3 = line.strip()

                    if i > 1:
                        line = level1 + '/' + level2 + '/' + line.strip()

                # 1 level
                elif line[0:4].count(' ') is 4:
                    if level3 is not None:
                        level3 = None

                    level2 = line.strip()

                    if i > 0:
                        line = level1 + '/' + line.strip()
                else:
                    level1 = line.strip()

                # Does the lines have a file extension? Create a file instead of folder
                if len(line.split('.')) == 2:
                    self.outputFileJoin("", self.drop_location + '/' + line.strip())
                else:
                    self.createFolder(self.drop_location + '/' + line.strip(), "")

    def outputZipFile(self):
        shutil.make_archive('zipRelease/' + self.outputName, 'zip', self.drop_location)

    # The monster method that returns the final payload
    def dropFiles(self):
        self.setUpDropFolderStructure()


        filledPages = self.insertTokenValues()
        for i, pageString in enumerate(filledPages):
            if 'NodeObjectPage' in str(type(self.pages[i])):
                self.createFolder(self.drop_location + '/database/', self.pages[i].name)
                self.outputFile(pageString, self.drop_location + '/database/' + self.pages[i].name, self.pages[i].name, '.js')
            
            elif 'NodeRunnerPage' in str(type(self.pages[i])):
                self.outputFile(pageString, self.drop_location, 'index', '.js')
            
            elif 'ObjectPage' in str(type(self.pages[i])):
                self.createFolder(self.drop_location + '/database/', self.pages[i].name)
                self.outputFile(pageString, self.drop_location + '/database/' + self.pages[i].name, '__init__')

            elif 'NodeRoutePage' in str(type(self.pages[i])):
                self.createFolder(self.drop_location + '/server/', self.pages[i].name)
                self.outputFile(pageString, self.drop_location + '/server/' + self.pages[i].name, self.pages[i].name, '.js')
            elif 'RoutePage' in str(type(self.pages[i])):
                self.createFolder(self.drop_location + '/server/', self.pages[i].name)
                self.outputFile(pageString, self.drop_location + '/server/' + self.pages[i].name, '__init__')
            elif 'NodeDatabaseRoot' in str(type(self.pages[i])):
                self.outputFile(pageString, self.drop_location + '/database', 'database', '.js')

            elif 'DatabaseRoot' in str(type(self.pages[i])):
                self.outputFile(pageString, self.drop_location + '/database', '__init__')

            elif 'NodeKitPage' in str(type(self.pages[i])):
                self.outputFile(pageString, self.drop_location + '/server/Kit', 'Kit', '.js')

            elif 'KitPage' in str(type(self.pages[i])):
                self.outputFile(pageString, self.drop_location + '/server/Kit', '__init__')

            elif 'RequirementsPage' in str(type(self.pages[i])):
                self.outputFile(pageString, self.drop_location, 'requirements', '.txt')

            elif 'JSLibraryPage' in str(type(self.pages[i])):
                self.outputFile(pageString, self.drop_location + '/static/scripts/library', self.pages[i].name, '.js')
            elif 'NodeConfigPage' in str(type(self.pages[i])):
                self.outputFile(pageString, self.drop_location, 'config', '.js')
            elif 'ConfigPage' in str(type(self.pages[i])):
                self.outputFile(pageString, self.drop_location, 'config')
            elif 'PackageJSONPage' in str(type(self.pages[i])):
                self.outputFile(pageString, self.drop_location, 'package', '.json')

            elif 'JinjaPage' in str(type(self.pages[i])):
                source = os.path.abspath(os.path.join(__file__, "../../../../Templates/Python/Flask/swaggerBlueprint"))
                dest = self.drop_location + '/server/swagger'
                shutil.copytree(source, dest)
                self.outputFile(pageString, self.drop_location + '/server/swagger/static', self.pages[i].name, self.pages[i].ext)

            else:
                self.outputFile(pageString, self.drop_location, self.pages[i].name )

        self.outputZipFile() 

        generalLogger.info("generated code has been dropped into /Releases folder")

        return self.drop_location + '/' + self.outputName + '.zip'


if __name__ == "__main__":
    #p1 = Page(["test"], None, )
    #b1 = Builder(None)
    #b1.outputFile("test", Builder.drop_location, "test")

    api_name = "TestAPI"

    o1_dict = {
        'api_name'                  :   api_name,
        'drop_root'                 :   'drop.',
        'class_name'                :   'Attribute',
        'imports'                   :   '',
        'object_params'             :   'id, name, description, isUnique, isEncrypted, isNullable, creation_datetime',
        'port_number'               :   '12345',
        'server_root'               :   '127.0.0.1', # 0.0.0.0 on server
        'supported_methods'         :   '\'POST\'',
        'column_types'              :   ['int', 'dec', 'string', 'bool', 'bool', 'bool', 'datetime'],
        'column_primary_key_list'   :   [True, False, False, False, False, False, False],
        'column_nullable_list'      :   [False, True, False, False, False, True, False],
        'column_unique_list'        :   [True, False, False, False, False, False, False],
    }

    user_dict = {
        'api_name'                  :   api_name,
        'drop_root'                 :   'drop.',
        'class_name'                :   'User',
        'imports'                   :   '',
        'object_params'             :   'id, name, email, password, creation_datetime',
        'port_number'               :   '12345',
        'server_root'               :   '127.0.0.1',
        'supported_methods'         :   '\'POST\'',
        'column_types'              :   ['int', 'string', 'string', 'string', 'datetime'],
        'column_primary_key_list'   :   [True, False, False, False, False],
        'column_nullable_list'      :   [False, False, False, False, True],
        'column_unique_list'        :   [True, False, True, False, False],
    }

    runner_dict = {
        'port_number'               : '12345',
        'drop_root'                 : 'drop.',
        'api_name'                  : api_name,
        'all_class_names_list'      : ['Attribute', 'User'],
        'server_root'               : '127.0.0.1',
    }

    o1 = ObjectPage(o1_dict, "Attribute")
    r1 = RoutePage(o1_dict, "Attribute")
    userObject = ObjectPage(user_dict, 'User')
    userRoute = RoutePage(user_dict, 'User')


    runner = RunnerPage(runner_dict)
    db_root = DatabaseRoot(runner_dict)
    print db_root.extractPageTokens()

    b3 = Builder([o1, r1, userObject, userRoute, runner, db_root], api_name)
    #print b3.extractAllPageTokens()
    b3.dropFiles()
