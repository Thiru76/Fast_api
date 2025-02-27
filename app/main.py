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
from app import models
from .database import engine, get_db
from . import pydantic
from sqlalchemy.orm import Session


#This is the main file where we are going to write the code for the API

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

empty_list = [{'title': 'about a man', 'content': 'Thiru is a good boy', 'published': False, 'id': 79},{'title': 'man_1', 'content': 'Thiru is a good boy', 'published': False, 'id': 77}]




@app.get("/posts", status_code = status.HTTP_200_OK)
def sample(db: Session = Depends(get_db)):
    # posts = cursur.execute("Select * from fast_api") #this is the query to get all the data from the table using sql query
    # posts = cursur.fetchall()
    sample = db.query(models.fast_api)
    print(sample)
    posts = db.query(models.fast_api).all() #this is the query to get all the data from the table using sql alchemy
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




#WE called the class called Post adn saved to variable adn asking them to print and return it will validate for us
@app.post("/create_post", response_model=  pydantic.response)
def create_post(value: pydantic.Post,db: Session = Depends(get_db)): # type: ignore
    print(value)
    # print(value.content)
    # value = value.dict()
    # value['id']= randrange(0, 100000)
    # output = empty_list.append(value)
    # print(output)
    # cursur.execute(""" INSERT INTO fast_api (title, content, published, id) VALUES (%s, %s, %s, %s) RETURNING * """,(value.title, value.content, value.published, value.id))    #this is the query to insert the data into the table using sql query
    
    # output = cursur.fetchall()
    # conn.commit()
    # posts = cursur.fetchall()
    # create_new_post = models.fast_api(title= value.title, content = value.content, published = value.published, id = value.id) #this is working fine.
    
    create_new_post = models.fast_api(**value.dict()) #this will unpach the dictionary and return the values in the form of key value pair and it is using to create the new post.
    db.add(create_new_post) #this is used to add the new data into the database
    db.commit()
    db.refresh(create_new_post) #this is used to refresh the data in the database means it will update the data in the database
    return create_new_post

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
def get_specific_post(id : int, response : Response, db: Session = Depends(get_db)):
    print(id)
    # retreived_post = find_post(id)
    # print(type(retreived_post))
    # retreived_post  = cursur.execute(""" SELECT * from fast_api WHERE id = %s  RETURNING * """, (str(id),))    
    # retreived_post = cursur.fetchone()
    retreived_post = db.query(models.fast_api).filter(models.fast_api.id == id).first()
    conn.commit()
    if not retreived_post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"this {id} is not found"}
    return retreived_post

@app.delete("/delete_post/{id}")
def delete_post(id : int, db: Session = Depends(get_db)):
    print(id)
    index = finding_index(id)
    deleted_post = db.query(models.fast_api).filter(models.fast_api.id == id)
    # deleted_post = cursur.execute(""" DELETE from fast_api where id = %s  RETURNING * """, (str(id),))
    # deleted_post = cursur.fetchone()
    # conn.commit()
    if deleted_post.first() == None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    
    deleted_post.delete(synchronize_session=False)
    db.commit()
    
    # empty_list.pop(index)
    return deleted_post

@app.put("/update_post/{id}")
def update_post(id: int, post_update: pydantic.Post, db: Session = Depends(get_db)):
    print("this is the update function")
    index = finding_index(id)
    print(index)
    # cursur.execute(""" UPDATE fast_api SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post_update.title, post_update.content, post_update.published, str(id),))
    # conn.commit()
    # updated_post = cursur.fetchone()
    updated_post = db.query(models.fast_api).filter(models.fast_api.id == id)

    post = updated_post.first()
    if post == None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    # if index == None:
    #     return Response(status_code=status.HTTP_404_NOT_FOUND, detail ="The given {id} is not available")
    

    # post_dict['id'] = id
    # empty_list[index] = post_dict 
    updated_post.update(post_update.model_dump(), synchronize_session=False)
    db.commit()
    
    return {'msg': updated_post.first()}


