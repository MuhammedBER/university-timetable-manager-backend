from pydantic import BaseModel
from .shared import CourseSimple

class ProfessorBase(BaseModel):
    first_name : str
    last_name : str
    hours_for_week : int
    
class ProfessorCreate(BaseModel):
    first_name : str
    last_name : str
    hours_for_week : int
    course_ids : list[int] = []

class ProfessorRead(ProfessorBase):
    id : int
    courses : list[CourseSimple] = []
    class Config:
        from_attributes = True
        
        
class ProfessorUpdate(BaseModel):
    first_name : str | None = None
    last_name : str | None = None
    hours_for_week : int | None = None
    course_ids : list[int] | None = None