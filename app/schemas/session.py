from pydantic import BaseModel
from datetime import date, time

class SessionBase(BaseModel):
    day : date
    start_hour :  time
    end_hour :  time 
    course_id : int
    professor_id : int
    field_id : int
    user_id : int
    room_id : int
    type_id : int

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
    