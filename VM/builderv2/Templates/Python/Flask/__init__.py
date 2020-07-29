HEADING = \
'''from flask import Flask, jsonify, request, Blueprint
from database.<class_name> import *
from server.Kit import *
from config import tokenCheck

blueprint_<class_name> = Blueprint('blueprint_<class_name>', __name__)'''

ROUTE_IMPORT = \
'''from server.<class_name> import <class_name>, create<class_name>, read<class_name>, update<class_name>, delete<class_name>
'''

RUNNER_PAGE = \
'''from flask import Flask
<class_blueprint_imports>
from server.swagger import blueprint_swagger
app = Flask(__name__)

if __name__ == "__main__":
    SERVER_ROOT = "<server_root>"
    app.debug = True

    # Register all the routes to the app
    <blueprint_registrations>

    app.register_blueprint(blueprint_swagger, url_prefix="/swagger")

    # Startup the connection to the database
    from database import init_db
    init_db()

    # Begin the actual application, serving it at this port number
    app.run(host=SERVER_ROOT, port=<port_number>)
'''

CLASS_BLUEPRINT_IMPORT = \
'''from server.<class_name> import blueprint_<class_name>
'''

BLUEPRINT_REGISTER = \
'''app.register_blueprint(blueprint_<class_name>)
    '''

RUN_CODE = \
'''
if __name__ == "__main__":
    SERVER_ROOT = "<server_root>"
    app = Flask(__name__)
    app.debug = True
    app.register_blueprint(blueprint_<class_name>)
    app.run(port=<port_number>)
'''

DATABASE_PAGE = \
'''from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os


parent_directory = (os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))))

if not os.path.exists(os.path.abspath(parent_directory + '/tmp')):
    os.makedirs(parent_directory + '/tmp')

engine = create_engine('sqlite:///tmp/DATABASE_<rand>.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    <db_imports>
    Base.metadata.create_all(bind=engine)
'''

# This is the page that will hold configs for the user's server. Keep inheritance to here at the lowest level
CONFIG_PAGE = \
'''APP_TOKEN = "<app_uuid>"

def tokenCheck(token):
    return token == APP_TOKEN
'''

# This template is responsible for adding the ability to check if the user is accessing the api from a valid app
# REQURES CONFIG PAGE IMPORT
# referred to as     <app_token_check>
APP_TOKEN_CHECK = \
'''
    if not checkParam(data, 'appToken') or not tokenCheck(data['appToken']):
        return jsonify(**{'message':'Unsupported App'}), ErrorCode_BadParams
'''

DB_IMPORT = \
'''import database.<class_name>
    '''

CRUD_POST_CREATE = \
'''
@blueprint_<class_name>.route("/create<class_name>", methods = [<supported_methods>])
def create<class_name>Route():
    data = request.get_json()

    <app_token_check>

    # the id parameter does not need checking on object creation
    params_on_create = <class_name>.params
    try:
        params_on_create.remove('id')
    except ValueError:
        pass
    if not checkParams(data, *params_on_create):
        return jsonify(**{'message':'Bad Params'}), ErrorCode_BadParams

    new_<class_name> = create<class_name>(<data_dict_params>)
    if new_<class_name> is None:
        return jsonify(**{'message':'Bad Params'}), ErrorCode_ServerError
    return jsonify(**dict(new_<class_name>)), ErrorCode_Success
'''

CRUD_POST_READ = \
'''
@blueprint_<class_name>.route("/read<class_name>", methods = [<supported_methods>])
def read<class_name>Route():
    data = request.get_json()

    <app_token_check>
    
    if not checkParam(data, 'filters'):
        return jsonify(**{'message':'Bad Params'}), ErrorCode_BadParams

    retrieved_<class_name>_list = read<class_name>(**data)
    if retrieved_<class_name>_list is None:
        return jsonify(**{'<class_name>':''}), ErrorCode_Success
    
    <class_name>_json_list = []
    try:
        for <class_name> in retrieved_<class_name>_list:
            <class_name>_json_list.append(dict(<class_name>))
        return jsonify(**{'<class_name>':<class_name>_json_list}), ErrorCode_Success
    except Exception as e:
        if e.__class__.__name__ in ('ValueError', 'TypeError'):
            return jsonify(**{'<class_name>':dict(retrieved_<class_name>_list)}), ErrorCode_Success
        else:
            print("An exception has occurred!\\n{}".format(str(e)))
            return jsonify(**{'message': '{}'.format(str(e))}), ErrorCode_ServerError
'''

CRUD_POST_UPDATE = \
'''
@blueprint_<class_name>.route("/update<class_name>", methods = [<supported_methods>])
def update<class_name>Route():
    data = request.get_json()

    <app_token_check>

    if not checkParam(data, 'id'):
        return jsonify(**{'message':'Bad Params'}), ErrorCode_BadParams

    if not (update<class_name>(int(data['id']), **data)):
        return jsonify(**{'message':'Bad object id'}), ErrorCode_NotFound
    return jsonify(**{}), ErrorCode_Success
'''

CRUD_POST_DELETE = \
'''
@blueprint_<class_name>.route("/delete<class_name>", methods = [<supported_methods>])
def delete<class_name>Route():
    data = request.get_json()

    <app_token_check>

    if not checkParam(data, 'id'):
        return jsonify(**{'message':'Bad Params'}), ErrorCode_BadParams

    if not (delete<class_name>(int(data['id']))):
        return jsonify(**{'message':'Bad object id'}), ErrorCode_NotFound
    return jsonify(**{}), ErrorCode_Success
'''

OBJECT_CLASS_CODE = \
'''from sqlalchemy import Column, <column_type_list>
from database import Base, db_session
from random import randint

class <class_name>(Base):

    params = [<object_params_as_strings>]

    __tablename__ = "<class_name>"
    <class_db_field_declerations>

    def __init__(self, <object_params>):
        <class_db_field_assignments>

        # set the id of the object to a random value
        # using a range unlikely to collide with other ids
        self.id = randint(0, 1000000)

    def __repr__(self):
        return '[<class_name> %r]' %self.id

    def __iter__(self):
        <yield_params>

    def __getitem(self, item):
        object_as_dict = dict(self)
        if item in object_as_dict:
            return object_as_dict[item]
        return None

def isValid<class_name>(obj_id):
    try:
        return <class_name>.query.filter(<class_name>.id==obj_id).one_or_none() is not None
    except Exception:
        return False

def create<class_name>(*args):
    if not isValid<class_name>(args[0]):
        new_obj = <class_name>(*args)
        db_session.add(new_obj)
        db_session.commit()
        return new_obj
    return dict() # an empty dict in case you are using **{} on this function's output

def read<class_name>(queries):
    attr = val = ""
    try:
        filter_list = []
        for attr, val in queries.items():
            filter_list.append(getattr(<class_name>, attr) == str(val))
        <class_name>_list = <class_name>.query.filter(*filter_list).all()
        return <class_name>_list if len(<class_name>_list) > 1 else <class_name>_list[0]
    except Exception as e:
        print("An exception occurred with the following details:\\n{}".format(str(e)))
        print("Attribute: {}\\tValue: {}\\n".format(attr, val))
        return None    

def update<class_name>(obj_id, **kwargs):
    if not isValid<class_name>(obj_id):
        return False

    retrieved_object = read<class_name>({"id":obj_id})

    for key, value in kwargs.items():
        if key in <class_name>.params:
            <kword_param_set_group>

    db_session.commit()
    return True

def delete<class_name>(obj_id):
    if not isValid<class_name>(obj_id):
        return False

    retrieved_object = read<class_name>({"id":obj_id})

    db_session.delete(retrieved_object)
    db_session.commit()
    return True
'''

CLASS_DB_FIELD_DECLARATION = \
'''
    <param_name> = Column(<column_type>, primary_key=<primary_key_bool>, nullable=<nullable_key_bool>, unique=<unique_key_bool>)'''

CLASS_DB_FIELD_ASSIGNMENT = \
'''
        self.<param_name> = <param_name>'''

# TODO: retire me!
CLASS_FIELD_ASSIGNMENT = \
'''
        self.<param_name> = <param_name>'''

# These likely need comma separations
DATA_DICT_PARAM = \
'''
        data['<param_name>'],'''

YIELD_PARAM = \
'''
        yield '<param_name>', self.<param_name>'''

KWORD_PARAM_SET = \
'''
            if key == '<param_name>':
                retrieved_object.<param_name> = value'''

# Kit file

KIT_PAGE = \
'''def checkParam(json, paramName):
    # Possible optimizations
    # 1) Take in multiples params and check each
    # for one line validation of objects
    # 2) make objects able to easily export all of their properties

    return (json is not None and
        paramName in json and
        json[paramName] is not None)


# check multiple params/ keys all in one function
def checkParams(json, *argv):
    if json is None:
        return False

    for param in argv:
        print 'check param: ' + param
        if param not in json or json[param] is None:
            return False

    return True

ErrorCode_ServerError   =   500
ErrorCode_NotFound      =   404
ErrorCode_BadParams     =   400
ErrorCode_Success       =   200
ErrorCode_ObjectCreated =   201
'''

REQUIREMENTS_PAGE = \
'''Click==7.0
Flask==1.1.1
itsdangerous==1.1.0
Jinja2==2.10.3
MarkupSafe==1.1.1
SQLAlchemy==1.3.10
Werkzeug==0.16.0
'''

### All the templates for the output JS Library that interacts with your newly created server!
JS_LIBRARY = \
'''
<route_functions>
'''

JS_ROUTE_FUNCTION = \
'''
function <action><className>(<js_inputs>)
{
    var request = new XMLHttpRequest();
    request.open('POST', '/<action><className>');
    request.setRequestHeader("Content-Type", "application/json; charset=UTF-8");

    // form the request json body
    var jsonData =
    {
        <request_entries>
    };

    request.onload = function() {
      if (request.status >= 200 && request.status < 400) {
        // Success!

        // Place code to edit html elements here!

      } else {
        // We reached our target server, but it returned an error
      }
    };

    request.onerror = function() {
      // There was a connection error of some sort
    };

    request.send(JSON.stringify(jsonData));
}
'''

JS_REQUEST_ENTRY = \
"""'<param_name>'  :   <param_name>,
"""

CLASS_BEGIN = "class <class_name>Lib {"

REQUIRED_ATTR_AND_TYPES = \
'''
    static getReqAttrAndTypes(){
        return <req_attr_and_types>
    }
'''

JS_CLASS_CREATE_FUNCTION = \
'''
    static async create(<object_params>) {
        // verify parameters and create data to send to the route
        const arrayOfAttributes = '<object_params>'.split(',');
        let routeGroupObj = {};
        for (let i = 0; i < arguments.length; i++) {
            if (
                typeof arguments[i] !==
                <class_name>Lib.getReqAttrAndTypes()[arrayOfAttributes[i]]
            ) {
                throw `${arrayOfAttributes[i]} expects ${<class_name>Lib.getReqAttrAndTypes()[arrayOfAttributes[i]]}, but recieved ${typeof arguments[i]}`;
            }
            routeGroupObj[arrayOfAttributes[i]] = arguments[i];
        }
        // Create and set id property to 0, currently required for the route
        routeGroupObj.appToken = "<app_uuid>";

        // request to server
        let resStream = await fetch(`/create<class_name>`, {
            method: 'POST',
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify(routeGroupObj),
        })
        .catch((err) => {
            console.log('Error:', err)
            return false;
        });

        let res = await resStream.json();

        return {
            createdObj: res,
            status: resStream.status === 200
        };
    }
'''

JS_CLASS_READ_FUNCTION = \
'''
    static async read(attributes_dict){
        for (const [attr_name, attr_val] of Object.entries(attributes_dict)) {
            if (typeof attr_val !== <class_name>Lib.getReqAttrAndTypes()[attr_name]) {
                throw "Bad Params! [Attribute Type Error]";
            }
        }
        let result_stream = await fetch(`/read<class_name>`, {
            method: 'POST',
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify("appToken":"<app_uuid>", "filters":attributes_dict)
        })
        .catch((err) => {
            console.log('Error: ', err);
            return false;
        });
        let res = await result_stream.json();

        return {
            readedObj:res,
            status:result_stream.status === 200
        };
    }
'''

JS_CLASS_UPDATE_FUNCTION = \
'''
    static async update(id, attributes_dict) {
        for (const [attr_name, attr_val] of Object.entries(attributes_dict)) {
            if(!<class_name>Lib.getReqAttrAndTypes()[attr_name])
                throw `${attr_name} is not an attribute of <class_name>`;

            if (typeof attr_val !== <class_name>Lib.getReqAttrAndTypes()[attr_name]) {
                throw `[Attribute Type Error] ${attr_name} expected ${<class_name>Lib.getReqAttrAndTypes()[attr_name]}, but received ${typeof attr_val}`;
            }
        }
        const updateAttributes = {};
        updateAttributes["id"] = id;
        updateAttributes["data"] = attributes_dict
        attributes_dict.appToken = "<app_uuid>";
        let result_stream = await fetch(`/update<class_name>`, {
            method: 'POST',
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify(updateAttributes)
        })
        .catch((err) => {
            console.log('Error: ', err);
            return false;
        });
        return result_stream.status === 200;
    }
'''

JS_CLASS_DELETE_FUNCTION = \
'''
    static async delete(id){
        if(typeof(id) !== "number") throw `[Attribute Type Error] ID expected of type 'number', but received of type ${typeof id}`;

        let resStream = await fetch(`/delete<class_name>`,{
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({id, appToken:"<app_uuid>"})
        })
        .catch((err) => {
            console.log('Error: ', err);
            return false;
        });
        return resStream.status===200;
    }
'''

CLASS_END = "}"

############################################################################
# Templates for Node Deployment

PACKAGE_JSON = \
'''
{
  "name": "projectName",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js"
  },
  "author": "",
  "license": "ISC",
  "dependencies": {
    "body-parser": "^1.19.0",
    "express": "^4.17.1",
    "sequelize": "^6.3.0",
    "sqlite3": "^5.0.0"
  },
  "devDependencies": {
    "nodemon": "^2.0.4"
  }
}
'''

NODE_DATABASE_PAGE = \
'''
const {Sequelize} = require('sequelize');

const db = new Sequelize({
    dialect: 'sqlite',
    storage: './tmp/DATABASE_<rand>.db'
});

const initDB = async () =>{
    try{
        await db.authenticate();
        console.log('Connection worked')
    }catch(err){
        console.log('Error! ', err)
    }
}

module.exports = {db, initDB}
  
'''

NODE_CLASS_DB_FIELD_DECLARATION = \
'''
    <param_name>: {
        type: DataTypes.<sequelize_type>,
        allowNull: <nullable_key_bool>
    },
'''

NODE_OBJECT_CLASS_CODE = \
'''
const { DataTypes } = require('sequelize')
const { db } = require('../database')

const <class_name>Attributes = {
<node_class_db_field_declerations>
}

const <class_name> = db.define('<class_name>', <class_name>Attributes)

<class_name>.sync()

const isValid<class_name> = async (objectId) => {
    const object = await <class_name>.findOne({where: {
        id: objectId
    }})
    .catch(err => {return false});
    if(object){
        return true;
    }
    return false;
}

const add<class_name> = async (objectOfAttributes) => {
    const object = await <class_name>.create(objectOfAttributes)
    .catch(err => {console.log('err', err)});

    return object;
}

const read<class_name> = async (objectId) => {
    if(!isValid<class_name>(objectId)){
        return null;
    }else{
        return await <class_name>.findOne({where: {
            id: objectId
        }})
    }
}

const findAll = async () => {
    const objects = await <class_name>.findAll()
    .catch(err => {})

    if(objects === undefined){
        console.log('Empty table');
        return {};
    }
    return objects;

}

const update<class_name> = async (objectId, attributesObject) => {
    if(!isValid<class_name>(objectId)){
        return false;
    }
    await <class_name>.update(attributesObject, {where: {id: objectId}})
    .catch(err => false)

    return true;
}

const delete<class_name> = async (objectId) => {
    if(!isValid<class_name>(objectId)){
        return false;
    }

    await <class_name>.destroy({where: {
        id: objectId
    }})
    .catch(err => false)

    return true;

}

module.exports = {isValid<class_name>, add<class_name>, read<class_name>, update<class_name>, delete<class_name>, findAll, <class_name>Attributes}
'''

NODE_IMPORT_ROUTE = \
'''app.use(require('./server/<class_name>/<class_name>'));
'''

NODE_RUNNER_PAGE = \
'''
const express = require('express');
const bodyParser = require('body-parser');
const path = require('path')
const {initDB} = require('./database/database')

const app = express();
app.use(bodyParser.json())
const PORT = <port_number>;

<node_class_blueprint_imports>

initDB();

app.listen(PORT, function () {
    console.log(`Listening on port ${PORT}`)
});
'''

# This is the page that will hold configs for the user's server. Keep inheritance to here at the lowest level
NODE_CONFIG_PAGE = \
'''APP_TOKEN = "<app_uuid>"

module.exports = (token) => {
    return token === APP_TOKEN
}
'''

NODE_HEADING = \
'''const express = require('express');
const router = express.Router();

const <class_name>DB = require('../../database/<class_name>/<class_name>')
const Kit = require('../Kit/Kit')

router.use(function timeLog(req, res, next) {
    console.log('Time: ', Date.now());
    next();
});
'''

NODE_CRUD_POST_CREATE = \
'''
router.post('/create<class_name>', async function (req, res) {
    res.contentType('application/json');

    const checkedParams = await Kit.checkParams(req.body, <class_name>DB.<class_name>Attributes);
    if(!checkedParams){
       return res.status(Kit.ErrorCode_BadParams).send({'message':'Bad Params'});
    }

    const new_<class_name> = await <class_name>DB.add<class_name>(req.body);

    if(!new_<class_name>){
       return res.status(Kit.ErrorCode_ServerError).send({'message':'Bad Params'});
    }

    return res.status(Kit.ErrorCode_Success).send(new_<class_name>);
})
'''

NODE_CRUD_POST_READ = \
'''
router.post('/read<class_name>', async function (req, res) {
    res.contentType('application/json');

    const checkedParams = await Kit.checkParam(req.body, 'id');
    if(!checkedParams){
        return res.status(Kit.ErrorCode_BadParams).send({'message':'Bad Params'});
    }

    const retrieved_obj_<class_name> = await <class_name>DB.read<class_name>(req.body['id'])

    if(!retrieved_obj_<class_name>){
       return res.status(Kit.ErrorCode_NotFound).send({'message':'Bad object id'});
    }

    return res.status(Kit.ErrorCode_Success).send(retrieved_obj_<class_name>)
})
'''

NODE_CRUD_POST_UPDATE = \
'''
router.post('/update<class_name>', async function (req, res) {
    res.contentType('application/json');

    const checkedParams = await Kit.checkParam(req.body, 'id');
    if(!checkedParams){
        return res.status(Kit.ErrorCode_BadParams).send({'message':'Bad Params'});
    }

    if (! await <class_name>DB.update<class_name>(req.body['id'], req.body['data'])){
        return res.status(ErrorCode_NotFound).send({'message':'Bad object id'})
    }

    return res.status(Kit.ErrorCode_Success).send({})
})
'''

NODE_CRUD_POST_DELETE = \
'''
router.post('/delete<class_name>', async function (req, res) {
    res.contentType('application/json');

    const checkedParams = await Kit.checkParam(req.body, 'id');
    if(!checkedParams){
        return res.status(Kit.ErrorCode_BadParams).send({'message':'Bad Params'});
    }

    if (! await <class_name>DB.delete<class_name>(req.body['id'])){
        return res.status(Kit.ErrorCode_NotFound).send({'message':'Bad object id'})
    }
    return res.status(Kit.ErrorCode_Success).send({})
})
'''
NODE_ROUTE_PAGE_ENDING = \
'''module.exports = router;'''

NODE_KIT_PAGE = \
'''const checkParam = async (json, paramName) => {
    return json && json.hasOwnProperty(paramName) && (json[paramName] || json[paramName] === 0);
}

const checkParams = async (json, params) => {
    if(!json){
        return false;
    }

    for(const param in params){
        if(!json.hasOwnProperty(param) || !json[param]){
            return false;
        }
    }

    return true;

}

const ErrorCode_ServerError   =   500;
const ErrorCode_NotFound      =   404;
const ErrorCode_BadParams     =   400;
const ErrorCode_Success       =   200;
const ErrorCode_ObjectCreated =   201;

module.exports = { checkParam, checkParams, ErrorCode_ServerError, ErrorCode_NotFound, ErrorCode_BadParams, ErrorCode_Success, ErrorCode_ObjectCreated }
'''
