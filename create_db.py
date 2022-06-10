from database import Base, engine
from models import Item

print("Creating Database ...")

#initialize the database
Base.metadata.create_all(engine)