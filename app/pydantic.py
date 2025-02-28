#This is the model from pydantic which helps ue to validate the input what user is providing
from psycopg2 import Timestamp
from pydantic import BaseModel, EmailStr
from email_validator import validate_email, EmailNotValidError
from datetime import datetime


class Post(BaseModel): 
    title : str
    content : str
    published : bool = True
    id : int

class response(Post):
    title : str
    content : str
    # created_time : str

    class Config:
        orm_mode = True

class user_create(BaseModel):
    email : EmailStr
    id : int
    name : str
    password : str


    

class user_response(BaseModel):
    email : EmailStr
    id : int
    name : str
    created_time : datetime

    class Config:
        orm_mode = True