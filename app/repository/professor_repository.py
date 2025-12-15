from sqlalchemy.orm import Session
from app.models.professor import Professor
from app.schemas.professor import ProfessorCreate, ProfessorUpdate

class ProfessorRepository:
    def create(self , db : Session , obj_in : ProfessorCreate ) -> Professor:
        db_obj = Professor(**obj_in.dict())
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
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self,db : Session , professor_id:int):
        db_obj = db.query(Professor).filter(Professor.id == professor_id).first()
        if not(db_obj):
            return None
        db.delete(db_obj)
        db.commit()
        return db_obj

professor_repository = ProfessorRepository()