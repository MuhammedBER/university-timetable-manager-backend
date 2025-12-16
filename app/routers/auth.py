from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.user import User
from app.auth.password import verify_password
from app.auth.jwt import create_access_token
from app.schemas.auth import LoginSchema
from app.schemas.user import UserCreate
from app.repository.user_repository import UserRepository

router = APIRouter(prefix='/auth',tags=["Auth"])

@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password,user.password):
        raise HTTPException(status_code=401,detail="Invalid credentials")
    
    token = create_access_token(user.id)
    
    return {"access_token":token,"token_type":"bearer"}



@router.post("/register")
async def register(data: UserCreate,db: Session = Depends(get_db)):
    user_repo = UserRepository()
    return user_repo.create(data, db)