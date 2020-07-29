import os
import json
from flask import Blueprint, send_from_directory, render_template, request

swagger = Blueprint('some name',
                           __name__,
                           static_folder='dist',
                           template_folder='templates')

fields = {
    'base_url': "/swagger",
    'config_json': {
        'dom_id': '#swagger-ui',
        'url': '/swagger/swagger.json'
    },
}

@swagger.route('/')
def showDocs():
    return render_template('index.template.html', **fields)

@swagger.route('/<path:path>')
def getStatic(path=None):
    return send_from_directory(
        os.path.join(
            swagger.root_path,
            swagger.static_folder
        ),
        path
    )