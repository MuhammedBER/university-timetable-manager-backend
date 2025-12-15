from sqlalchemy.orm import Session
from app.models.professor import Professor
from app.schemas.professor import ProfessorCreate, ProfessorUpdate
from app.repository.professor_repository import professor_repository

class ProfessorService:
    def create(self,db:Session ,obj_in:ProfessorCreate) -> Professor:
        return professor_repository.create(db,obj_in)

    def get_all(self,db:Session ) :
        return professor_repository.get_all(db)

    def get_by_id(self,db:Session,professor_id:int) :
        return professor_repository.get_by_id(db,professor_id)

    def update(self,db:Session,professor_id:int,obj_in:ProfessorUpdate)  :
        return professor_repository.update(db,professor_id,obj_in)

    def delete(self,db:Session,professor_id:int) :
        return professor_repository.delete(db,professor_id)

professor_service = ProfessorService()
