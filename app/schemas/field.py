from pydantic import BaseModel
from .shared import CourseSimple

class FieldBase(BaseModel):
    name :  str
    user_id : int
    
class FieldRead(FieldBase):
    id : int 
    courses : list[CourseSimple] = []
    class Config:
        from_attributes = True
    
class FieldCreate(FieldBase):
    course_ids : list[int] = []

class FieldUpdate(BaseModel):
    name : str | None = None
    course_ids : list[int] | None = None
    
    
 