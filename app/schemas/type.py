from pydantic import BaseModel
from enrollment import EnrollmentRead

class TypeBase(BaseModel):
    name : str
    
class TypeCreate(TypeBase):
    id_user : int

class TypeRead(TypeBase):
    id : int
    enrollments: list[EnrollmentRead] = []
    
    class Config:
        from_attributes = True

class TypeUpdate(BaseModel):
    name : str | None = None