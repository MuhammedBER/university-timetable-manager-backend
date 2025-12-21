from sqlalchemy.orm import Session
from app.models.time_table import TimeTable
from app.schemas.time_table import TimeTableCreate, TimeTableUpdate

class TimeTableRepository:
    def create(self, db: Session, obj_in: TimeTableCreate, user_id: int) -> TimeTable:
        db_obj = TimeTable(
            university_year=obj_in.university_year,
            semester=obj_in.semester,
            field=obj_in.field,
            user_id=user_id,
            url=obj_in.url
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_all(self, db: Session):
        return db.query(TimeTable).all()

    def get_by_id(self, db: Session, id: int):
        return db.query(TimeTable).filter(TimeTable.id == id).first()

    def update(self, db: Session, id: int, obj_in: TimeTableUpdate):
        db_obj = db.query(TimeTable).filter(TimeTable.id == id).first()
        if not db_obj:
            return None
        
        update_data = obj_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_obj, key, value)
            
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int):
        db_obj = db.query(TimeTable).filter(TimeTable.id == id).first()
        if not db_obj:
            return None
        
        db.delete(db_obj)
        db.commit()
        return db_obj

time_table_repository = TimeTableRepository()
