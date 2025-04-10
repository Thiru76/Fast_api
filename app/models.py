import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from app.database import Base

Base = declarative_base()

class Post(Base):
    __tablename__ = "fast_api_orm"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)


#this class is used to create the table in the database and also return the data from the database whatever the column we have mentioned here will return that columns only.
class fast_api(Base):
    __tablename__ = "fast_api"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    user_id = Column(Integer, ForeignKey("user_table.id", on_delete="CASCADE"),nullable=False)
    owner = relationship("user")



class user(Base):
    __tablename__ = "user_table"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    # created_time = Column(TIMESTAMP, server_default='True', nullable=False)
    created_time = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

