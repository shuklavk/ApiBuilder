from flask import Flask
import os
import onAppRunConfig.logConfig

def onProductionServer():
    return  os.getenv("ON_PRODUCTION_SERVER") == "True"

def getServerHostIP():
    return '0.0.0.0' if onProductionServer() else '127.0.0.1'

SERVER_ROOT = getServerHostIP()

CLIENT_ZIP = os.path.abspath(os.getcwd()) + '/zipRelease'