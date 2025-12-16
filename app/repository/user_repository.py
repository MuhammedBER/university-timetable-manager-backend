from fastapi import Depends,HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.models.user import User
from app.api.deps import get_db
from app.auth.password import hash_password


class UserRepository:
    def create(self, data : UserCreate, db: Session):
        existing_user = db.query(User).filter(User.email == data.email).first()
        if existing_user:
            raise HTTPException(status_code=400,detail="Email already registered")
        
        new_user = User(
            first_name = data.first_name,
            last_name = data.last_name,
            email = data.email,
            password = hash_password(data.password)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
        
    
