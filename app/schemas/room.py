from pydantic import BaseModel

class SalleBase(BaseModel):
    num : int
    type : str

class SalleCreate(SalleBase):
    id_user : int
class SalleRead(SalleBase):
    id : int 
    class Config:
        from_attributes = True
class SalleUpdate(SalleBase):
    num : int | None = None
    type : int | None = None
    