from sqlalchemy.orm import Session
from app.models.room import Room
from app.schemas.room import RoomCreate, RoomUpdate

class RoomRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, room: RoomCreate) -> Room:
        db_room = Room(**room.dict())
        self.db.add(db_room)
        self.db.commit()
        self.db.refresh(db_room)
        return db_room

    def get_by_id(self, room_id: int) -> Room | None:
        return self.db.query(Room).filter(Room.id == room_id).first()

    def get_all(self) -> list[Room]:
        return self.db.query(Room).all()

    def update(self, room_id: int, room_update: RoomUpdate) -> Room | None:
        db_room = self.get_by_id(room_id)
        if not db_room:
            return None

        update_data = room_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_room, key, value)

        self.db.commit()
        self.db.refresh(db_room)
        return db_room

    def delete(self, room_id: int) -> bool:
        db_room = self.get_by_id(room_id)
        if not db_room:
            return False

        self.db.delete(db_room)
        self.db.commit()
        return True
