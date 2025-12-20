from fastapi import APIRouter, Depends
from requests import Session
from app.api.deps import get_current_user, get_db
from app.schemas.user import UserUpdate, UserBase, UserApi
from app.models.user import User
from app.repository.user_repository import UserRepository

router = APIRouter(prefix='/api',tags=["User"])

@router.get("/user")
def getUser(current_user = Depends(get_current_user)):
    return UserApi(
        id=current_user.id,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        email=current_user.email
    )

@router.put("/user")
def update(user_update: UserUpdate,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    user_repo = UserRepository()
    return user_repo.updateUser(user_update, db, current_user) 
    
@router.delete("/user")
def deleteUser(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db.delete(current_user)
    db.commit()
    return {"detail":"User deleted successfully"}