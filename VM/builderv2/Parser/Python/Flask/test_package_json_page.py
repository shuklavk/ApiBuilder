from builderv2.Parser.Python.Flask.Builder import PackageJSONPage
from builderv2.Templates.Python.Flask import PACKAGE_JSON

# Common Variables
empty_package_json_page = PackageJSONPage()

# Testing the constructor

def test_makeEmptyPackageJSONPageConstructor():
    p1 = empty_package_json_page

    assert p1.token_dict == None
    assert p1.name == "package.json"


def test_makeSimpleNPackageJSONPageConstructor():
    p1 = PackageJSONPage()

    assert p1.token_dict == None
    assert p1.name == "package.json"

# Testing Create Page

def test_createEmptyPackageJSONPage():
    p1 = PackageJSONPage()

    full_page = p1.createPage()
    assert "".join(full_page.split()) == "".join(PACKAGE_JSON.split())
