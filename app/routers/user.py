import time
from fastapi import APIRouter, Body, FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from app import models
from .. database import engine, get_db
from .. import pydantic
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext


router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/create_user", response_model = pydantic.user_response)
def create_user(user: pydantic.user_create, db : Session = Depends(get_db)):

    #creating hash password
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password

    new_user = models.user(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user