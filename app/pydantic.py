#This is the model from pydantic which helps ue to validate the input what user is providing
from psycopg2 import Timestamp
from pydantic import BaseModel


class Post(BaseModel): 
    title : str
    content : str
    published : bool = True
    id : int

class response(BaseModel):
    title : str
    content : str
    # created_time : str

    class Config:
        orm_mode = True