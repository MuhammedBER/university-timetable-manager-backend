from pydantic import BaseModel
from enrollment import EnrollmentRead
from shared import ProfessorSimple

class CourseBase(BaseModel):
    name : str
    id_user : int

class CourseCreate(CourseBase):
    professor_ids : list[int] = []

class CourseRead(BaseModel):
    id : int 
    professors : list[ProfessorSimple] = []
    enrollments: list[EnrollmentRead] = []
    class Config:
        from_attributes = True
    
class CourseUpdate(BaseModel):
    name : str | None = None
    professor_ids : list[int] | None =None
    