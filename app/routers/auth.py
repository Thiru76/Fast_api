from fastapi import APIRouter, Body, FastAPI, Depends, Response, status, HTTPException
from passlib.context import CryptContext
from ..pydantic import BaseModel, user_login
from sqlalchemy.orm import Session
from .. import database, pydantic, models
from .. import database
from ..database import get_db, engine
from .. import utils
# from utils import verify

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()

@router.post("/login")
def login(user_credentials:pydantic.user_login, db:Session = Depends(database.get_db)):
    user = db.query(models.user).filter(models.user.email == user_credentials.email).first()
    print(user)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=404, detail="Incorrect password")
    return{"success"}