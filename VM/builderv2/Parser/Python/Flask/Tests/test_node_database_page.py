from builderv2.Parser.Python.Flask.Builder import NodeDatabaseRoot

# Common Variables
empty_tokens = dict()
empty_node_database_page = NodeDatabaseRoot(empty_tokens)

MODIFIED_NODE_DATABASE_PAGE = \
'''
const {Sequelize} = require('sequelize');

const db = new Sequelize({
    dialect: 'sqlite',
    storage: './tmp/DATABASE_1.db'
});

const initDB = async () =>{
    try{
        await db.authenticate();
        console.log('Connection worked')
    }catch(err){
        console.log('Error! ', err)
    }
}

module.exports = {db, initDB}
  
'''
# Testing the constructor

def test_makeEmptyNodeDatabasePageConstructor():
    p1 = empty_node_database_page

    assert p1.token_dict == None
    assert p1.name == "database.js"


def test_makeSimpleNodeDatabasePageConstructor():
    test_dict = {"test": "test"}
    p1 = NodeDatabaseRoot(test_dict)

    assert p1.token_dict == test_dict
    assert p1.name == "database.js"

# Testing Create Page

def test_createEmptyNodeDatabasePage():
    p1 = NodeDatabaseRoot({'rand': "1"})

    full_page = p1.createPage()
    assert "".join(full_page.split()) == "".join(MODIFIED_NODE_DATABASE_PAGE.split())
