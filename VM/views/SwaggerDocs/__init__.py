from flask import Flask, Blueprint, send_from_directory, render_template, request
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = 'http://192.168.1.162:5050/swagger.json'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL
)

swagger_blueprint = Blueprint("swagger", __name__)

@swaggerui_blueprint.route("/swagger.json")
def getSwagJson():
    return send_from_directory("static","swagger.json")