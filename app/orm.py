from array import array
from ast import Delete, While
from genericpath import exists
from logging import raiseExceptions
from operator import index
from optparse import Option
from sqlite3 import Cursor
from turtle import title
from typing import Optional,List
from urllib import response
from fastapi.params import Body
from fastapi import FastAPI,Response,status,HTTPException,Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy import Session
from . import models,schema,utils
from .database import engine,get_db
from .Routers import post,user,auth,votes
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


print(settings.database_username)

models.Base.metadata.create_all(bind=engine)

#path operation/route operation, get, put, post is http method; (/) is route path

app = FastAPI()
origins=["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)
#pydantic model,its refere to schema,it has been reference to our path operation.schema/pydantic model define the structure of request & response.

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get("/")
def read_posts():
        return{"msg":"Welcome"}


# #for orm
# to creat the table
# @app.get("/sqlalchemy")
# def test_posts(db:Session=Depends(get_db)):

#     posts=db.query(models.Post).all()
#     print(posts)
#     return{"data":posts}
# for ORM it will give you sql query try it to run
    # posts=db.query(models.Post) 
    # print(posts)
    # return{"data":"Successfull"}


# my_post=[{"title":"title of post 1","content":"content of post 1","id":1},{"title":"favorite foof","content":"I like Pizza","id":2}]

# def find_post(id):
#     for p in my_post:
#         if p[id]==id:
#             return p

# def find_index_post(id):
#     for i,p in enumerate(my_post):
#         if p[id]==id:
#             return p

# pip install -r requirement.txt