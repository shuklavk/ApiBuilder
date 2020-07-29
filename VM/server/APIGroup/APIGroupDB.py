from sqlalchemy import Column, Integer, String, Boolean
from server import Base, db_session
from random import randint
from server.User.UserDB import isValidUser

class APIGroup(Base):
    __tablename__ = "api_groups"
    params = ['userId', 'apiName']

    id = Column(Integer, primary_key=True)
    userId = Column(Integer, nullable=False)
    name = Column(String(64), nullable=False)


    def __init__(self, userId, name):
        self.userId = userId
        self.name = name

        self.id = randint(0, 10000)

def isValidAPIGroup(groupId):
    try:
        return APIGroup.query.filter(APIGroup.id == groupId).one_or_none() is not None
    except Exception:
        return False

def addAPI(userId, apiGroup):
    if isValidUser(userId):
        db_session.add(apiGroup)
        db_session.commit()

def updateAPI(userId, apiGroup):
    if isValidUser(userId):
        api_row = APIGroup.query.filter(APIGroup.userId == userId).one_or_none()
        api_row.name = apiGroup.name
        db_session.commit()

def getUserAPIs(userId):
    if not isValidUser(userId):
        return []

    return APIGroup.query.filter(APIGroup.userId == userId).all()

def getCurrentAPI(userId):
    if not isValidUser(userId):
        return []

    return APIGroup.query.filter(APIGroup.userId == userId).first()



