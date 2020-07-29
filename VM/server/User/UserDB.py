from sqlalchemy import Column, Integer
from server import Base, db_session
from random import randint

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)

    def __init__(self):
        self.id = randint(0, 10000)


def isValidUser(userId):
    try:
        return User.query.filter(User.id==userId).one_or_none() is not None
    except Exception:
        return False

def addUser(user):
    if not isValidUser(user.id):
        db_session.add(user)
        db_session.commit()
        return True
    return False

def retrieveUser(userId):
    if isValidUser(userId):
        return User.query.filter(User.id==userId).one()
    return None

def gimmeNewUser():
    user = User()
    while not addUser(user):
        # keep generating users until you get a valid one
        user = User()
    return user