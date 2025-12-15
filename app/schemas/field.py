from pydantic import BaseModel

class FieldBase(BaseModel):
    name :  str
    university_year : str 
    user_id : int
    
class FieldRead(FieldBase):
    id : int 
    class Config:
        from_attributes = True
    
class FieldCreate(FieldBase):
    pass

class FieldUpdate(BaseModel):
    name : str | None = None
    university_year : str | None = None
    
 