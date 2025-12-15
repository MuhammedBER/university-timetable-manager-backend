from pydantic import BaseModel

class FieldBase(BaseModel):
    name :  str
    university_year : str 
    
class FieldRead(FieldBase):
    id : int 
    
class FieldCreate(FieldBase):
    id_user : int

class FieldUpdate(FieldBase):
    name : str | None = None
    university_year : str | None = None
    
 