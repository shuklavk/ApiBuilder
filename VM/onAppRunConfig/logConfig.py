import os
import time
import json
import socket
import logging
from logging.handlers import RotatingFileHandler
from LoggerCreator import LoggerCreator

LOG_DIR = os.path.join(os.getcwd(), "logs")

if not os.path.isdir(LOG_DIR):
    os.mkdir(LOG_DIR)

logger = logging.getLogger("ABLog")
logger.setLevel(logging.DEBUG)

rotatingFilehandler = RotatingFileHandler("logs/Log_" + str(os.getpid()), maxBytes=20000, backupCount=5)
logger.addHandler(rotatingFilehandler)

hostname = socket.gethostname()
try:
    ip_address = socket.gethostbyname(hostname+".local")
except:
    ip_address = socket.gethostbyname(hostname)

loggerCreator = LoggerCreator(ip_address, os.getpid(), logger)
[routeRequestLogger, generalLogger, routeResponseLogger] = loggerCreator.createLoggers()