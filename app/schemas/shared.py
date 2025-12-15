from pydantic import BaseModel

class CourseSimple(BaseModel):
    id: int 
    name: str

class TypeSimple(BaseModel):
    id: int 
    name: str