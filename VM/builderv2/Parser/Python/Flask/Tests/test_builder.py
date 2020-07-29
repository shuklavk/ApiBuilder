from builderv2.Parser.Python.Flask.Builder import Builder, Page


# All the builder tests for the constructor
def test_builderConstructor_empty():
     b1 = Builder([])

     assert b1.pages == []
     assert b1.outputName == "Test"
     assert b1.drop_location == "drop/Test"

def test_builderContstructor_pages():
    p1 = Page([], dict(), "")
    b1 = Builder([p1])

    assert b1.pages == [p1]
    assert b1.outputName == "Test"
    assert b1.drop_location == "drop/Test"

def test_builderConstructor_name():
    b1 = Builder([], "output")

    assert b1.pages == []
    assert b1.outputName == "output"
    assert b1.drop_location == "drop/output"

def test_builderConstructor_pagesName():
    p1 = Page([], dict(), "")
    b1 = Builder([p1], "output")

    assert b1.pages == [p1]
    assert b1.outputName == "output"
    assert b1.drop_location == "drop/output"


# All the builder tests for extract functions
def test_extractAllPageTokens_empty():
    b1 = Builder([])
    assert b1.extractAllPageTokens() == set()

def test_extractAllPageTokens_filled_emptyPages():
    p1 = Page([], dict(), "")
    p2 = Page([], dict(), "")
    p3 = Page([], dict(), "")

    b1 = Builder([p1, p2, p3], "test")

    assert b1.extractAllPageTokens() == set()

def test_extractAllPageTokens_filled_filledPages():
    p1 = Page(["<one>"], {"one": "1"}, "p1")
    p2 = Page(["<two>"], {"two": "2"}, "p2")
    p3 = Page(["<three>"], {"three":"3"}, "p3")

    b1 = Builder([p1, p2, p3], "test")

    assert b1.extractAllPageTokens() == {"one", "two", "three"}

def test_extractAllPageTokens_duplication():
    p1 = Page(["<one>"], dict(), "p1")
    p2 = Page(["<one>"], dict(), "p2")
    p3 = Page(["two"], dict(), "p3")

    b1 = Builder([p1, p2, p3], "test")

    assert b1.extractAllPageTokens() == {"one"}

# All the builder tests for inserting tokens
def test_insertTokens_empty():
    pass
