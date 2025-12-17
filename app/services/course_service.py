from sqlalchemy.orm import Session

from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate
from app.repository.course_repository import course_repository


class CourseService:
    def create(self, db: Session, obj_in: CourseCreate) -> Course:
        return course_repository.create(db, obj_in)

    def get_all(self, db: Session):
        return course_repository.get_all(db)

    def get_by_id(self, db: Session, course_id: int):
        return course_repository.get_by_id(db, course_id)

    def update(self, db: Session, course_id: int, obj_in: CourseUpdate):
        return course_repository.update(db, course_id, obj_in)

    def delete(self, db: Session, course_id: int):
        return course_repository.delete(db, course_id)


course_service = CourseService()
