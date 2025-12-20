import os
from app.database.db import SessionLocal
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.models.user import User
from dotenv import load_dotenv
from app.schemas.user import UserApi

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
)->UserApi:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload["sub"])
        print(payload)
    except JWTError:
        raise HTTPException(status_code=401, detail=token)

    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return UserApi(id=user.id,last_name=user.last_name,first_name=user.first_name,email=user.email)


def get_current_user_id(request: Request) -> int:
    """
    Extract user_id from request state (set by AuthMiddleware).
    Use this dependency when you only need the user_id, not the full user object.
    """
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")
    return user_id