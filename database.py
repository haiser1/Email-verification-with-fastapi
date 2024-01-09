from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
load_dotenv()

db_user = os.getenv('DB_USER')
db_passowrd = os.getenv('DB_PASSWORD')

database_url = f"mysql+pymysql://{db_user}:{db_passowrd}@localhost/uas_py"

engine = create_engine(database_url)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()