from sqlalchemy.orm import Session
from app.models.time_table import TimeTable
from app.schemas.time_table import TimeTableCreate, TimeTableUpdate
from app.repository.time_table_repository import time_table_repository

class TimeTableService:
    def create(self, db: Session, obj_in: TimeTableCreate) -> TimeTable:
        return time_table_repository.create(db, obj_in)

    def get_all(self, db: Session):
        return time_table_repository.get_all(db)

    def get_by_id(self, db: Session, id: int):
        return time_table_repository.get_by_id(db, id)

    def update(self, db: Session, id: int, obj_in: TimeTableUpdate):
        return time_table_repository.update(db, id, obj_in)

    def delete(self, db: Session, id: int):
        return time_table_repository.delete(db, id)

time_table_service = TimeTableService()
