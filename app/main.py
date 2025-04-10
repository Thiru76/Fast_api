from random import randrange
from fastapi import Body, FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from app import models
from .database import engine, get_db
from . import pydantic
from sqlalchemy.orm import Session
from typing import List, Optional
from .routers import post, user, auth
from fastapi.middleware.cors import CORSMiddleware



#This is the main file where we are going to write the code for the API

models.Base.metadata.create_all(bind=engine)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

empty_list = [{'title': 'about a man', 'content': 'Thiru is a good boy', 'published': False, 'id': 79},{'title': 'man_1', 'content': 'Thiru is a good boy', 'published': False, 'id': 77}]




@app.get("/posts", response_model=  List[pydantic.response])
def sample(db: Session = Depends(get_db), limit:int = 5, search: Optional[str]  = ""):
    # posts = cursur.execute("Select * from fast_api") #this is the query to get all the data from the table using sql query
    # posts = cursur.fetchall()
    # sample = db.query(models.fast_api)
    # print(sample)
    posts = db.query(models.fast_api).filter(models.fast_api.title.contains).limit(limit).all() #this is the query to get all the data from the table using sql alchemy
    print(posts)
    return posts



def finding_index(id):
    for index, i in enumerate(empty_list):
        if i['id'] == id:
            return index



def find_post(id):
    for i in empty_list:
        print(i)
        if i['id'] == id:
            print(i)
            return i




app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


