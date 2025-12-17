from sqlalchemy.orm import Session
from app.models.course import Course
from app.models.professor import Professor
from app.models.enrollment import Enrollment
from app.schemas.course import CourseCreate, CourseUpdate


class CourseRepository:
    def create(self, db: Session, obj_in: CourseCreate) -> Course:
        # Create the course
        db_obj = Course(
            name=obj_in.name,
            user_id=obj_in.user_id,
        )
        
        # Add professors if provided
        if obj_in.professor_ids:
            # Note: Robustness check for valid professor IDs should ideally be here.
            professors = db.query(Professor).filter(Professor.id.in_(obj_in.professor_ids)).all()
            db_obj.professors = professors

        db.add(db_obj)
        # We commit/refresh only once at the end for atomicity (Course and Enrollments in one transaction).
        
        # Create enrollments for TD, TP, and Cour
        # Assuming type IDs: TD=1, TP=2, Cour=3
        enrollments_data = [
            {"id_type": 1, "nbr_hour": obj_in.td_hours},     # TD
            {"id_type": 2, "nbr_hour": obj_in.tp_hours},     # TP
            {"id_type": 3, "nbr_hour": obj_in.cour_hours},   # Cour (consistent naming)
        ]
        
        for enroll_data in enrollments_data:
            enrollment = Enrollment(
                id_course=db_obj.id, 
                id_type=enroll_data["id_type"],
                nbr_hour=enroll_data["nbr_hour"]
            )
            db.add(enrollment)
        
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
        
        # Handle professor_ids specially
        if "professor_ids" in data:
            prof_ids = data.pop("professor_ids")
            if prof_ids is None:
                db_obj.professors = []
            else:
                professors = db.query(Professor).filter(Professor.id.in_(prof_ids)).all()
                db_obj.professors = professors
        
        # Handle enrollment hours updates
        hours_updates = {}
        if "td_hours" in data:
            hours_updates[1] = data.pop("td_hours")     # TD type_id = 1
        if "tp_hours" in data:
            hours_updates[2] = data.pop("tp_hours")     # TP type_id = 2
        if "cour_hours" in data:
            hours_updates[3] = data.pop("cour_hours")   # Cour type_id = 3 (consistent naming)
        
        # Update enrollments if hours are provided
        for type_id, nbr_hour in hours_updates.items():
            enrollment = db.query(Enrollment).filter(
                Enrollment.id_course == course_id,
                Enrollment.id_type == type_id
            ).first()
            
            if enrollment:
                enrollment.nbr_hour = nbr_hour
            else:
                # Create enrollment if it doesn't exist
                new_enrollment = Enrollment(
                    id_course=course_id,
                    id_type=type_id,
                    nbr_hour=nbr_hour
                )
                db.add(new_enrollment)

        # Update remaining course fields
        for key, value in data.items():
            setattr(db_obj, key, value)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, course_id: int):
        db_obj = db.query(Course).filter(Course.id == course_id).first()
        if not db_obj:
            return None
        
        # Delete associated enrollments first
        # (Only necessary if ondelete="CASCADE" is not correctly set on the Enrollment table relationship)
        db.query(Enrollment).filter(Enrollment.id_course == course_id).delete(synchronize_session=False)
        
        db.delete(db_obj)
        db.commit()
        return db_obj


course_repository = CourseRepository()