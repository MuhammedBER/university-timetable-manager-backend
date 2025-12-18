from typing import Optional
from sqlalchemy.orm import Session

from app.models.field import Field
from app.models.course import Course
from app.schemas.field import FieldCreate, FieldUpdate


class FieldRepository:
    def create(self, db: Session, obj_in: FieldCreate) -> Optional[Field]:
        existing = (
            db.query(Field)
            .filter(
                Field.name == obj_in.name,
                Field.user_id == obj_in.user_id,
            )
            .first()
        )
        if existing:
            return None

        db_field = Field(name=obj_in.name, user_id=obj_in.user_id)
        if obj_in.course_ids:
            courses = (
                db.query(Course)
                .filter(Course.id.in_(obj_in.course_ids))
                .all()
            )
            db_field.courses = courses

        db.add(db_field)
        db.commit()
        db.refresh(db_field)
        return db_field

    def get_all(self, db: Session) -> list[Field]:
        return db.query(Field).all()

    def get_by_id(self, db: Session, field_id: int) -> Optional[Field]:
        return db.query(Field).filter(Field.id == field_id).first()

    def update(
        self, db: Session, field_id: int, obj_in: FieldUpdate
    ) -> Optional[Field]:
        db_field = self.get_by_id(db, field_id)
        if not db_field:
            return None

        if obj_in.name is not None:
            db_field.name = obj_in.name

        if obj_in.course_ids is not None:
            courses = (
                db.query(Course)
                .filter(Course.id.in_(obj_in.course_ids))
                .all()
            )
            db_field.courses = courses

        db.commit()
        db.refresh(db_field)
        return db_field

    def delete(self, db: Session, field_id: int) -> Optional[Field]:
        db_field = self.get_by_id(db, field_id)
        if not db_field:
            return None

        db.delete(db_field)
        db.commit()
        return db_field


field_repository = FieldRepository()
