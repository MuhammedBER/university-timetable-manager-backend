from pydantic import BaseModel

class CourseSimple(BaseModel):
    id: int 
    name: str

class TypeSimple(BaseModel):
    id: int 
    name: str

class ProfessorSimple(BaseModel):
    id : int
    first_name : str
    last_name : str
    email: str