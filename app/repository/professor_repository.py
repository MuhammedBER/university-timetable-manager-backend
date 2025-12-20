from sqlalchemy.orm import Session

from app.models.course import Course
from app.models.professor import Professor
from app.schemas.professor import ProfessorCreate, ProfessorUpdate, ProfessorRead

class ProfessorRepository:
    def create(self , db : Session , obj_in : ProfessorCreate, user_id: int ) -> Professor:
        db_obj = Professor(
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            user_id=user_id,
            hours_for_week=obj_in.hours_for_week
        )
        # if obj_in.course_ids:
        #     courses = db.query(Course).filter(
        #         Course.id.in_(obj_in.course_ids)
        #     ).all()
            
        #     if len(courses) != len(obj_in.course_ids):
        #         print(f"WARNING: Requested {len(obj_in.course_ids)} courses, found {len(courses)}")
            
        #     db_obj.courses = courses
        if obj_in.course_ids:
            courses = db.query(Course).filter(
                Course.id.in_(obj_in.course_ids)
            ).all()
            db_obj.courses = courses

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_all(self,db: Session ):
        return db.query(Professor).all()

    def get_by_id(self,db: Session , id: int):
        return db.query(Professor).filter(Professor.id == id).first()

    def update(self,db : Session , professor_id:int , obj_in :ProfessorUpdate) :
        db_obj = db.query(Professor).filter(Professor.id == professor_id).first()
        if not(db_obj):
            return None
        for key, value in obj_in.dict(exclude_unset=True).items():
            setattr(db_obj, key, value)
        if obj_in.course_ids:
            courses = db.query(Course).filter(
                Course.id.in_(obj_in.course_ids)
            ).all()
            db_obj.courses = courses
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
            # if obj_in.course_ids:
            # courses = db.query(Course).filter(
            #     Course.id.in_(obj_in.course_ids)
            # ).all()
            # db_obj.courses = courses

    def delete(self, db: Session, professor_id: int):
        db_obj = db.query(Professor).filter(Professor.id == professor_id).first()
        if not db_obj:
            return None
            
        # 1. Clear the relationships (remove rows from the link table)
        db_obj.courses = [] 
        
        # 2. Now you can safely delete the professor
        professor = ProfessorRead.model_validate(db_obj)
        db.delete(db_obj)
        db.commit()
        return professor

professor_repository = ProfessorRepository()