from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os


parent_directory = (os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))))

if not os.path.exists(os.path.abspath(parent_directory + '/tmp')):
    os.makedirs(parent_directory + '/tmp')

engine = create_engine('sqlite:///tmp/test.db'.format(dir=parent_directory), convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import server.User.UserDB
    import server.RouteGroup.RouteGroupDB
    import server.APIGroup.APIGroupDB
    import server.ObjectAttributes.ObjectAttributesDB
    Base.metadata.create_all(bind=engine)
