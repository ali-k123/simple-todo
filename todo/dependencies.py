from .crud import get_user_by_username
from .security import oauth2_scheme, TokenData,SECRET_KEY,ALGORITHM
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from .database import get_db
from sqlalchemy.orm import Session

async def get_user(db : Session = Depends(get_db),token : str = Depends(oauth2_scheme)):
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
    user = get_user_by_username(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user
