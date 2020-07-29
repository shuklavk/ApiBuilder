from builderv2.Parser.Python.Flask.Builder import NodeConfigPage

# Common Variables
empty_tokens = dict()
empty_node_config_page = NodeConfigPage(empty_tokens)

MODIFIED_NODE_CONFIG_PAGE = \
'''APP_TOKEN = ""

module.exports = (token) => {
    return token === APP_TOKEN
}
'''
# Testing the constructor

def test_makeEmptyNodeConfigPageConstructor():
    p1 = empty_node_config_page

    assert p1.token_dict == None
    assert p1.name == "config"


def test_makeSimpleNodeConfigPageConstructor():
    test_dict = {"test": "test"}
    p1 = NodeConfigPage(test_dict)

    assert p1.token_dict == test_dict
    assert p1.name == "config"

# Testing Create Page

def test_createEmptyNodeConfigPage():
    p1 = NodeConfigPage({'app_uuid': ""})

    full_page = p1.createPage()
    assert "".join(full_page.split()) == "".join(MODIFIED_NODE_CONFIG_PAGE.split())
