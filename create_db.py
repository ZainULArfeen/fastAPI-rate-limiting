from database import Base, engine
from models import Item

print("Creating Database ...")

Base.metadata.create_all(engine)