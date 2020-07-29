from builderv2.Parser.Python.Flask.Extractor import extractTokensFromTemplates

def test_noTemplate():
    assert extractTokensFromTemplates("") == set()

def test_simpleTemplate():
    assert extractTokensFromTemplates("<test>") == {"test"}

def test_complexTemplate():
    assert extractTokensFromTemplates("<1> <2> <3> <4>") == {"1", "2", "3", "4"}

def test_NestTemplate():
    assert extractTokensFromTemplates("<<test>>") == {"test"}

    assert extractTokensFromTemplates("<!<test!><>") == set()

def test_number():
    assert extractTokensFromTemplates("<1>") == set("1")

def test_words():
    assert extractTokensFromTemplates("word<words>") == set(["words"])

def test_characters():
    assert extractTokensFromTemplates("<@>") == set()
    assert extractTokensFromTemplates("<*>") == set()

def test_brackets():
    assert extractTokensFromTemplates("<bracket>") == set(["bracket"])
    assert extractTokensFromTemplates("no_bracket") == set()