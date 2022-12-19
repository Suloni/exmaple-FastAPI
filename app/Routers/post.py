from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from typing import List,Optional,Dict
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models,schema,oauth2
from ..database import get_db


router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/",response_model=list[schema.PostOut])

def get_posts(db:Session=Depends(get_db),current_user:int= Depends(oauth2.get_current_user),
limit:int=10,skip:int=0,search:Optional[str]=""):
    # print(limit)
    # posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()


    posts=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts
    # posts=db.query(models.Post).filter(models.Post.owner_id==current_user.id).all()

    # print(current_user)
    # print(posts)

    

@router.get("/{id}",response_model=schema.PostOut)
def get_post(id:int,db:Session=Depends(get_db),current_user:int= Depends(oauth2.get_current_user)):
    # post=db.query(models.Post).filter(models.Post.id==id).first()
    # print(post)
    posts=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    # print(current_user)
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id:{id} was not found") 
    return posts


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.Post)
def create_post(post:schema.PostCreate,db:Session=Depends(get_db),current_user:int= Depends(oauth2.get_current_user)):
# If you don't want to write long query
    # new_post=models.Post(title=post.title,content=post.content,published=post.published)

    # print(current_user.email)
    # print(current_user.id)

    # new_post=models.Post(**post.dict())
    new_post=models.Post(owner_id=current_user.id,**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),current_user:int= Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()

    print(current_user.email)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id:{id} does not exists")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorised to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()    
#  return{'message':'post was successfully deleted'}
    return Response(status_code=status.HTTP_204_NO_CONTENT)  

#update post
@router.put("/{id}",response_model=schema.Post)
def update_post(id:int,updated_post:schema.PostCreate,db:Session=Depends(get_db),current_user:int= Depends(oauth2.get_current_user)):

    print(current_user.email)

    post_query=db.query(models.Post).filter(models.Post.id==id)

    post=post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exists")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorised to perform requested action")

    post_query.update(updated_post.dict(),synchronize_session=False)

    db.commit()

    # return{"data":post_query.first()} or
    return post_query.first() 