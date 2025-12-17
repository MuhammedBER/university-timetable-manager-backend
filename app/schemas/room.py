from pydantic import BaseModel

class RoomBase(BaseModel):
    num : int
    room_type : str
    user_id : int
    
class RoomCreate(RoomBase):
    pass

class RoomRead(RoomBase):
    id : int 
    class Config:
        from_attributes = True
        
class RoomUpdate(BaseModel):
    num : int | None = None
    room_type : str | None = None
    