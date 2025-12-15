from pydantic import BaseModel
from shared import CourseSimple

class ProfessorBase(BaseModel):
    first_name : str
    last_name : str
class ProfessorCreate(ProfessorBase):
    id_user : int
    course_ids : list[int]

class ProfessorRead(ProfessorBase):
    id : int
    courses : list[CourseSimple] = []
    class Config:
        from_attributes = True
        
        
class ProfessorUpdate(BaseModel):
    first_name : str | None = None
    last_name : str | None = None