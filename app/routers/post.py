from random import randrange
import time
from fastapi import APIRouter, Body, FastAPI, Depends
from pydantic import BaseModel
from fastapi import Response, status, HTTPException
import psycopg2
from psycopg2.extras import DictCursor,RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app import models
from .. database import engine, get_db
from .. import pydantic
from sqlalchemy.orm import Session
from .. import oauth2

while True:

    try : 
        conn = psycopg2.connect(host = "localhost", database = "postgres", user="postgres", password="Password", cursor_factory=RealDictCursor)
        cursur = conn.cursor()
        print("connnection established")
        break
    except Exception as e:
        print(e)
        time.sleep(10)


router = APIRouter(
    # prefix="/posts", if we want we can the prefix here and it will be added to the url the endpoind also will be changed
    tags=["posts"]
)

#WE called the class called Post adn saved to variable adn asking them to print and return it will validate for us
@router.post("/create_post", response_model=  pydantic.response)
def create_post(value: pydantic.Post,db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)): # type: ignore
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
    print(user_id)
    create_new_post = models.fast_api(**value.dict()) #this will unpach the dictionary and return the values in the form of key value pair and it is using to create the new post.
    db.add(create_new_post) #this is used to add the new data into the database
    db.commit()
    db.refresh(create_new_post) #this is used to refresh the data in the database means it will update the data in the database
    return create_new_post



@router.get("/get_specific_post/{id}", response_model=  pydantic.response)
def get_specific_post(id : int, response : Response, db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
    print(id)
    # retreived_post = find_post(id)
    # print(type(retreived_post))
    # retreived_post  = cursur.execute(""" SELECT * from fast_api WHERE id = %s  RETURNING * """, (str(id),))    
    # retreived_post = cursur.fetchone()
    print(user_id)
    retreived_post = db.query(models.fast_api).filter(models.fast_api.id == id).first()
    conn.commit()
    if not retreived_post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"this {id} is not found"}
    return retreived_post

@router.delete("/delete_post/{id}")
def delete_post(id : int, db: Session = Depends(get_db), Current_user: int = Depends(oauth2.get_current_user)):
    # print(id)
    # index = finding_index(id)
    deleted_post = db.query(models.fast_api).filter(models.fast_api.id == id)
    # deleted_post = cursur.execute(""" DELETE from fast_api where id = %s  RETURNING * """, (str(id),))
    # deleted_post = cursur.fetchone()
    # conn.commit()

    print(Current_user)
    # print(Current_user.id)
    post = deleted_post.first()
    if deleted_post.first() == None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    
    # if post.user_id != user_id.id:
    #     return Response(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    deleted_post.delete(synchronize_session=False)
    db.commit()
    
    # empty_list.pop(index)
    return {"message": f"this {id} is deleted"}

@router.put("/update_post/{id}", response_model=  pydantic.response)
def update_post(id: int, post_update: pydantic.Post, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    print("this is the update function")
    # index = finding_index(id)
    # print(index)
    # cursur.execute(""" UPDATE fast_api SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post_update.title, post_update.content, post_update.published, str(id),))
    # conn.commit()
    # updated_post = cursur.fetchone()
    print(user_id)
    updated_post = db.query(models.fast_api).filter(models.fast_api.id == id)

    post = updated_post.first()
    if post == None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    
    if post.user_id != oauth2.get_current_user.id:
        return Response(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    # if index == None:
    #     return Response(status_code=status.HTTP_404_NOT_FOUND, detail ="The given {id} is not available")
    

    # post_dict['id'] = id
    # empty_list[index] = post_dict 
    updated_post.update(post_update.model_dump(), synchronize_session=False)
    db.commit()
    
    return  updated_post.first()
