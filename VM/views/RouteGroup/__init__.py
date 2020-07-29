from flask import Blueprint, jsonify, request
from server.Kit import *
from server.User.UserDB import retrieveUser, isValidUser, gimmeNewUser
from server.RouteGroup.RouteGroupDB import RouteGroup, addRoute, getRoute, getUserRoutes, deleteRoute, updateRoute
from server.ObjectAttributes.ObjectAttributesDB import retrieveObjectAttributes

from onAppRunConfig.logConfig import routeRequestLogger, generalLogger

routeGroup = Blueprint('routeGroup', __name__)


"""Create a new Route Group Object

Request data provides: userId, objectName, isCrud, isReadMultiple,
                        isReadAllObjects, isSingleRoute
Uses this data to create a RouteGroup Object
Finally, links the created RouteGroup with the user's id in the database
Returns a JSON object with the created RouteGroup's id and a status code of ErrorCode_Success
"""
@routeGroup.route("/addNewRouteGroup", methods=['POST'])
def addNewRouteGroup():
    try:
        data = request.get_json()

        routeRequestLogger.info(request)

        if not checkParams(data, *RouteGroup.params):
            generalLogger.error("data sent to " + request.path + " does not have correct params. Expected " + RouteGroup.params + " but received " + data)

            return jsonify(**{"message": "Bad params"}), ErrorCode_BadParams

        if data['objectName'] == '':
            generalLogger.error("route group name is empty. cannot be empty")
            return jsonify(**{"message": "Bad params"}), ErrorCode_BadParams
        
        user = retrieveUser(data['userId'])

        newRouteGroup = RouteGroup(data['userId'],
                                data["objectName"],
                                data["apiId"],
                                data["isCRUD"],
                                data['isReadMultiple'],
                                data['isReadAllObjects'],
                                data['isSingleRoute'])

        addRoute(user.id, newRouteGroup)
        return jsonify(**{"objectId": newRouteGroup.id}), ErrorCode_Success
    except:
        routeRequestLogger.exception(request)
        return jsonify(**{"message": "Unexpected Error"}), ErrorCode_ServerError


"""
Gets all the Routes associated with a RouteGroup object

Request data provides: userId, objectId
Uses this data to get a specific RouteGroup object
Gets all routes associated with the RouteGroup
Returns array of all the routes and a status code of ErrorCode_Success
"""
@routeGroup.route("/showObjectRoutes", methods=['POST'])
def showObjectRoutes():
    try:
        data = request.get_json()
        
        routeObject = getRoute(data['userId'], {'id':data['objectId']})
        if not routeObject:
            return jsonify(**{'message': 'List of Objects not found'}), ErrorCode_NotFound
        
        routeRequestLogger.info(request)

        if not checkParam(data, 'userId') or \
                not checkParam(data, 'objectId'):
            return jsonify(**{'message': 'Bad params'}), ErrorCode_BadParams

        routeObject = getRoute(data['userId'], {'id':data['objectId']})
        if not routeObject:
            return jsonify(**{'message': 'Object not found'}), ErrorCode_NotFound

        # stupid route creation code
        customRoutes = []
        for protocol in ['/create', '/read', '/update', '/delete']:
            customRoutes += [protocol + routeObject.objectName]

        # Now send the routes made by the builder
        return jsonify(**{'routes': customRoutes}), ErrorCode_Success
    except:
        routeRequestLogger.exception(request)
        return jsonify(**{"message": "Unexpected Error"}), ErrorCode_ServerError

"""
Gets all RouteGroups objects associated with the user

Request data provides: userId
If no user is found, creates a new user
Uses userId to access a specific user from the database
Returns an array of all RouteGroups associated with the user and a status code of ErrorCode_Success 
"""
@routeGroup.route("/viewAvailableRouteGroups", methods=['POST'])
def viewAvailableRouteGroups():
    try:
        data = request.get_json()

        routeRequestLogger.info(request)

        if data is None:
            return jsonify(**{}), ErrorCode_ServerError

        if not checkParam(data, 'userId'): 
            user = gimmeNewUser()
        else:
            user = retrieveUser(data['userId'])
        
        if not isValidUser(user.id):
            return jsonify(**{'message': 'Bad Params'}), ErrorCode_BadParams

        # routes = [{"id":route.id, "objectName" : route.objectName, "apiId": route.apiId} for route in getUserRoutes(user.id)]
        routes = []
        for route in getUserRoutes(user.id):
            attributes = retrieveObjectAttributes(data['userId'], route.id)
            new_list = {}
            for attr in attributes:
                new_list[attr.id] = dict(attr) 
            routes.append({"id":route.id, "objectName" : route.objectName, "apiId": route.apiId, "attributes": new_list}) 

        return jsonify(**{"groups": routes}), ErrorCode_Success
    except:
        routeRequestLogger.exception(request)
        return jsonify(**{"message": "Unexpected Error"}), ErrorCode_ServerError


'''
Deletes the RouteGroup associated with the objectId

Request data provides: userId, objectId
If no data is found, a serverError is sent
If no userId/objectId is found, a badParams error is sent
Uses userId to access a specifi user from the database, and validates the user
Deletes the RouteGroup and returns {} with a status code of ErrorCode_Success 
'''
@routeGroup.route("/deleteRouteGroup", methods=['POST'])
def deleteRouteGroup():
    try:
        data = request.get_json()

        routeRequestLogger.info(request)

        if data is None:
            return jsonify(**{'message': 'No data found'}), ErrorCode_ServerError
        
        if not checkParam(data, 'userId') or not checkParam(data, 'objectId'):
            return jsonify(**{'message': 'Bad params'}), ErrorCode_BadParams
        
        user = retrieveUser(data['userId'])
        if user is None:
            return jsonify(**{'message': 'No data found'}), ErrorCode_ServerError
        if not isValidUser(user.id):
            return jsonify(**{'message': 'Bad Params'}), ErrorCode_BadParams

        deleteRoute(user.id, data['objectId'])
    
        return jsonify(**{}), ErrorCode_Success
    except:
        routeRequestLogger.exception(request)
        return jsonify(**{"message": "Unexpected Error"}), ErrorCode_ServerError


'''
Updates the attributes associated with the RouteGroup

Request data provides: objectId, updatedRouteGroup (dictionary of RouteGroup attributes)
If no data is found, a serverError is sent
If no userId/updatedRouteGroup is found, a badParams error is sent
Uses userId to access a specifi user from the database, and validates the user
Updates RouteGroup and returns RouteGroup id if successful
On failure, returns an error message
'''
@routeGroup.route("/updateRouteGroup", methods=['POST'])
def updateRouteGroup():
    try:
        data = request.get_json()

        routeRequestLogger.info(request)

        if data is None:
            return jsonify(**{'message': 'No data found'}), ErrorCode_ServerError
        
        if not checkParam(data, 'objectId') or not checkParams(data['updatedRouteGroup'], *RouteGroup.params):
            return jsonify(**{'message': 'Bad params'}), ErrorCode_BadParams
        
        user = retrieveUser(data['updatedRouteGroup']['userId'])
        if user is None:
            return jsonify(**{'message': 'No data found'}), ErrorCode_ServerError
        if not isValidUser(user.id):
            return jsonify(**{'message': 'Bad Params'}), ErrorCode_BadParams 
        
        if updateRoute(user.id, data['objectId'], data['updatedRouteGroup']):
            return jsonify(**{'objectId': data['objectId']}), ErrorCode_Success
        
        return jsonify(**{'message': 'Update failed'}), ErrorCode_ServerError
    except:
        routeRequestLogger.exception(request)
        return jsonify(**{"message": "Unexpected Error"}), ErrorCode_ServerError


'''
Returns the JSON object of the RouteGroup associated with the given objectId and userId

Request data provides: userId, objectId
If no data is found, a serverError is sent
If no userId/objectId is found, a badParams error is sent
RouteGroup is retrieved, and the object is packaged in a dictionary, routeObject
Return routeObject 
'''
@routeGroup.route("/getRouteGroup", methods=['POST'])
def getRouteGroup():
    try:
        data = request.get_json()

        routeRequestLogger.info(request)

        if data is None:
            return jsonify(**{'message': 'No data found'}), ErrorCode_ServerError

        if not checkParam(data, 'userId') or not checkParam(data, 'filters'):
            return jsonify(**{'message': 'Bad params'}), ErrorCode_BadParams

        routes = getRoute(data['userId'], data['filters'])
        if not routes:
            return jsonify(**{'routeGroups': ''}), ErrorCode_NotFound

        route_groups = []
        try:
            for route in routes:
                route_groups.append(dict(route))
            return jsonify(**{'routeGroups': route_groups}), ErrorCode_Success
        except Exception as e:
            # ValueError and TypeError will be raised if routes is a RouteGroup object
            if e.__class__.__name__ in ('ValueError', 'TypeError'):
                return jsonify(**{'routeGroups': dict(routes), "id": routes.id}), ErrorCode_Success
            else:
                routeRequestLogger.exception(request)
                return jsonify(**{'message': '{}'.format(str(e))}), ErrorCode_ServerError
    except:
        routeRequestLogger.exception(request)
        return jsonify(**{"message": "Unexpected Error"}), ErrorCode_ServerError
