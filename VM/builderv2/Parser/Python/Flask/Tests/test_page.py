from builderv2.Parser.Python.Flask.Builder import Page

# Common Variables
empty_page = Page([], dict(), "")

# Testing the constructor

def test_makeEmptyPageConstructor():
    p1 = Page([], dict(), "")

    assert p1.templates == []
    assert p1.token_dict is None
    assert p1.name == ""

def test_makeSimplePageConstructor():
    test_dict = {"test": "test"}
    test_page_name = "testPage"
    p1 = Page([], test_dict, test_page_name)

    assert p1.templates == []
    assert p1. token_dict == test_dict
    assert p1.name == test_page_name


# Testing Create Page

def test_createEmptyPage():
    p1 = Page([], dict(), "")

    full_page = p1.createPage()
    assert full_page == ""

def test_createSimplePage_EmptyDict():
    p1 = Page(["TestTemplate"], dict(), "testPage")

    full_page = p1.createPage()
    assert full_page == "TestTemplate"


simple_template =\
    "Hello, <world>!"


simple_dict = {
    "world" : "world"
}

expected_output =\
    "Hello, world!\n"

def test_createSimplePage_NoDict():
    p1 = Page([simple_template], dict(), "test")
    try:
        p1.createPage()

        # You shouldn't reach this spot in the code
        assert False
    except ValueError:
        # This is the expected exception. Let others bubble up and fail the test
        pass

def test_createSimplePage_SimpleDict():
    p1 = Page([simple_template], simple_dict, "hey")

    full_page = p1.createPage()
    assert full_page == expected_output


complex_dict = {
    "world"      : "world",
    "nonNeed"    : "nonNeed",
    "?"          : "?"
}
def test_createSimplePage_ComplexDict():
    p1 = Page([simple_template], simple_dict, "hey")

    full_page = p1.createPage()
    assert full_page == expected_output

def test_createMultiPage_ComplexDict():
    p1 = Page([simple_template, simple_template], simple_dict, "hey")

    assert p1.createPage() == (expected_output + expected_output)


# Testing extract Page Tokens

def test_extractPageTokens_empty():
    assert empty_page.extractPageTokens() == set()

def test_extractPageTokens_filled():
    p1 = Page([simple_template], dict(), "testPage")

    tokens = p1.extractPageTokens()
    assert tokens is not None

    assert "world" in tokens

complex_template =\
    "<1><2><3><4><5><6><7>"
def test_extractPageTokens_multiple():
    p1 = Page([simple_template, complex_template], dict(), "complexPage")

    tokens = p1.extractPageTokens()

    assert tokens is not None

    assert False not in [str(i) in tokens for i in xrange(1,8)]
    assert "world" in tokens


# Testing generating Tokens

def test_genTokens_empty():
    assert empty_page.genTokens(None) is None

def test_genTokens_className():
    class_name = "class"
    test_dict = {"class_name": class_name}

    # ok to use empty page here since genTokens doesn't rely on anything internal
    tokens = empty_page.genTokens(test_dict)
    assert tokens is not None


    assert "class_name" in tokens
    assert tokens["class_name"] == class_name

    assert "object_name" in tokens
    assert tokens["object_name"] == "obj_" + class_name

    assert 'rand' in tokens

def test_genTokens_allClassNamesList_noDropRoot():
    all_class = "all_class"
    test_dict = {"all_class_names_list": [all_class]}

    # ok to use empty page here since genTokens doesn't rely on anything internal
    tokens = empty_page.genTokens(test_dict)
    assert tokens is not None

    assert "all_class_names_list" in tokens
    assert tokens["all_class_names_list"] == test_dict["all_class_names_list"]

    assert "all_class_names" in tokens
    assert tokens["all_class_names"] == all_class

    assert "blueprint_registrations" in tokens
    assert tokens["blueprint_registrations"] == "app.register_blueprint(blueprint_" + all_class + ")\n    "

    assert "class_blueprint_imports" in tokens
    assert tokens["class_blueprint_imports"] == "from server." + all_class + " import blueprint_" + all_class +"\n"

    assert "rand" in tokens

    # Make sure these aren't in the dictionary yet
    assert "drop_root" not in tokens
    assert "api_name" not in tokens
    assert "db_imports" not in tokens

def test_genTokens_allClassNamesList_noDropRoot():
    all_class = "all_class"
    test_dict = {"all_class_names_list" : [all_class],
                 "drop_root"            : "root",
                 "api_name"             : "api-name"}

    # ok to use empty page here since genTokens doesn't rely on anything internal
    tokens = empty_page.genTokens(test_dict)
    assert tokens is not None

    assert "all_class_names_list" in tokens
    assert tokens["all_class_names_list"] == test_dict["all_class_names_list"]

    assert "all_class_names" in tokens
    assert tokens["all_class_names"] == all_class

    assert "blueprint_registrations" in tokens
    assert tokens["blueprint_registrations"] == "app.register_blueprint(blueprint_" + all_class + ")\n" + " " * 4

    assert "class_blueprint_imports" in tokens
    assert tokens["class_blueprint_imports"] == "from server." + all_class + " import blueprint_" + all_class +"\n"

    assert "rand" in tokens

    # Now make sure these are present
    assert "drop_root" in tokens
    assert tokens["drop_root"] == test_dict["drop_root"]

    assert "api_name" in tokens
    assert tokens["api_name"] == test_dict["api_name"]

    assert "db_imports" in tokens
    assert tokens["db_imports"] == "import database." + all_class + "\n" + " " * 4


def test_genTokens_Params_IncompleteParams():
    token_dict = {"object_params": "params"}
    returned_tokens = empty_page.genTokens(token_dict)
    assert "yield_params" not in returned_tokens


    token_dict["column_types"] = "types"
    returned_tokens = empty_page.genTokens(token_dict)
    assert "yield_params" not in returned_tokens

    token_dict["column_primary_key_list"] = "primary"
    returned_tokens = empty_page.genTokens(token_dict)
    assert "yield_params" not in returned_tokens

    token_dict["column_nullable_list"] = "nulls"
    returned_tokens = empty_page.genTokens(token_dict)
    assert "yield_params" not in returned_tokens

    token_dict["column_unique_list"] = "uniques"
    token_dict.pop("column_nullable_list")
    returned_tokens = empty_page.genTokens(token_dict)
    assert "yield_params" not in returned_tokens

    assert "rand" in returned_tokens

# shared
param_dict = {
    "object_params": 'param1',
    "column_types": ['int'],
    "column_primary_key_list": ['true'],
    "column_nullable_list": ['True'],
    "column_unique_list": ['false']
}

def test_genTokens_Params_Malformed():
    test_dict = param_dict.copy()
    test_dict["column_unique_list"] = []

    try:
        returned_tokens = empty_page.genTokens(test_dict)

        # This code should not be reachable
        assert not returned_tokens or False
    except IndexError:
        # Failed as intended. Continue on. Let other errors pass through so it fails the test
        pass

def test_genTokens_Params_perfectRun():
    returned_tokens = empty_page.genTokens(param_dict)

    # Do full page checks in other tests
    assert "yield_params" in returned_tokens
    assert "\n" + " "*8 + "yield 'param1', self.param1" == returned_tokens["yield_params"]

    assert "class_db_field_declerations" in returned_tokens
    assert "\n" + " "*4 + "param1 = Column(Integer, primary_key=True, nullable=True, unique=False)" == \
           returned_tokens["class_db_field_declerations"]

    assert "class_db_field_assignments" in returned_tokens
    assert "\n" + " "*8 + "self.param1 = param1" == returned_tokens["class_db_field_assignments"]

    assert "kword_param_set_group" in returned_tokens
    assert "\n\n" + " "*12 + "if key == 'param1':\n" + " "*16 + "retrieved_object.param1 = value"

    assert "object_params_as_strings" in returned_tokens
    assert " 'param1'," == returned_tokens["object_params_as_strings"]

    assert "data_dict_params" in returned_tokens
    assert "param1" in returned_tokens["data_dict_params"]


    assert "column_type_list" in returned_tokens
