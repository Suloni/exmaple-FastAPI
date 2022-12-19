from array import array
from ast import Delete, While
from genericpath import exists
from logging import raiseExceptions
from operator import index
from optparse import Option
from sqlite3 import Cursor
from turtle import title
from typing import Optional
from urllib import response
from fastapi.params import Body
from fastapi import FastAPI,Response,status,HTTPException,Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

#path operation/route operation, get, put, post is http method; (/) is route path

app = FastAPI()


class Post(BaseModel):
    id: int
    title:str
    content:str
    published:bool=True



try:
        conn =psycopg2.connect(host='localhost',database='FastAPI',user='postgres',
                                                password='Aditya', cursor_factory=RealDictCursor)
        Cursor = conn.cursor()
        print("Database connection was successful")
except Exception as error:
        print("Connecting to database failed")
        print("Error:",error)
        time.sleep(2)

@app.get("/ss")
def read_posts():
        return{"msg":"Welcome"}

@app.get("/posts")
def get_posts():
    Cursor.execute("""Select * from posts """)
    posts=Cursor.fetchall()
    print(posts)
    return {"data":posts}
    

@app.get("/posts/{id}")
def get_post(id:int):
    Cursor.execute("""Select * from posts where id= %s""",(str(id),))
    post=Cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id:{id} was not found") 
    return {"post_detail":post}



@app.post("/post")
def create_post(post:Post):
    Cursor.execute("""INSERT INTO posts (id, title, content) VALUES (%s, %s,%s) RETURNING * """,(post.id, post.title,post.content))
    new_post=Cursor.fetchone()
    conn.commit()
    return{"data":"successful"}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    Cursor.execute("""Delete from posts where id= %s returning *""",(str(id),))
    Deleted_post=Cursor.fetchone()
    conn.commit()
    if Deleted_post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exists")
    return{'message':'post was successfully deleted'}
    # return Response(status_code=status.HTTP_204_NO_CONTENT)  
#update post
@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    Cursor.execute("""UPDATE posts SET id=%s, title=%s, content=%s Where id= %s Returning * """,(post.id, post.title,post.content,str(id),))
    updated_post=Cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exists")
    
    return{'Message':'post successfully updated'}
    