from sqlalchemy.orm import Session

from app.models.course import Course
from app.models.professor import Professor
from app.schemas.course import CourseCreate, CourseUpdate


class CourseRepository:
    def create(self, db: Session, obj_in: CourseCreate) -> Course:
        db_obj = Course(
            name=obj_in.name,
            user_id=obj_in.user_id,
        )
        if obj_in.professor_ids:
            professors = db.query(Professor).filter(Professor.id.in_(obj_in.professor_ids)).all()
            db_obj.professors = professors

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_all(self, db: Session):
        return db.query(Course).all()

    def get_by_id(self, db: Session, id: int):
        return db.query(Course).filter(Course.id == id).first()

    def update(self, db: Session, course_id: int, obj_in: CourseUpdate):
        db_obj = db.query(Course).filter(Course.id == course_id).first()
        if not db_obj:
            return None

        data = obj_in.dict(exclude_unset=True)
        # handle professor_ids specially
        if "professor_ids" in data:
            prof_ids = data.pop("professor_ids")
            if prof_ids is None:
                db_obj.professors = []
            else:
                professors = db.query(Professor).filter(Professor.id.in_(prof_ids)).all()
                db_obj.professors = professors

        for key, value in data.items():
            setattr(db_obj, key, value)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, course_id: int):
        db_obj = db.query(Course).filter(Course.id == course_id).first()
        if not db_obj:
            return None
        db.delete(db_obj)
        db.commit()
        return db_obj


course_repository = CourseRepository()
