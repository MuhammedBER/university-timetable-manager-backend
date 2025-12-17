from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.room import RoomCreate, RoomUpdate, RoomRead
from app.repository.room_repository import RoomRepository

router = APIRouter(prefix="/rooms" , tags = ["Rooms"])

@router.post("/", response_model=RoomRead)
def create_room_route(room: RoomCreate, db: Session = Depends(get_db)):
    repo = RoomRepository(db)
    return repo.create(room)

@router.get("/{room_id}", response_model=RoomRead)
def get_room_route(room_id: int, db: Session = Depends(get_db)):
    repo = RoomRepository(db)
    room = repo.get_by_id(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room
@router.get("/", response_model=list[RoomRead])
def get_rooms_route(db: Session = Depends(get_db)):
    repo = RoomRepository(db)
    return repo.get_all()

@router.patch("/{room_id}", response_model=RoomRead)
def update_room_route(
    room_id: int,
    room_update: RoomUpdate,
    db: Session = Depends(get_db)
):
    repo = RoomRepository(db)
    room = repo.update(room_id, room_update)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@router.delete("/{room_id}", response_model=dict)
def delete_room_route(room_id: int, db: Session = Depends(get_db)):
    repo = RoomRepository(db)
    if not repo.delete(room_id):
        raise HTTPException(status_code=404, detail="Room not found")
    return {"message": "Room deleted successfully"}