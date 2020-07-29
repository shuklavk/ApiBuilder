from builderv2.Parser.Python.Flask.Builder import NodeRoutePage
from builderv2.Templates.Python.Flask import NODE_HEADING, NODE_CRUD_POST_CREATE, NODE_CRUD_POST_READ, NODE_CRUD_POST_UPDATE, NODE_CRUD_POST_DELETE, NODE_ROUTE_PAGE_ENDING

# Common Variables
empty_tokens = dict()
empty_node_object_page = NodeRoutePage(empty_tokens, "")
MODIFIED_NODE_HEADING = \
'''const express = require('express');
const router = express.Router();

const DB = require('../../database//')
const Kit = require('../Kit/Kit')

router.use(function timeLog(req, res, next) {
    console.log('Time: ', Date.now());
    next();
});
'''

MODIFIED_NODE_CRUD_POST_CREATE = \
'''
router.post('/create', async function (req, res) {
    res.contentType('application/json');

    const checkedParams = await Kit.checkParams(req.body, DB.Attributes);
    if(!checkedParams){
       return res.status(Kit.ErrorCode_BadParams).send({'message':'Bad Params'});
    }

    const new_ = await DB.add(req.body);

    if(!new_){
       return res.status(Kit.ErrorCode_ServerError).send({'message':'Bad Params'});
    }

    return res.status(Kit.ErrorCode_Success).send(new_);
})
'''

MODIFIED_NODE_CRUD_POST_READ = \
'''
router.post('/read', async function (req, res) {
    res.contentType('application/json');

    const checkedParams = await Kit.checkParam(req.body, 'id');
    if(!checkedParams){
        return res.status(Kit.ErrorCode_BadParams).send({'message':'Bad Params'});
    }

    const retrieved_obj_ = await DB.read(req.body['id'])

    if(!retrieved_obj_){
       return res.status(Kit.ErrorCode_NotFound).send({'message':'Bad object id'});
    }

    return res.status(Kit.ErrorCode_Success).send(retrieved_obj_)
})
'''

MODIFIED_NODE_CRUD_POST_UPDATE = \
'''
router.post('/update', async function (req, res) {
    res.contentType('application/json');

    const checkedParams = await Kit.checkParam(req.body, 'id');
    if(!checkedParams){
        return res.status(Kit.ErrorCode_BadParams).send({'message':'Bad Params'});
    }

    if (! await DB.update(req.body['id'], req.body['data'])){
        return res.status(ErrorCode_NotFound).send({'message':'Bad object id'})
    }

    return res.status(Kit.ErrorCode_Success).send({})
})
'''

MODIFIED_NODE_CRUD_POST_DELETE = \
'''
router.post('/delete', async function (req, res) {
    res.contentType('application/json');

    const checkedParams = await Kit.checkParam(req.body, 'id');
    if(!checkedParams){
        return res.status(Kit.ErrorCode_BadParams).send({'message':'Bad Params'});
    }

    if (! await DB.delete(req.body['id'])){
        return res.status(Kit.ErrorCode_NotFound).send({'message':'Bad object id'})
    }
    return res.status(Kit.ErrorCode_Success).send({})
})
'''
MODIFIED_NODE_ROUTE_PAGE_ENDING = \
'''module.exports = router;'''

FINAL_MODIFIED_STRING = MODIFIED_NODE_HEADING + MODIFIED_NODE_CRUD_POST_CREATE + MODIFIED_NODE_CRUD_POST_READ + MODIFIED_NODE_CRUD_POST_UPDATE + MODIFIED_NODE_CRUD_POST_DELETE + MODIFIED_NODE_ROUTE_PAGE_ENDING
# Testing the constructor

def test_makeEmptyNodeRoutePageConstructor():
    p1 = empty_node_object_page

    assert p1.token_dict == None
    assert p1.name == ""


def test_makeSimpleNodeRoutePageConstructor():
    test_dict = {"test": "test"}
    test_page_name = "testPage"
    p1 = NodeRoutePage(test_dict, test_page_name)

    assert p1. token_dict == test_dict
    assert p1.name == test_page_name

# Testing Create Page

def test_createEmptyNodeRoutePage():
    p1 = NodeRoutePage(
        {'class_name': ""}, '')

    full_page = p1.createPage()
    assert "".join(full_page.split()) == "".join(FINAL_MODIFIED_STRING.split())
