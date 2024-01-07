from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

database_url = "mysql+pymysql://root:@localhost/uas_py"

engine = create_engine(database_url)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()