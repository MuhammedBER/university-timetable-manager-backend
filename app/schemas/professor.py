from pydantic import BaseModel

class ProfessorBase(BaseModel):
    first_name : str
    last_name : str


class ProfessorCreate(ProfessorBase):
    id_user : int


class ProfessorRead(ProfessorBase):
    id : int
    
    class Config:
        from_attributes = True
        
        
class ProfessorUpdate(BaseModel):
    first_name : str | None = None
    last_naem : str | None = None