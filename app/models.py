from datetime import timezone
from .database import Base
from sqlalchemy import Column, Integer, String,Boolean,ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

# Create "SQLAlchemy models" from the Base class
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True,nullable =False)
    title = Column(String, unique=True, nullable=False)
    content = Column(String,nullable=False)
    published=Column(Boolean,server_default='True',nullable=False)
    created_at=Column(TIMESTAMP(timezone==True), 
                    nullable=False,server_default=text('now()'))
    owner_id=Column(Integer,ForeignKey("users.id",ondelete="Cascade"),nullable=False)
    owner=relationship("User")
    uselist=False
    
    

# helps to user can create login account

class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True,nullable =False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone==True), nullable=False,server_default=text('now()'))
    phone_number = Column(String)

class Vote(Base):
    __tablename__="votes"
    user_id=Column(Integer,ForeignKey("users.id",ondelete="Cascade"),primary_key=True) 
    post_id=Column(Integer,ForeignKey("posts.id",ondelete="Cascade"),primary_key=True)
    


