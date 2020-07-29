from flask import Blueprint, jsonify, request
from server.Kit import *
from server.ObjectAttributes.ObjectAttributesDB import ObjectAttributes, addObjectAttributes, retrieveObjectAttributes, deleteObjectAttributes, updateObjectAttributes, isValidAttribute, getSingleObjectAttribute
from server.User.UserDB import retrieveUser, isValidUser
from server.RouteGroup.RouteGroupDB import getRoute
from onAppRunConfig.logConfig import routeRequestLogger

objectAttribute = Blueprint('objectAttribute', __name__)

"""
Add's Attributes to a RouteGroup

Request data provides: userId, objectId, attributes
    attributes is an array of objects (one for each attribute)
        each object contains: name, isUnique, isEncrypted, generationMethod,
                                type, isNullable, description
For each attribute, uses it's info and creates an Attributes Object.
Links each each attribute to a specific user and a Route Group in the database.
Collects the ids of each attribute and stores in an array (attributeIds).
Returns a JSON objects with attributeIds and a status code of ErrorCode_Success
"""
@objectAttribute.route("/addObjectAttributes", methods=['POST'])
def addObjectAttribute():
    try:
        data = request.get_json()

        routeRequestLogger.info(request)

        if not checkParams(data, *['userId', 'objectId', 'attributes']):
            return jsonify(**{'message': 'Bad params'}), ErrorCode_BadParams

        attributeIds = []

        user = retrieveUser(data['userId'])
        route = getRoute(user.id, {"id": data['objectId']})
        for row in data['attributes']:
            if not checkParams(row, *ObjectAttributes.params):
                return jsonify(**{'message': 'Bad params'}), ErrorCode_BadParams
            if row['name'] == '':
                return jsonify(**{'message': 'Bad params'}), ErrorCode_BadParams

            routeRequestLogger.info(
                request_method=POST,
                url=request.path,
                request_body=data,
                client_ip=request.remote_addr
            )

            if not checkParams(data, *['userId', 'objectId', 'attributes']):
                return jsonify(**{'message': 'Bad params'}), ErrorCode_BadParams

            newObjectAttributes = ObjectAttributes(
                data['userId'],
                data['objectId'],
                row['name'],
                row['type'],
                row['description'],
                row['isUnique'],
                row['isEncrypted'],
                row['isNullable'],
                row['generationMethod']
            )
            addObjectAttributes(user.id, route.id, newObjectAttributes)

            attributeIds += [newObjectAttributes.id]

        return jsonify(**{'attributeIds': attributeIds}), ErrorCode_Success
    except:
        routeRequestLogger.exception(request)


"""Returns all attributes of a RouteGroup object"""
@objectAttribute.route('/getObjectAttributes', methods=['POST'])
def getObjectAttributes():
    try:
        data = request.get_json()

        routeRequestLogger.info(request)

        if not checkParam(data, 'userId') or \
            not checkParam(data, 'objectId') or \
                not isValidUser(int(data['userId'])):
            return jsonify(**{'message': 'Bad params'}), ErrorCode_BadParams

        object_attrs = retrieveObjectAttributes(int(data['userId']), int(data['objectId']))
        attributes = []
        for obj in object_attrs:
            attributes.append(dict(obj))
        return jsonify(**{'attributes': attributes}), ErrorCode_Success
    except:
        routeRequestLogger.exception(request)
        return jsonify(**{"message": "Unexpected Error"}), ErrorCode_ServerError

'''Updates Object Attribute with information in updatedObjectAttribute dictionary '''
@objectAttribute.route('/updateObjectAttribute', methods=['POST'])
def updateObjectAttribute():
    try:
        data = request.get_json()

        routeRequestLogger.info(request)

        if data is None:
            return jsonify(**{'message': 'No data found'}), ErrorCode_ServerError
        
        if not checkParam(data, 'userId') or not checkParam(data, 'attributeId') or not\
            checkParams(data['updatedObjectAttribute'], *ObjectAttributes.params):
            return jsonify(**{'message': 'Bad params'}), ErrorCode_BadParams
        
        user = retrieveUser(data['userId'])
        if user is None:
            return jsonify(**{'message': 'No data found'}), ErrorCode_ServerError
        if not isValidUser(user.id):
            return jsonify(**{'message': 'Bad Params'}), ErrorCode_BadParams 
        
        if updateObjectAttributes(user.id, data['attributeId'], **data['updatedObjectAttribute']):
            return jsonify(**{'attributeId': data['attributeId']}), ErrorCode_Success
        
        return jsonify(**{'message': 'Update failed'}), ErrorCode_ServerError
    except:
        routeRequestLogger.exception(request)
        return jsonify(**{"message": "Unexpected Error"}), ErrorCode_ServerError

'''Updates all Object Attributes associated with a given Route Group id '''
@objectAttribute.route('/updateMultipleObjectAttributes', methods=['POST'])
def updateMultipleObjectAttributes():
    try:
        data = request.get_json()

        routeRequestLogger.info(request)

        if data is None:
            return jsonify(**{'message': 'No data found'}), ErrorCode_ServerError
        
        if not checkParam(data, 'userId') or not checkParam(data, 'objectId') or not checkParam(data, 'attributes') or not checkParam(data, "deletedAttr"):
            return jsonify(**{'message': 'Bad params'}), ErrorCode_BadParams
        
        user = retrieveUser(data['userId'])
        attrToDelete = data['deletedAttr']
        for i in attrToDelete:
            deleteObjectAttributes(user.id, int(i))
        if user is None:
            return jsonify(**{'message': 'No data found'}), ErrorCode_ServerError
        if not isValidUser(user.id):
            return jsonify(**{'message': 'Bad Params'}), ErrorCode_BadParams 

        allDBAttributes = retrieveObjectAttributes(user.id, data['objectId'])
        for dbAttributes in allDBAttributes:
            deleteObjectAttributes(user.id, dbAttributes.id)
        
        allAttributes = data['attributes']
        for attrId in allAttributes:
            modifiedAttrDict = allAttributes[attrId]
            if(modifiedAttrDict["name"] == "" or modifiedAttrDict["type"] == ""):
                continue
            modifiedAttrDict['description'] = ""
            modifiedAttrDict['isUnique'] = True
            modifiedAttrDict['isEncrypted'] = True
            modifiedAttrDict['isNullable'] = True
            modifiedAttrDict['generationMethod'] = ""
            if isValidAttribute(modifiedAttrDict["name"], data['objectId'], user.id):
                try:
                    if str(attrId) in attrToDelete:
                        deleteObjectAttributes(user.id, attrId)
                    else:
                        updateObjectAttributes(user.id, attrId, modifiedAttrDict)
                except Exception as e: print(e)
            else:
                try:
                    newObjectAttributes = ObjectAttributes(
                        user.id,
                        data['objectId'],
                        modifiedAttrDict['name'],
                        modifiedAttrDict['type'],
                        modifiedAttrDict['description'],
                        modifiedAttrDict['isUnique'],
                        modifiedAttrDict['isEncrypted'],
                        modifiedAttrDict['isNullable'],
                        modifiedAttrDict['generationMethod']
                    )
                    addObjectAttributes(user.id, data['objectId'], newObjectAttributes)
                except Exception as e: print(e)
        
        # if updateObjectAttributes(user.id, data['attributeId'], **data['updatedObjectAttribute']):
        #     return jsonify(**{'attributeId': data['attributeId']}), ErrorCode_Success
        
        # return jsonify(**{'message': 'Update failed'}), ErrorCode_ServerError
        return jsonify(**{'message': 'Update success'}), ErrorCode_Success
    except:
        routeRequestLogger.exception(request)
        return jsonify(**{"message": "Unexpected Error"}), ErrorCode_ServerError

'''Deletes an Object Attribute provided a valid id'''
@objectAttribute.route('/deleteObjectAttribute', methods=['POST'])
def deleteObjectAttribute():
    try:
        data = request.get_json()

        routeRequestLogger.info(request)

        if data is None:
            return jsonify(**{'message': 'No data found'}), ErrorCode_ServerError
        
        if not checkParam(data, 'userId') or not checkParam(data, 'attributeId'):
            return jsonify(**{'message': 'Bad params'}), ErrorCode_BadParams
        
        user = retrieveUser(data['userId'])
        if user is None:
            return jsonify(**{'message': 'No data found'}), ErrorCode_ServerError
        if not isValidUser(user.id):
            return jsonify(**{'message': 'Bad Params'}), ErrorCode_BadParams

        deleteObjectAttributes(user.id, data['attributeId'])
    
        return jsonify(**{}), ErrorCode_Success
    except:
        routeRequestLogger.exception(request)
        return jsonify(**{"message": "Unexpected Error"}), ErrorCode_ServerError
