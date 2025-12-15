from pydantic import BaseModel
from enrollment import EnrollmentRead

class TypeBase(BaseModel):
    name : str
    user_id : int
    
class TypeCreate(TypeBase):
    pass

class TypeRead(TypeBase):
    id : int
    enrollments: list[EnrollmentRead] = []
    
    class Config:
        from_attributes = True

class TypeUpdate(BaseModel):
    name : str | None = None