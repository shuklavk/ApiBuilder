from flask import render_template, Blueprint, jsonify, send_from_directory, request
from server.User.UserDB import gimmeNewUser, isValidUser
from server.Kit import *
import os
import time
from onAppRunConfig.logConfig import routeRequestLogger, routeResponseLogger
import json

pages = Blueprint('pages', __name__)

"""Landing Page HTML/CSS"""
@pages.route("/", methods=['GET'])
def pre_ship():
    try:
        routeRequestLogger.info(request)
        return render_template("index.html")
    except:
        routeRequestLogger.exception(request)
        return jsonify(**{"message": "Unexpected Error"}), ErrorCode_ServerError

"""
Returns JSON object with a fake user's id

Temporary Solution to authentication. 
"""
@pages.route("/grabFakeUser", methods=['GET'])
def grabFakeUser():
    try:
        routeRequestLogger.info(request=request)
        
        newUser = gimmeNewUser()
        response_body = jsonify(**{'id': newUser.id})

        routeResponseLogger.info(
            request=request,
            response_body=json.dumps({'id': newUser.id}),
            status_code=ErrorCode_Success
        )    

        return response_body
    except:
        routeRequestLogger.exception(request)
        return jsonify(**{"message": "Unexpected Error"}), ErrorCode_ServerError


"""Returns userId and a status of ErrorCode_Success if the userId is valid, else a Bad Params error and a status of ErrorCode_BadParams"""
@pages.route('/isValidUser', methods=['POST'])
def checkValidUser():
    try:
        data = request.get_json()

        routeRequestLogger.info(request)

        if not checkParam(data, 'userId'):
            return jsonify(**{'message': 'Bad params'}), ErrorCode_BadParams
        if not isValidUser(int(data['userId'])):
            return jsonify(**{'message': 'Invalid User'}), ErrorCode_NotFound
        return jsonify(**{'id': int(data['userId'])}), ErrorCode_Success
    except:
        routeRequestLogger.exception(request)
        return jsonify(**{"message": "Unexpected Error"}), ErrorCode_ServerError

"""Adds icon to the web browser tab"""
@pages.route('/favicon.ico')
def favicon():
    try: 
        routeRequestLogger.info(request)
        return send_from_directory(os.path.join(app.root_path, 'static'), 'output.ico',mimetype='image/vnd.microsoft.icon')
    except:
        routeRequestLogger.exception(request)
        return jsonify(**{"message": "Unexpected Error"}), ErrorCode_ServerError
