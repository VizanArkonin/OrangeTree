"""
Database module initialization
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from server.config import DATABASE_CONFIG

engine = create_engine(DATABASE_CONFIG["connection_string"], convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=DATABASE_CONFIG["autocommit"],
                                         autoflush=DATABASE_CONFIG["autoflush"],
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

"""
import all modules here that might define models so that they will be registered properly on the metadata.  
Otherwise you will have to import them first before calling create_all.
"""
import server.database.models

Base.metadata.create_all(bind=engine)
