from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from .routers import tasks, auth

from pydantic import BaseModel, Field, EmailStr

class Task(BaseModel):
    id : int
    title : str = Field(min_length = 1, max_length = 16)
    description : str | None =  Field(default = None, max_length = 256)
    owner_id : int
    
    class Config:
        orm_mode = True

class User(BaseModel):
    id: int
    name : str
    username : EmailStr
    tasks: list[Task] = []

    class Config:
        orm_mode = True

class TaskIn(BaseModel):
    title : str = Field(min_length = 1, max_length = 16)
    description : str | None = Field(default = None, max_length = 256)

class TaskOut(BaseModel):
    id : int
    title : str = Field(min_length = 1, max_length = 16)
    description : str | None = Field(default = None, max_length = 256)

class UserIn(BaseModel):
    name : str = Field(min_length = 1, max_length = 32)
    username : EmailStr
    password : str = Field(min_length = 8, max_length = 32)
    password2 : str = Field(min_length = 8, max_length = 32)

from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

def calculate_hash(password:str):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)

def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    #check expire time
    user = user_database.get(token_data.username)
    if user is None:
        raise credentials_exception
    return user
##################

from sqlalchemy.orm import Session

from . import models, types


def get_user_by_username(db: Session, username : str):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: UserIn):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()


def create_user_task(db: Session, task: TaskIn, user_id: int):
    db_task = models.Task(**task.dict(), owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


app = FastAPI()

app.include_router(auth.router)
app.include_router(tasks.router)
