import os
import json
from flask import Blueprint, send_from_directory, render_template, request

blueprint_swagger = Blueprint('blueprint_swagger',
                           __name__,
                           static_folder='static',
                           template_folder='templates')

fields = {
    'base_url': "/swagger",
    'config_json': {
        'dom_id': '#swagger-ui',
        'url': '/swagger/swagger.json'
    },
}

@blueprint_swagger.route('/')
def showDocs():
    return render_template('index.template.html', **fields)

@blueprint_swagger.route('/<path:path>')
def getStatic(path=None):
    return send_from_directory(
        os.path.join(
            blueprint_swagger.root_path,
            blueprint_swagger.static_folder
        ),
        path
    )