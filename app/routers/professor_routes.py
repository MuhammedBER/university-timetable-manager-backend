from  fastapi import APIRouter , Depends ,  HTTPException , status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user_id

from app.schemas.professor import (ProfessorCreate, ProfessorUpdate,ProfessorRead)

from app.services.professor_service import professor_service

router = APIRouter(prefix="/professors", tags=["professors"])

@router.post("", response_model=ProfessorRead,status_code=status.HTTP_201_CREATED)
def create_professor(professor_in: ProfessorCreate , db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    professor_with_user = ProfessorCreate(**professor_in.model_dump())
    return professor_service.create(db, professor_with_user, user_id)
    # Wait, the prompt says: "REMOVE user_id field from {Entity}Create class ONLY. Keep user_id in {Entity}Read class."
    # And specifically for Pattern 1 (Service): 
    # {entity}_data = {entity}_in.model_dump()
    # {entity}_data["user_id"] = user_id
    # {entity}_with_user = {Entity}Create(**{entity}_data)
    # BUT I just removed user_id from ProfessorCreate! So I cannot re-instantiate ProfessorCreate with user_id if the field is gone.
    # Looking at the prompt's example:
    # BEFORE: class ProfessorCreate(BaseModel): first_name: str; user_id: int
    # AFTER: class ProfessorCreate(BaseModel): first_name: str
    #
    # Then in route:
    # {entity}_with_user = {Entity}Create(**{entity}_data)
    # This seemingly contradicts Pydantic validation if I pass 'user_id' to a model that doesn't define it, UNLESS extra="ignore" or similar.
    # However, Looking at the prompt again carefully.
    # "Pattern 1 ... {entity}_with_user = {Entity}Create(**{entity}_data)"
    # If {Entity}Create no longer has user_id, this line will fail if I pass user_id, OR it will just ignore it.
    # But then passing it to service.create(db, {entity}_with_user) means the service receives an object WITHOUT user_id.
    # Let's check the service.
    
    # Actually, looking at app/schemas/professor.py:
    # class ProfessorBase(BaseModel): ... user_id: int ...
    # class ProfessorCreate(ProfessorBase): ...
    # So ProfessorCreate INHERITS user_id.
    # The instruction said: "REMOVE user_id field from {Entity}Create class ONLY".
    # In my previous step (Step 37), I changed ProfessorCreate to NOT inherit from ProfessorBase? 
    # No, I replaced "class ProfessorCreate(ProfessorBase):" with "class ProfessorCreate(BaseModel):" effectively, redefining the fields.
    # Ah, I see what I did in Step 37.
    # Original:
    # class ProfessorBase(BaseModel): ... user_id: int ...
    # class ProfessorCreate(ProfessorBase): ...
    
    # My replacement in Step 37:
    # class ProfessorCreate(BaseModel):
    #     first_name : str
    #     last_name : str
    #     hours_for_week : int
    #     course_ids : list[int] = []
    
    # So I decoupled it from ProfessorBase. Good.
    # Now, how do I pass user_id to the service?
    # The service likely takes the Pydantic model and converts it to DB model.
    # If the service does `db_obj = Professor(**obj_in.model_dump())`, then `obj_in` needs `user_id`?
    # Or does the service expect a dict?
    # The prompt says:
    # {entity}_data = {entity}_in.model_dump()
    # {entity}_data["user_id"] = user_id
    # {entity}_with_user = {Entity}Create(**{entity}_data)
    
    # This logic provided in the prompt implies {Entity}Create SHOULD accept user_id. 
    # But the prompt ALSO says "REMOVE user_id field from {Entity}Create".
    # This is a contradiction in the instructions IF strict validation is on.
    # However, maybe the user implies I should use a DIFFERENT schema or just pass the dict?
    # "return {entity}_service.create(db, {entity}_with_user)"
    
    # The services usually invoke .model_dump() or .dict().
    # Let's assume I should NOT re-instantiate ProfessorCreate if it doesn't have the field.
    # I should probably inspect the service to see what it does.
    # Reading app/services/professor_service.py would be wise.
    pass

@router.get("", response_model=list[ProfessorRead])
def get_professors(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    all_professors = professor_service.get_all(db)
    return [item for item in all_professors if item.user_id == user_id]

@router.get("/{id}", response_model=ProfessorRead)
def get_professor(id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    professor = professor_service.get_by_id(db, id)
    if not professor :
        raise HTTPException(status_code=404, detail="Professor not found")
    if professor.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return professor

@router.put("/{id}", response_model=ProfessorRead)
def update_professor(id:int , professor_in: ProfessorUpdate , db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    existing = professor_service.get_by_id(db, id)
    if not existing:
         raise HTTPException(status_code=404, detail="Professor not found")
    if existing.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    professor = professor_service.update(db, id, professor_in)
    if not professor :
        raise HTTPException(status_code=404, detail="Professor not found")
    return professor


@router.delete("/{id}", response_model=ProfessorRead)
def delete_professor(id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    existing = professor_service.get_by_id(db, id)
    if not existing:
         raise HTTPException(status_code=404, detail="Professor not found")
    if existing.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    professor = professor_service.delete(db, id)
    if not professor :
        raise HTTPException(status_code=404, detail="Professor not found")
    print(f"DEBUG: Deleted professor object: {professor}")
    print(f"DEBUG: Type: {type(professor)}")
    return professor