from builderv2.Parser.Python.Flask.Builder import NodeRunnerPage
from builderv2.Templates.Python.Flask import NODE_RUNNER_PAGE

# Common Variables
empty_tokens = dict()
empty_node_runner_page = NodeRunnerPage(empty_tokens)

MODIFIED_NODE_RUNNER_PAGE = \
'''
const express = require('express');
const bodyParser = require('body-parser');
const path = require('path')
const {initDB} = require('./database/database')

const app = express();
app.use(bodyParser.json())
const PORT = ;



initDB();

app.listen(PORT, function () {
    console.log(`Listening on port ${PORT}`)
});
'''

# Testing the constructor

def test_makeEmptyNodeRunnerPageConstructor():
    p1 = empty_node_runner_page

    assert p1.token_dict == None
    assert p1.name == "index.js"


def test_makeSimpleNodeRunnerPageConstructor():
    test_dict = {"test": "test"}
    p1 = NodeRunnerPage(test_dict)

    assert p1.token_dict == test_dict
    assert p1.name == "index.js"

# Testing Create Page

def test_createEmptyNodeRunnerPage():
    p1 = NodeRunnerPage(
        {'port_number': "", 'node_class_blueprint_imports': ""})

    full_page = p1.createPage()
    assert "".join(full_page.split()) == "".join(MODIFIED_NODE_RUNNER_PAGE.split())
