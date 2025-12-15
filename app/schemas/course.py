from pydantic import BaseModel

class CourseBase(BaseModel):
    name : str

class CourseCreate(CourseBase):
    pass

class CourseRead(BaseModel):
    id : int 
    
class CourseUpdate(BaseModel):
    name : str | None = None