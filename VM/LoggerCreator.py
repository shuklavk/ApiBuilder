import json
import time
import os
import socket

class LoggerCreator:

    def __init__(self, server_ip, pid, logger):
        self.server_ip = server_ip
        self.pid = pid
        self.logger = logger

    def createLoggers(self):
        return [
            RouteRequestLogger(self.server_ip, self.pid, self.logger),
            GeneralLogger(self.server_ip, self.pid, self.logger),
            RouteResponseLogger(self.server_ip, self.pid, self.logger)
        ]

class RouteRequestLogger:

    def __init__(self, server_ip, pid, logger):
        self.server_ip = server_ip
        self.pid = pid
        self.logger = logger

    def info(self, request):
        try:
            request_body = request.get_json()
        except:
            request_body = request.data

        self.logger.info("[INFO] requesting '" + request.path + "' " + json.dumps({
            "server_ip": self.server_ip,
            "time": time.ctime(time.time()),
            "pid": self.pid,
            "request_method": request.method,
            "request_body": request_body,
            "path": request.path,
            "client_ip": request.remote_addr
        },
        indent=4))

    def exception(self, request):
        try:
            request_body = request.get_json()
        except:
            request_body = request.data

        self.logger.exception("[ERROR] requesting '" + request.path + "' " + json.dumps({
            "server_ip": self.server_ip,
            "time": time.ctime(time.time()),
            "pid": self.pid,
            "request_method": request.method,
            "request_body": request_body,
            "path": request.path,
            "client_ip": request.remote_addr
        }, indent=4) + "\n")

class GeneralLogger:

    def __init__(self, server_ip, pid, logger):
        self.server_ip = server_ip
        self.pid = pid
        self.logger = logger

    def info(self, message):
        self.logger.info("[INFO] " + message + json.dumps({
            "server_ip": self.server_ip,
            "time": time.ctime(time.time()),
            "pid": self.pid,
            "message": message
        }, 
        indent=4))

    def error(self, message):
        self.logger.error("[ERROR] " + message + json.dumps({
            "server_ip": self.server_ip,
            "time": time.ctime(time.time()),
            "pid": self.pid,
            "message": message
        }, 
        indent=4))

class RouteResponseLogger:

    def __init__(self, server_ip, pid, logger):
        self.server_ip = server_ip
        self.pid = pid
        self.logger = logger

    def info(self, request, status_code, response_body):
        try:
            request_body = request.get_json()
        except:
            request_body = request.data

        self.logger.info("[INFO] responding to request to " + request.path + " " + json.dumps({
            "server_ip": self.server_ip,
            "time": time.ctime(time.time()),
            "pid": self.pid,
            "request_method": request.method,
            "request_body": request_body,
            "response_body": response_body,
            "path": request.path,
            "client_ip": request.remote_addr,
            "status_code": status_code
        },
        indent=4))