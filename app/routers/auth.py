from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.user import User
from app.auth.password import verify_password
from app.auth.jwt import create_access_token
from app.schemas.auth import LoginSchema
from app.schemas.user import ResetPasswordRequest, UserCreate,UserPasswordUpdate
from app.repository.user_repository import UserRepository
from app.api.deps import get_current_user
from app.auth.password import hash_password
import secrets
from app.utils.email import send_email

router = APIRouter(prefix='/api/auth',tags=["Auth"])

@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password,user.password):
        raise HTTPException(status_code=401,detail="Invalid credentials")
    
    token = create_access_token(user.id)
    
    return {"token":token}


@router.post("/register")
def register(data: UserCreate,db: Session = Depends(get_db)):
    user_repo = UserRepository()
    return user_repo.create(data, db)


@router.post("/change-password")
def change_password(data : UserPasswordUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not verify_password(data.old_password, current_user.password):
        raise HTTPException(status_code=400, detail="Old password is incorrect")
    
    current_user.password = hash_password(data.new_password)
    db.commit()
    db.refresh(current_user)
    
    return {"detail":"Password updated successfully"}

@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_password = secrets.token_urlsafe(8)
    user.password = hash_password(new_password)
    db.commit()

    await send_email(
        to=user.email,
        subject="Reset Password",
        body=f"Your new password is: {new_password}"
    )

    return {"message": "New password sent to your email"}