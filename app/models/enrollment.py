from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database.db import Base

class Enrollment(Base):
    __tablename__ = "enrollments"

    course_id = Column(
        Integer,
        ForeignKey("courses.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )

    type_id = Column(
        Integer,
        ForeignKey("types.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )

    nbr_hours = Column(Integer, nullable=False)

    course = relationship("Course", back_populates="enrollments")
    type = relationship("Type", back_populates="enrollments")
