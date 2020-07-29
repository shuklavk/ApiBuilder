from builderv2.Parser.Python.Flask.Builder import NodeObjectPage
from builderv2.Templates.Python.Flask import NODE_OBJECT_CLASS_CODE

# Common Variables
empty_tokens = dict()
empty_node_object_page = NodeObjectPage(empty_tokens, "")
MODIFIED_NODE_OBJECT_CLASS_CODE = \
'''
const { DataTypes } = require('sequelize')
const { db } = require('../database')

const Attributes = {

}

const  = db.define('', Attributes)

.sync()

const isValid = async (objectId) => {
    const object = await .findOne({where: {
        id: objectId
    }})
    .catch(err => {return false});
    if(object){
        return true;
    }
    return false;
}

const add = async (objectOfAttributes) => {
    const object = await .create(objectOfAttributes)
    .catch(err => {console.log('err', err)});

    return object;
}

const read = async (objectId) => {
    if(!isValid(objectId)){
        return null;
    }else{
        return await .findOne({where: {
            id: objectId
        }})
    }
}

const findAll = async () => {
    const objects = await .findAll()
    .catch(err => {})

    if(objects === undefined){
        console.log('Empty table');
        return {};
    }
    return objects;

}

const update = async (objectId, attributesObject) => {
    if(!isValid(objectId)){
        return false;
    }
    await .update(attributesObject, {where: {id: objectId}})
    .catch(err => false)

    return true;
}

const delete = async (objectId) => {
    if(!isValid(objectId)){
        return false;
    }

    await .destroy({where: {
        id: objectId
    }})
    .catch(err => false)

    return true;

}

module.exports = {isValid, add, read, update, delete, findAll, Attributes}
'''

# Testing the constructor

def test_makeEmptyNodeObjectPageConstructor():
    p1 = empty_node_object_page

    assert p1.token_dict == None
    assert p1.name == ""


def test_makeSimpleNodeObjectPageConstructor():
    test_dict = {"test": "test"}
    test_page_name = "testPage"
    p1 = NodeObjectPage(test_dict, test_page_name)

    assert p1. token_dict == test_dict
    assert p1.name == test_page_name

# Testing Create Page

def test_createEmptyNodeObjectPage():
    p1 = NodeObjectPage(
        {'class_name': "", 'node_class_db_field_declerations': ""}, '')

    full_page = p1.createPage()
    assert "".join(full_page.split()) == "".join(MODIFIED_NODE_OBJECT_CLASS_CODE.split())
