from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user_id
from app.schemas.room import RoomCreate, RoomUpdate, RoomRead
from app.repository.room_repository import RoomRepository

router = APIRouter(prefix="/rooms" , tags = ["Rooms"])

@router.post("/", response_model=RoomRead)
def create_room_route(room: RoomCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    repo = RoomRepository(db)
    room_data = room.model_dump()
    room_data["user_id"] = user_id
    
    # Manually attach user_id since RoomCreate structure doesn't support it anymore
    room_with_user = RoomCreate(**room_data)
    if not hasattr(room_with_user, "user_id"):
        object.__setattr__(room_with_user, "user_id", user_id)
        
    return repo.create(room_with_user)

@router.get("/{room_id}", response_model=RoomRead)
def get_room_route(room_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    repo = RoomRepository(db)
    room = repo.get_by_id(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if room.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return room

@router.get("/", response_model=list[RoomRead])
def get_rooms_route(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    repo = RoomRepository(db)
    all_rooms = repo.get_all()
    return [item for item in all_rooms if item.user_id == user_id]

@router.patch("/{room_id}", response_model=RoomRead)
def update_room_route(
    room_id: int,
    room_update: RoomUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    repo = RoomRepository(db)
    existing = repo.get_by_id(room_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Room not found")
    if existing.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    room = repo.update(room_id, room_update)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@router.delete("/{room_id}", response_model=dict)
def delete_room_route(room_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    repo = RoomRepository(db)
    existing = repo.get_by_id(room_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Room not found")
    if existing.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    if not repo.delete(room_id):
        raise HTTPException(status_code=404, detail="Room not found")
    return {"message": "Room deleted successfully"}