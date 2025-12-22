from  sqlalchemy import Column, String, Integer , ForeignKey , Table
from app.database.db import  Base
from sqlalchemy.orm import relationship

class CourseField(Base):
    __tablename__ = "course_fields"

    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    field_id = Column(Integer, ForeignKey("fields.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    semester = Column(String(50), nullable=True) # S1, S2, etc.

    course = relationship("Course", back_populates="course_fields")
    field = relationship("Field", back_populates="course_fields")