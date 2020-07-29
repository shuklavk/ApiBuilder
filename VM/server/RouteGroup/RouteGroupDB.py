from sqlalchemy import Column, Integer, String, Boolean
from server import Base, db_session
from random import randint
from server.User.UserDB import isValidUser
from onAppRunConfig.logConfig import generalLogger

class RouteGroup(Base):
    __tablename__ = "route_groups"
    params = ['userId', 'objectName', 'apiId', 'isCRUD', 'isReadMultiple', 'isSingleRoute']

    id = Column(Integer, primary_key=True)
    userId = Column(Integer, nullable=False)
    objectName = Column(String(64), nullable=False)
    apiId = Column(Integer, nullable=False)
    isCRUD = Column(Boolean, nullable=False)
    isReadMultiple = Column(Boolean, nullable=False)
    isSingleRoute = Column(Boolean, nullable=False)

    def __init__(self, userId, name, apiId, isCrud, isReadMultiple, isReadAllObjects, isSingleRoute):
        self.userId = userId
        self.objectName = name
        self.apiId = apiId
        self.isCRUD = isCrud
        self.isReadMultiple = isReadMultiple
        self.isReadAllObjects = isReadAllObjects
        self.isSingleRoute = isSingleRoute

        self.id = randint(0, 10000)

    def __iter__(self):
        for param in self.params:
            yield param, getattr(self, param)

    def __getitem__(self, item=None):
        obj_to_dict = dict(self)
        if item in obj_to_dict:
            return obj_to_dict[item]
        return None


def isValidRouteGroup(groupId):
    try:
        return RouteGroup.query.filter(RouteGroup.id == groupId).one_or_none() is not None
    except Exception:
        return False

def isValidRoute(routeName):
    try:
        return RouteGroup.query(User.userId).filter(RouteGroup.objectName == routeName).one() is None
    except Exception:
        return False

def addRoute(userId, routeGroup):
    if isValidUser(userId):
        # if isValidRoute(routeGroup.objectName):
        #     print ('in error', routeGroup.objectName)
        #     generalLogger.error("Error: RouteGroup '" + routeGroup.objectName + "' already added to userID '" + str(userId) + "'")
        #     return
        # print('IN DB', routeGroup)
        db_session.add(routeGroup)
        db_session.commit()
        generalLogger.info("RouteGroup '" + routeGroup.objectName + "' added to userID '" + str(userId) + "'")

def getRoute(userId, queries):
    if not isValidUser(userId):
        return None
    attr = val = ""
    try:
        filter_list = []
        for attr, val in queries.items():
            filter_list.append(getattr(RouteGroup, attr) == str(val))
        route_list = RouteGroup.query.filter(*filter_list).all()
        return route_list if len(route_list) > 1 else route_list[0]
    except Exception as e:
        print("An exception occurred with the following details:\n{}".format(str(e)))
        print("Attribute: {}\tValue: {}\n".format(attr, val))
        return None


def updateRoute(userID, routeId, dict):
    try:
        originalRouteGroup = getRoute(userID, {'id':routeId})
        for routeGroupParam in dict:
            setattr(originalRouteGroup, routeGroupParam,dict[routeGroupParam])
            db_session.commit()
        return True
    except Exception:
        return False


def deleteRoute(userId, routeId):
    routeGroup = getRoute(userId, {'id':routeId})
    if routeGroup:
        db_session.delete(routeGroup)
        db_session.commit()


def getUserRoutes(userId):
    if not isValidUser(userId):
        return []
    return RouteGroup.query.filter(RouteGroup.userId == userId).all()
