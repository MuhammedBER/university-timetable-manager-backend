from pydantic import BaseModel

class RoomBase(BaseModel):
    num : int
    type : str
    id_user : int
class RoomCreate(RoomBase):
    pass
class RoomRead(RoomBase):
    id : int 
    class Config:
        from_attributes = True
class RoomUpdate(BaseModel):
    num : int | None = None
    type : str | None = None
    