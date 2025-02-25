from random import randrange
import time
from fastapi import Body, FastAPI, Depends
from pydantic import BaseModel
from fastapi import Response, status, HTTPException
import psycopg2
from psycopg2.extras import DictCursor,RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

#This is the main file where we are going to write the code for the API

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

empty_list = [{'title': 'about a man', 'content': 'Thiru is a good boy', 'published': False, 'id': 79},{'title': 'man_1', 'content': 'Thiru is a good boy', 'published': False, 'id': 77}]
#This is the model from pydantic which helps ue to validate the input what user is providing
class Post(BaseModel): 
    title : str
    content : str
    published : bool = True
    id : int

@app.get("/posts", status_code = status.HTTP_200_OK)
def sample():
    posts = cursur.execute("Select * from fast_api")
    posts = cursur.fetchall()
    print(posts)
    return posts

while True:

    try : 
        conn = psycopg2.connect(host = "localhost", database = "postgres", user="postgres", password="Password", cursor_factory=RealDictCursor)
        cursur = conn.cursor()
        print("connnection established")
        break
    except Exception as e:
        print(e)
        time.sleep(10)


@app.get("/sql_alchemy_table")
def create_post(value: Post, db: Session = Depends(get_db)):
    print(value)
    return {"message": "this is the sql alchemy table"}
    


#WE called the class called Post adn saved to variable adn asking them to print and return it will validate for us
@app.post("/create_post")
def create_post(value: Post): # type: ignore
    print(value)
    # print(value.content)
    # value = value.dict()
    # value['id']= randrange(0, 100000)
    # output = empty_list.append(value)
    # print(output)
    cursur.execute(""" INSERT INTO fast_api (title, content, published, id) VALUES (%s, %s, %s, %s) RETURNING * """,(value.title, value.content, value.published, value.id))    
    
    # output = cursur.fetchall()
    conn.commit()
    posts = cursur.fetchall()
    return(posts)

def find_post(id):
    for i in empty_list:
        print(i)
        if i['id'] == id:
            print(i)
            return i


def finding_index(id):
    for index, i in enumerate(empty_list):
        if i['id'] == id:
            return index



@app.get("/get_specific_post/{id}")
def get_specific_post(id : int, response : Response):
    print(id)
    # retreived_post = find_post(id)
    # print(type(retreived_post))
    retreived_post  = cursur.execute(""" SELECT * from fast_api WHERE id = %s  RETURNING * """, (str(id),))    
    retreived_post = cursur.fetchone()
    conn.commit()
    if not retreived_post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"this {id} is not found"}
    return retreived_post

@app.delete("/delete_post/{id}")
def delete_post(id : int):
    print(id)
    index = finding_index(id)
    deleted_post = cursur.execute(""" DELETE from fast_api where id = %s  RETURNING * """, (str(id),))
    deleted_post = cursur.fetchone()
    conn.commit()
    if index == None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    
    # empty_list.pop(index)
    return deleted_post

@app.put("/update_post/{id}")
def update_post(id: int, update_post : Post):
    print("this is the update function")
    index = finding_index(id)
    print(index)
    cursur.execute(""" UPDATE fast_api SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (update_post.title, update_post.content, update_post.published, str(id),))
    conn.commit()
    updated_post = cursur.fetchone()
    # if index == None:
    #     return Response(status_code=status.HTTP_404_NOT_FOUND, detail ="The given {id} is not available")
    

    # post_dict = update_post.dict()
    # post_dict['id'] = id
    # empty_list[index] = post_dict 
    return updated_post