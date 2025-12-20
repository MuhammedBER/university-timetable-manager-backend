from pydantic import BaseModel
from typing import Optional

class TimeTableBase(BaseModel):
    university_year: str
    semester: int
    field: str
    url: Optional[str] = None
    user_id: int

class TimeTableCreate(TimeTableBase):
    pass

class TimeTableUpdate(BaseModel):
    university_year: Optional[str] = None
    semester: Optional[int] = None
    field: Optional[str] = None
    user_id: Optional[int] = None
    url: Optional[str] = None
    

class TimeTableRead(TimeTableBase):
    id: int

    class Config:
        from_attributes = True
