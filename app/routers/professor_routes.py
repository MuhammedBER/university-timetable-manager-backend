from  fastapi import APIRouter , Depends ,  HTTPException , status
from sqlalchemy.orm import Session

from app.api.deps import get_db

from app.schemas.professor import (ProfessorCreate, ProfessorUpdate,ProfessorRead)

from app.services.professor_service import professor_service

router = APIRouter(prefix="/professors", tags=["professors"])

@router.post("", response_model=ProfessorRead,status_code=status.HTTP_201_CREATED)
def create_professor(professor_in: ProfessorCreate , db: Session = Depends(get_db)):
    return professor_service.create(db, professor_in)

@router.get("", response_model=list[ProfessorRead])
def get_professors(db: Session = Depends(get_db)):
    return professor_service.get_all(db)

@router.get("/{id}", response_model=ProfessorRead)
def get_professor(id: int, db: Session = Depends(get_db)):
    professor = professor_service.get_by_id(db, id)
    if not professor :
        raise HTTPException(status_code=404, detail="Professor not found")
    return professor

@router.put("/{id}", response_model=ProfessorRead)
def update_professor(id:int , professor_in: ProfessorUpdate , db: Session = Depends(get_db)):
    professor = professor_service.update(db, id, professor_in)
    if not professor :
        raise HTTPException(status_code=404, detail="Professor not found")
    return professor


@router.delete("/{id}", response_model=ProfessorRead)
def delete_professor(id: int, db: Session = Depends(get_db)):
    professor = professor_service.delete(db, id)
    if not professor :
        raise HTTPException(status_code=404, detail="Professor not found")