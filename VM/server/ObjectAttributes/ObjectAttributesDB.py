from sqlalchemy import Column, Integer, String, Boolean
from server import Base, db_session
from random import randint
from server.User.UserDB import isValidUser
from server.RouteGroup.RouteGroupDB import RouteGroup, isValidRouteGroup

class ObjectAttributes(Base):
    __tablename__ = "object_attributes"

    # Used to validate jsons containing entries for this object
    # map init params to json strings names that will be sent
    params = ['name', 'type', 'description', 'isUnique', 'isEncrypted', 'generationMethod', 'isNullable']

    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer, nullable=False)
    objectId = Column(Integer, nullable=False)
    name = Column(String(64), nullable=False)
    type = Column(String(64), nullable=False)
    description = Column(String(512), nullable=False)
    isUnique = Column(Boolean, nullable=False)
    isEncrypted = Column(Boolean, nullable=False)
    isNullable = Column(Boolean, nullable=False)
    generationMethod = Column(String(64), nullable=False)

    def __init__(self, userId, objectId, name, objType, description, isUnique, isEncrypted, isNullable,
                 generationMethod):
        self.userId = int(userId)
        self.objectId = int(objectId)
        self.name = str(name)
        self.type = str(objType)
        self.description = str(description)
        self.isUnique = isUnique
        self.isEncrypted = isEncrypted
        self.isNullable = isNullable
        self.generationMethod = str(generationMethod)

    def __iter__(self):
        for param in self.params:
            yield param, getattr(self, param)

    def __getitem__(self, item=None):
        obj_to_dict = dict(self)
        if item in obj_to_dict:
            return obj_to_dict[item]
        return None


def isValidAttribute(attributeName, routeGroupId, userId):
    try:
        allAttrs = retrieveObjectAttributes(userId, routeGroupId)
        for attrs in allAttrs:
            if attrs.name == attributeName:
                return True
        return False
    except Exception:
        return False


def addObjectAttributes(userId, groupId, objectAttributes):
    if ObjectAttributes.query.filter(ObjectAttributes.objectId == groupId).filter(ObjectAttributes.name == objectAttributes.name).first():
        print("This attribute already exists!")
        return
    if isValidUser(userId) and isValidRouteGroup(groupId):
        db_session.add(objectAttributes)
        db_session.commit()

def getSingleObjectAttribute(userId, attributeId):
    if not isValidUser(userId):
        return None
 
    try:
        return ObjectAttributes.query.filter(ObjectAttributes.id == attributeId).one_or_none()
    except Exception:
        return None

def retrieveObjectAttributes(userId, groupId):
    if not isValidUser(userId) or not isValidRouteGroup(groupId):
        return []

    return ObjectAttributes.query.filter(ObjectAttributes.userId == userId).\
        filter(ObjectAttributes.objectId == groupId).all()

def updateObjectAttributes(userId, attributeId, attrDict):
    try:
        originalObjectAttribute = getSingleObjectAttribute(userId, attributeId)
        for objectAttributeParam in attrDict:
            setattr(originalObjectAttribute, objectAttributeParam, attrDict[objectAttributeParam])
            db_session.commit()
        return True
    except Exception:
        return False

def deleteObjectAttributes(userId, attributeId):
    objectAttribute = getSingleObjectAttribute(userId, int(attributeId))
    if objectAttribute:
        db_session.delete(objectAttribute)
        db_session.commit()