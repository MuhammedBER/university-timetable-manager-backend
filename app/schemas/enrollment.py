from pydantic import BaseModel
from shared import CourseSimple
from shared import TypeSimple

class EnrollmentBase(BaseModel):
    id_type : int
    id_course : int 
    nbr_hour : int 
    
class EnrollmentCreate(EnrollmentBase):
    pass
class EnrollmentRead(EnrollmentBase):
    courses : list [CourseSimple] | None = None
    types : list [TypeSimple] | None = None
    class Config:
        from_attributes = True
class EnrollmentUpdate(BaseModel):
    nbr_hour : int | None = None