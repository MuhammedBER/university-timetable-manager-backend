from pydantic import BaseModel
from .shared import CourseSimple
from .shared import TypeSimple

class EnrollmentBase(BaseModel):
    type_id : int
    course_id : int 
    nbr_hours : int 
    
class EnrollmentCreate(EnrollmentBase):
    pass
class EnrollmentRead(EnrollmentBase):
    pass
    class Config:
        from_attributes = True
class EnrollmentUpdate(BaseModel):
    nbr_hours : int | None = None