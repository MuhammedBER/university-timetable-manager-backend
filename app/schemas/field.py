from pydantic import BaseModel

class FieldBase(BaseModel):
    name :  str
    university_year : str 
    id_user : int
    
class FieldRead(FieldBase):
    id : int 
    class Config:
        from_attributes = True
    
class FieldCreate(FieldBase):
    pass

class FieldUpdate(BaseModel):
    name : str | None = None
    university_year : str | None = None
    
 