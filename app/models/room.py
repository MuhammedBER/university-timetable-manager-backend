from  sqlalchemy import Column, String, Integer , ForeignKey
from app.database.db import  Base, engine
from sqlalchemy.orm import relationship

class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    num = Column(Integer, nullable=False)
    room_type = Column(String(50), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="rooms", passive_deletes=True)
    seances = relationship("Seance", back_populates="room",cascade="all, delete-orphan",passive_deletes=True)
