from typing import Optional

from sqlalchemy.orm import Session

from app.models.field import Field
from app.schemas.field import FieldCreate, FieldUpdate


class FieldRepository:
    def create(self, db: Session, obj_in: FieldCreate) -> Field:
       
        existing = (
            db.query(Field)
            .filter(
                Field.name == obj_in.name,
                Field.university_year == obj_in.university_year,
                Field.user_id == obj_in.user_id,
            )
            .first()
        )
        if existing:
            
            return None

        db_obj = Field(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_all(self, db: Session):
        return db.query(Field).all()

    def get_by_id(self, db: Session, id: int) -> Optional[Field]:
        return db.query(Field).filter(Field.id == id).first()

    def update(self, db: Session, field_id: int, obj_in: FieldUpdate) -> Optional[Field]:
        db_obj = db.query(Field).filter(Field.id == field_id).first()
        if not db_obj:
            return None

        for key, value in obj_in.model_dump(exclude_unset=True).items():
            setattr(db_obj, key, value)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, field_id: int) -> Optional[Field]:
        db_obj = db.query(Field).filter(Field.id == field_id).first()
        if not db_obj:
            return None

        db.delete(db_obj)
        db.commit()
        return db_obj


field_repository = FieldRepository()
