from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.database.db import Base

class Type(Base):
    __tablename__ = "types"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    enrollments = relationship(
        "Enrollment",
        back_populates="type",
        cascade="all, delete-orphan",
    )

    courses = relationship(
        "Course",
        secondary="enrollments",
        viewonly=True,
    )
