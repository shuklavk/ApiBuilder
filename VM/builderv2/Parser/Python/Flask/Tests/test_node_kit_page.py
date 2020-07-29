from builderv2.Parser.Python.Flask.Builder import NodeKitPage
from builderv2.Templates.Python.Flask import NODE_KIT_PAGE

# Common Variables
empty_node_kit_page = NodeKitPage()

# Testing the constructor

def test_makeEmptyNodeKitPageConstructor():
    p1 = empty_node_kit_page

    assert p1.token_dict == None
    assert p1.name == "Kit.js"


def test_makeSimpleNodeKitPageConstructor():
    p1 = NodeKitPage()

    assert p1.token_dict == None
    assert p1.name == "Kit.js"

# Testing Create Page

def test_createEmptyNodeKitPage():
    p1 = NodeKitPage()

    full_page = p1.createPage()
    assert "".join(full_page.split()) == "".join(NODE_KIT_PAGE.split())
