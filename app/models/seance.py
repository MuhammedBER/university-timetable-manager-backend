from  sqlalchemy import Column, String, Integer , ForeignKey , Time
from app.database.db import  Base, engine
from sqlalchemy.orm import relationship

class Seance(Base):
    __tablename__ = 'seances'

    id = Column(Integer, primary_key=True)
    day = Column(String(50), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    semester = Column(String(50), nullable=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    field_id = Column(Integer, ForeignKey("fields.id", ondelete="CASCADE"), nullable=False)
    professor_id = Column(Integer, ForeignKey("professors.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    type_id = Column(Integer, ForeignKey("types.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="seances", passive_deletes=True)
    field = relationship("Field", back_populates="seances", passive_deletes=True)
    course = relationship("Course", back_populates="seances", passive_deletes=True)
    room = relationship("Room", back_populates="seances", passive_deletes=True)
    professor = relationship("Professor",back_populates="seances", passive_deletes=True)
    type = relationship("Type", back_populates="seances", passive_deletes=True)