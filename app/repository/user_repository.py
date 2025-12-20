from fastapi import Depends,HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate,UserApi, UserUpdate
from app.models.user import User
from app.api.deps import get_current_user, get_db
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
        return UserApi(
            id=new_user.id,
            first_name=new_user.first_name,
            last_name=new_user.last_name,
            email=new_user.email
        )

    def updateUser(self, user_update: UserUpdate, db: Session, current_user: User):
        if user_update.first_name is not None:
            current_user.first_name = user_update.first_name

        if user_update.last_name is not None:
            current_user.last_name = user_update.last_name

        if user_update.email is not None:
            current_user.email = user_update.email

        db.commit()
        db.refresh(current_user)
        return UserApi(
            id=current_user.id,
            first_name=current_user.first_name,
            last_name=current_user.last_name,
            email=current_user.email
        )
    
