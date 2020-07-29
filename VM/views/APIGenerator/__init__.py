from flask import Blueprint, jsonify, request, send_from_directory
from server.Kit import *
from server.User.UserDB import retrieveUser, isValidUser
from server.RouteGroup.RouteGroupDB import getUserRoutes
from server.APIGroup.APIGroupDB import APIGroup, addAPI, getUserAPIs, updateAPI, getCurrentAPI
from server.ObjectAttributes.ObjectAttributesDB import retrieveObjectAttributes
from builderv2.Parser.Python.Flask.Builder import Builder, RoutePage, ObjectPage, RunnerPage, DatabaseRoot, KitPage, \
    ConfigPage, JSLibraryPage, PackageJSONPage, NodeDatabaseRoot, NodeObjectPage, NodeRunnerPage, NodeConfigPage, NodeRoutePage, \
    NodeKitPage, RequirementsPage, JinjaPage
from deployer.FlaskDeployer import FlaskDeployer
from random import randint
from onAppRunConfig import SERVER_ROOT, CLIENT_ZIP
import uuid
from onAppRunConfig.logConfig import routeRequestLogger, generalLogger
import socket

apiGenerator = Blueprint('apiGenerator', __name__)

"""Deploy at given source location."""
def deploy(source_location):
    fd = FlaskDeployer(source_location)
    return fd.deploy()


"""Return a random port number between 1000 and 5000."""
def retrieveUserPortNumber():
    return randint(1000, 5000)

"""Sends zip file to the user as an attachment"""
@apiGenerator.route('/get-compress/<path:path>')
def get_zip(path):
    try:
        data = request.get_json()

        routeRequestLogger.info(request=request)

        return send_from_directory(CLIENT_ZIP, filename=path, as_attachment=True)
    except:
        routeRequestLogger.exception(request)

        return jsonify(**{'message': 'File Not Found'}), ErrorCode_NotFound


@apiGenerator.route('/setAPIName', methods=['POST'])
def setAPIName():
    try:
        data = request.get_json()

        routeRequestLogger.info(request)

        if not checkParam(data, 'userId') or \
            not isValidUser(int(data['userId'])):
            return jsonify(**{'message': 'Bad params'}), ErrorCode_BadParams

        #adds APIname to API table
        user = retrieveUser(data['userId'])

        newAPIGroup = APIGroup(data['userId'],
                            data["apiName"],)

        if not getUserAPIs(data['userId']):
            addAPI(user.id, newAPIGroup)
        else:
            updateAPI(user.id, newAPIGroup)

        if not checkParam(data, 'userId') or \
            not isValidUser(int(data['userId'])):

            generalLogger.error(logTemplate.generalLogTemplate("userID is not given or userID is invalid at " + request.path))
            return jsonify(**{'message': 'Bad params'}), ErrorCode_BadParams
        
        generalLogger.info("user successfully verified in " + request.path)

        #adds APIname to API table
        user = retrieveUser(data['userId'])

        newAPIGroup = APIGroup(data['userId'],
                            data["apiName"],)

        if not getUserAPIs(data['userId']):
            addAPI(user.id, newAPIGroup)
        else:
            updateAPI(user.id, newAPIGroup)

        return jsonify(**{'api_name': data['apiName']})
    except:
        routeRequestLogger.exception(request)
        return jsonify(**{"message": "Unexpected Error"}), ErrorCode_ServerError

@apiGenerator.route('/getAPIName', methods=['POST'])
def getAPIName():
    try:
        data = request.get_json()

        routeRequestLogger.info(request)

        if not checkParam(data, 'userId') or \
            not isValidUser(int(data['userId'])):
            return jsonify(**{'message': 'Bad params'}), ErrorCode_BadParams

        user = retrieveUser(data['userId'])
        try:
            currentAPI = getCurrentAPI(user.id)
        except Exception as e: print e

        if currentAPI == None:
            return jsonify(**{'api_name': ""})
        return jsonify(**{'api_name': currentAPI.name})
    except:
        routeRequestLogger.exception(request)
        return jsonify(**{"message": "Unexpected Error"}), ErrorCode_ServerError

"""Generates API using all the Route Groups created

Request data provides: userId, objectId
+API name gets set
For each RouteGroup object, we create a tokens object which is used to create
the Object and Route Page
    Object Page = Defines model to database and creates functions to aide CRUD
                    operations to the database (ex. adding/querying users)
                    - located in database/{nameOfRouteGroup}
    Route Page  = Page with CRUD operations for the RouteGroup
                    - located in server/{nameOfRouteGroup}
For the overall API, the runner file, db_root, and Kit are created
    runner = file that runs the server (run.py)
    db_root = initializes the DB (database/__init__.py)
    Kit = general functions and variables (server/Kit/__init__.py)
All pages are stored in a pages array and ran through a Builder
Finally, files are deployed
"""
@apiGenerator.route('/generateFullAPI', methods=['POST'])
def generateFullAPI():
    try:
        data = request.get_json()

        routeRequestLogger.info(request)

        if not checkParam(data, 'userId') or \
                not checkParam(data, 'output') or \
                    not isValidUser(int(data['userId'])):
            return jsonify(**{'message': 'Bad params'}), ErrorCode_BadParams

        user_objects = getUserRoutes(int(data['userId']))
        outputType = data['output']
        pages = []

        #second check if objectId is stored but there are no user routegroups
        if not len(user_objects):
            return jsonify(), ErrorCode_BadParams

        if not getCurrentAPI(data['userId']) or not getCurrentAPI(data['userId']).name:
            api_name = "Release_" + str(randint(0, 1000000))
        else:
            api_name = "Release_" + getCurrentAPI(data['userId']).name + "_" + str(randint(0, 1000000))

        drop_root = ''
        app_uuid = uuid.uuid4()

        api_port_number = retrieveUserPortNumber()

        try:
            host_ip = socket.gethostbyname(socket.gethostname()+".local")
        except:
            host_ip = socket.gethostbyname(socket.gethostname())

        swaggerTokens = {
            'port_number': str(api_port_number),
            'drop_root': drop_root,
            'api_name': api_name,
            'all_class_names_list': [obj.objectName for obj in user_objects],
            'server_root': SERVER_ROOT,
            'app_uuid': str(app_uuid),
            'all_class_details': [],
            'enumerate': enumerate,
            'len': len,
            'host_ip': host_ip
        }
        for obj in user_objects:
            object_attrs = retrieveObjectAttributes(
                int(data['userId']), int(obj.id))
            object_params = ','.join([o.name for o in object_attrs])

            swaggerTokens["all_class_details"].append({
                'attr_name_and_types': [{"name":o.name, "type":o.type} for o in object_attrs],
                'column_primary_key_list': [True if o.name == "id" else False for o in object_attrs],
                'column_nullable_list': [o.isNullable for o in object_attrs],
                'column_unique_list': [o.isUnique for o in object_attrs],

                'api_name': api_name,  # TODO: make this user editable
                'drop_root': drop_root,
                'class_name': obj.objectName,
                'imports': '',
                # TODO: make this something that comes from the user profile / does a great job
                'port_number': str(api_port_number),
                # of limiting user to only one api per account too',
                'server_root': SERVER_ROOT,
                'supported_methods': '\'POST\''
            })

            tokens = {
                'object_params': object_params,
                'column_types': [o.type for o in object_attrs],
                'column_primary_key_list': [True if o.name == "id" else False for o in object_attrs],
                'column_nullable_list': [o.isNullable for o in object_attrs],
                'column_unique_list': [o.isUnique for o in object_attrs],

                'api_name': api_name,  # TODO: make this user editable
                'drop_root': drop_root,
                'class_name': obj.objectName,
                'imports': '',
                # TODO: make this something that comes from the user profile / does a great job
                'port_number': str(api_port_number),
                # of limiting user to only one api per account too',
                'server_root': SERVER_ROOT,
                'supported_methods': '\'POST\'',
                'app_uuid': str(app_uuid)
            }
            if outputType == 'node':
                pages += [NodeObjectPage(tokens, obj.objectName), NodeRoutePage(tokens, obj.objectName), JSLibraryPage(tokens, obj.objectName)]
            elif outputType == 'flask':
                pages += [ObjectPage(tokens, obj.objectName), RoutePage(tokens, obj.objectName), JSLibraryPage(tokens, obj.objectName)]
            

        # All add the runner page and included kit
        tokens = {
            'port_number': str(api_port_number),
            'drop_root': drop_root,
            'api_name': api_name,
            'all_class_names_list': [obj.objectName for obj in user_objects],
            'server_root': SERVER_ROOT,
            'app_uuid': str(app_uuid),

        }
        # The runner class is responsible for actually running the server. The deployer explicity uses this created file
        if outputType == 'node':
            runner = NodeRunnerPage(tokens)
            db_root = NodeDatabaseRoot(tokens)
            kit = NodeKitPage()
            config = NodeConfigPage(tokens)
            packageJSON = PackageJSONPage()
            pages += [packageJSON]
        elif outputType == 'flask':
            runner = RunnerPage(tokens)
            db_root = DatabaseRoot(tokens)
            kit = KitPage()
            requirements = RequirementsPage()
            config = ConfigPage(tokens)
            # swaggerJSON = JinjaPage(swaggerTokens, "swagger.j2", "swagger", ".json")
            pages += [requirements]
            # pages += [requirements, swaggerJSON]

        pages += [runner, kit,db_root, config]

        builder = Builder(pages, api_name)
        loc = builder.dropFiles()

        print "Running user server on port:", api_port_number

        return jsonify(**{'port_number': api_port_number,
                        'api_name': api_name,
                        'app_uuid': str(app_uuid)})
    except Exception as e:
        routeRequestLogger.exception(request)
        return jsonify(**{"message": "Unexpected Error"}), ErrorCode_ServerError
