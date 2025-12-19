from pydantic import BaseModel
from .enrollment import EnrollmentRead
from .shared import ProfessorSimple
from.shared import FieldSimple

class CourseBase(BaseModel):
    name : str
    user_id : int

class CourseCreate(CourseBase):
    professor_ids : list[int] = []
    field_ids : list[int] = []
    td_hours : int
    tp_hours : int
    cours_hours : int

class CourseRead(BaseModel):
    id : int 
    name : str
    professors : list[ProfessorSimple] = []
    fields : list [FieldSimple] = []
    enrollments: list[EnrollmentRead] = []
    class Config:
        from_attributes = True
    
class CourseUpdate(BaseModel):
    name : str | None = None
    professor_ids : list[int] | None = None
    field_ids : list[int] | None = None
    td_hours : int | None = None
    tp_hours : int | None = None
    cours_hours : int | None = None