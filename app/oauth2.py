from jose import JWTError,jwt
from datetime import datetime,timedelta
from .import schema, database,models
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme= OAuth2PasswordBearer(tokenUrl='/login')

# secert_key
# Algorithm
# Expression_time

# Secret_Key="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
Secret_Key= settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data:dict):
    to_encode =data.copy()

    expire=datetime.utcnow()+ timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt=jwt.encode(to_encode,Secret_Key,algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token:str,credentials_expection):
    try:

        payload= jwt.decode(token,Secret_Key,algorithms=[ALGORITHM])
        id: str=payload.get("user_id")
        if id is None:
            raise credentials_expection
        token_data=schema.TokenData(id=id)

    except JWTError:
        raise credentials_expection
    # except JWTError as e:

        # print(e)
        

    return token_data

def get_current_user(token:str= Depends(oauth2_scheme),db:Session=Depends(database.get_db)):
    credentials_expection=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Could not validate credentials",
    headers={"WWW-Authentication":"Bearer"})
    
    # return verify_access_token(token,credentials_expection)
    token=verify_access_token(token,credentials_expection)

    user=db.query(models.User).filter(models.User.id==token.id).first()

    return user 
   