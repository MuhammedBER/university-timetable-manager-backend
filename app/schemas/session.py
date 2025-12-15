from pydantic import BaseModel
from datetime import date, time

class SessionBase(BaseModel):
    day : date
    start_hour :  time
    end_hour :  time 
    id_course : int
    id_professor : int
    id_field : int
    id_user : int
    id_room : int

class SessionCreate(SessionBase):
    pass
class SessionRead(SessionBase):
    id: int 
    class Config:
        from_attributes = True
class SessionUpdate(BaseModel):
    day : date | None = None
    start_hour :  time | None = None
    end_hour :  time | None = None
    