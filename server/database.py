from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 

#Database URL
URL_DATABASE='sqlite:///./chatbot.db'

# Create engine and tables
engine = create_engine(URL_DATABASE,connect_args = {"check_same_thread": False}) # can use postgres/mysql/mongodb etc for production

# Create a db session
SessionLocal = sessionmaker(bind=engine,autoflush=False,autocommit=False)

#Base class
Base = declarative_base()

