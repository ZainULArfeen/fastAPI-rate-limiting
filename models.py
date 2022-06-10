from email.policy import default
from enum import unique
from database import Base
from sqlalchemy import String, Boolean, Integer, Column, Text


#iItem class inhertis from base, each instance of our Item class will correspond to a row in the 'items' table.
class Item(Base):
    #set the name of the table in database
    __tablename__ = 'items'

    id = Column(Integer, primary_key = True)
    name = Column(String(255), nullable = False, unique = True)
    description = Column(Text)
    price = Column(Integer, nullable = False)

    
    def __repr__(self):
        return f"<Item name = {self.name} price={self.price}>"

