from fastapi import FastAPI, Depends, status, HTTPException
from pydantic import BaseModel
from slowapi import Limiter
from database import SessionLocal
from typing import List, Optional
import models

from starlette.requests import Request

from starlette.applications import Starlette
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

#add a pydantic model, defining the acceptable input fromat.
class Item(BaseModel):
    id : int
    name : str
    description : str
    price : int

    class Config:
        orm_mode = True

    


#db instance
db = SessionLocal()

@app.get('/home')
@limiter.limit("300/minute")
async def homepage(request: Request):
    return {"WORKINGGGG"}


@app.get('/items', response_model= List[Item], status_code=200)
@limiter.limit("5/minute")
async def list_items(request : Request):
    """
    get all the items
    """
    items = db.query(models.Item).all()

    return items



@app.post('/items', response_model= Item, status_code = status.HTTP_201_CREATED)
def create_item(item : Item):
    """
    create an item and add it into the database
    """
    new_item = models.Item(
        name = item.name,
        price = item.price,
        description = item.description,
        
    )

    db_item=db.query(models.Item).filter(models.Item.name==item.name).first()

    if db_item is not None:
        raise HTTPException(status_code=400,detail="Item already exists")

    db.add(new_item)
    db.commit()

    return new_item

@app.put('/item/{item_id}',response_model=Item,status_code=status.HTTP_200_OK)
def update_an_item(item_id:int,item:Item):
    """
    updating an item and commiting
    """
    item_to_update=db.query(models.Item).filter(models.Item.id==item_id).first()
    item_to_update.name=item.name
    item_to_update.price=item.price
    item_to_update.description=item.description

    db.commit()

    return item_to_update

@app.delete('/item/{item_id}')
def delete_item(item_id:int):
    item_to_delete=db.query(models.Item).filter(models.Item.id==item_id).first()

    if item_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Resource Not Found")
    
    db.delete(item_to_delete)
    db.commit()

    return item_to_delete
