from pydantic import BaseModel
from .field import FieldRead
from .room import RoomRead
from .course import CourseRead
from .professor import ProfessorRead
from .session import SessionRead

class UserBase(BaseModel):
    first_name : str
    last_name : str
    email : str 

class UserRead(UserBase):
    id :  int
    fields: list[FieldRead] = [] 
    courses: list[CourseRead] = [] 
    professors: list[ProfessorRead] = [] 
    rooms: list[RoomRead] = [] 
    sessions: list[SessionRead] = [] 
    class Config:
        from_attributes = True
class UserCreate(UserBase):
    password : str 

class UserUpdate(BaseModel):
    password : str | None = None
    first_name : str | None = None
    last_name : str | None = None
    email : str | None = None
    
class UserApi(UserBase):
    id : int

class UserPasswordUpdate(BaseModel):
    old_password : str
    new_password : str
    
class ResetPasswordRequest(BaseModel):
    email: str