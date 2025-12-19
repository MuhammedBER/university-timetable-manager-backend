from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.schemas.user import UserUpdate

router = APIRouter(prefix='/api',tags=["User"])

@router.get("/user")
def getUser(current_user = Depends(get_current_user)):
    return current_user
