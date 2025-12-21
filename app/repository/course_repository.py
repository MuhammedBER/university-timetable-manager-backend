from sqlalchemy.orm import Session
# Ensure these model imports are correct based on your file structure
from app.models.course import Course
from app.models.professor import Professor
from app.models.field import Field 
from app.models.enrollment import Enrollment
from app.schemas.course import CourseCreate, CourseUpdate


class CourseRepository:
    def create(self, db: Session, obj_in: CourseCreate, user_id: int) -> Course:
        # Create the course base object
        db_obj = Course(
            name=obj_in.name,
            user_id=user_id,
        )
        
        # 1. Handle professor and field associations
        if obj_in.professor_ids:
            professors = db.query(Professor).filter(Professor.id.in_(obj_in.professor_ids)).all()
            db_obj.professors = professors

        if obj_in.field_ids:
            fields = db.query(Field).filter(Field.id.in_(obj_in.field_ids)).all()
            db_obj.fields = fields

        db.add(db_obj)
        db.flush() 

        # 2. Create enrollments for TD, TP, and Cours
        # The type IDs are: 1=TD, 2=TP, 3=Cours
        enrollments_data = [
            {"type_id": 1, "hour_val": obj_in.td_hours},     
            {"type_id": 2, "hour_val": obj_in.tp_hours},     
            {"type_id": 3, "hour_val": obj_in.cours_hours},  
        ]
        
        for enroll_data in enrollments_data:
            enrollment = Enrollment(
                course_id=db_obj.id,           # Matches model
                type_id=enroll_data["type_id"],
                # *** FINAL FIX APPLIED HERE: Using nbr_hours (plural) ***
                nbr_hours=enroll_data["hour_val"]
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

        data = obj_in.model_dump(exclude_unset=True)
        
        # 1. Handle professor_ids
        if "professor_ids" in data:
            prof_ids = data.pop("professor_ids")
            if prof_ids is None:
                db_obj.professors = []
            else:
                professors = db.query(Professor).filter(Professor.id.in_(prof_ids)).all()
                db_obj.professors = professors
        
        # 2. Handle field_ids
        if "field_ids" in data:
            field_ids = data.pop("field_ids")
            if field_ids is None:
                db_obj.fields = []
            else:
                fields = db.query(Field).filter(Field.id.in_(field_ids)).all()
                db_obj.fields = fields
                
        # 3. Handle enrollment hours updates
        hours_updates = {}
        if "td_hours" in data:
            hours_updates[1] = data.pop("td_hours")     
        if "tp_hours" in data:
            hours_updates[2] = data.pop("tp_hours")     
        if "cours_hours" in data:
            hours_updates[3] = data.pop("cours_hours")  
        
        # Update or Create enrollments if hours are provided
        for type_id, hour_val in hours_updates.items():
            enrollment = db.query(Enrollment).filter(
                Enrollment.course_id == course_id,
                Enrollment.type_id == type_id 
            ).first()
            
            if enrollment:
                # *** FINAL FIX APPLIED HERE: Using nbr_hours (plural) ***
                enrollment.nbr_hours = hour_val
            elif hour_val is not None:
                new_enrollment = Enrollment(
                    course_id=course_id,
                    type_id=type_id,
                    # *** FINAL FIX APPLIED HERE: Using nbr_hours (plural) ***
                    nbr_hours=hour_val
                )
                db.add(new_enrollment)

        # 4. Update remaining course fields
        for key, value in data.items():
            setattr(db_obj, key, value)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, course_id: int):
        db_obj = db.query(Course).filter(Course.id == course_id).first()
        if not db_obj:
            return None
        
        # Delete associated enrollments first (uses course_id, which is correct)
        db.query(Enrollment).filter(Enrollment.course_id == course_id).delete(synchronize_session=False)
        
        db.delete(db_obj)
        db.commit()
        return db_obj


course_repository = CourseRepository()