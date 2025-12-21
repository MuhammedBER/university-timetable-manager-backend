from pydantic import BaseModel

class CourseSimple(BaseModel):
    id: int 
    name: str
    class Config:
        from_attributes = True

class TypeSimple(BaseModel):
    id: int 
    name: str
    class Config:
        from_attributes = True

class ProfessorSimple(BaseModel):
    id : int
    first_name : str
    last_name : str
    class Config:
        from_attributes = True

class FieldSimple(BaseModel):
    id : int
    name :  str
    class Config:
        from_attributes = True