from flask import Flask, jsonify

# We have to initialize the database here to make sure it gets generated in time for future use
from server import init_db
init_db()

from onAppRunConfig import SERVER_ROOT

app = Flask(__name__)


from views.Pages import pages
from views.RouteGroup import routeGroup
from views.ObjectAttribute import objectAttribute
from views.APIGenerator import apiGenerator
from views.Swagger import swagger

app.register_blueprint(pages)
app.register_blueprint(routeGroup)
app.register_blueprint(objectAttribute)
app.register_blueprint(apiGenerator)
app.register_blueprint(swagger, url_prefix="/swagger")


if __name__ == "__main__":
    app.run(host=SERVER_ROOT, port=5050, debug=False, use_reloader=False)
