from pydantic import BaseModel

class TypeBase(BaseModel):
    name : str
    
class TypeCreate(TypeBase):
    id_user : int

class TypeRead(TypeBase):
    id : int
    
    class Config:
        from_attributes = True

class TypeUpdate(BaseModel):
    name : str | None = None