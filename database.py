from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


#engine’s job is to transform python objects and sqlalchemy functions into 
# SQL code that can be interpreted by the database
engine = create_engine("postgresql://zainularfeen:zainularfeen@localhost/newitems_db",
    echo = True
)#database url

#constructs a base class for declarative class definations
Base = declarative_base()

#database session
SessionLocal = sessionmaker(bind = engine)