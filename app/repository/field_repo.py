from typing import Optional

from sqlalchemy.orm import Session
from app.models.field import Field
from app.schemas.field import FieldCreate, FieldUpdate
from app.models.course import Course

class FieldRepository:
    def create(self, db: Session, obj_in: FieldCreate) -> Optional[Field]:
        # Vérifier si un field identique existe déjà
        existing = (
            db.query(Field)
            .filter(
                Field.name == obj_in.name,             
                Field.user_id== obj_in.user_id,
            )
            .first()
        )
        if existing:
            return None

        db_obj = Field(
            name=obj_in.name,
            user_id=obj_in.user_id,
        )
        courses = []
        if obj_in.course_ids:
            courses = db.query(Course).filter(
                Course.id.in_(obj_in.course_ids)
            ).all()
        db_obj.courses = courses
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_all(self, db: Session):
        return db.query(Field).all()

    def get_by_id(self, db: Session, field_id: int) -> Optional[Field]:
        return db.query(Field).filter(Field.id == field_id).first()

    def update(self, db: Session, field_id: int, obj_in: FieldUpdate) -> Optional[Field]:
        db_obj = db.query(Field).filter(Field.id == field_id).first()
        if not db_obj:
            return None

        update_data = obj_in.model_dump(exclude_unset=True)
        if "course_ids" in update_data:
            course_ids = update_data.pop("course_ids")
            if course_ids is not None:
                courses = db.query(Course).filter(
                    Course.id.in_(course_ids)
                ).all()
                db_obj.courses = courses
            else:
                db_obj.courses = []

        for key, value in update_data.items():
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
