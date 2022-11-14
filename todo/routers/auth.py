from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas import UserIn
from ..crud import get_user_by_username, create_user
from ..security import Token,create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from passlib.context import CryptContext

router = APIRouter()

@router.post("/signin", response_model=Token)
async def signin(form_data: OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    user = get_user_by_username(db, form_data.username)
    if not user:
        print("SIGN IN : not user")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    pwd_context = CryptContext(schemes=["bcrypt"])
    if not pwd_context.verify(form_data.password,user.hashed_password):
        print("SIGN IN : incorrect password")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/signup")
async def signup(user : UserIn, db : Session = Depends(get_db)):
    u = get_user_by_username(db, user.username)
    if u:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="username exists !",
        )
    if user.password!=user.password2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="passwords dont match !",
        )
    create_user(db, user)
