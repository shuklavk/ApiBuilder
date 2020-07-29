from builderv2.Parser.Python.Flask.Insertor import insertTokensIntoTemplate


def test_noTokens_noTemplate():
    output = insertTokensIntoTemplate("")
    assert output == ""

    output = insertTokensIntoTemplate("test")
    assert output == "test"

some_tokens = {
    "one"   : "1",
    "two"   : "2",
    "three" : "3"
}

def test_someTokens_noTemplate():
    output = insertTokensIntoTemplate("", **some_tokens)
    assert output == ""

    output = insertTokensIntoTemplate("test", **some_tokens)
    assert output == "test"

def test_noToken_simpleTemplate():
    try:
        insertTokensIntoTemplate("<test>")

        # You should not have reached here.
        assert False
    except ValueError:
        # This was the right result. Continue on
        pass

def test_simpleTokens_simpleTemplate():
    assert insertTokensIntoTemplate("<one> + <two> + <three> = 6", **some_tokens) == "1 + 2 + 3 = 6"

    assert insertTokensIntoTemplate("<<one>> + <<two>> + <<three>> = [6]", **some_tokens) == \
           "<1> + <2> + <3> = [6]"