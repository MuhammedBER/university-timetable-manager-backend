from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database.db import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="courses",
        passive_deletes=True,
    )

    enrollments = relationship(
        "Enrollment",
        back_populates="course",
        cascade="all, delete-orphan",
    )

    types = relationship(
        "Type",
        secondary="enrollments",
        viewonly=True,
    )

    professors = relationship(
        "Professor",
        secondary="course_professor_association",
        back_populates="courses",
        # FIX: Removed cascade="all, delete" to prevent deleting the Professor entity 
        # when the Course is deleted. The association link will be removed.
    )

    course_fields = relationship(
        "CourseField",
        back_populates="course",
        cascade="all, delete-orphan",
    )

    fields = relationship(
        "Field",
        secondary="course_fields",
        back_populates="courses",
        viewonly=True,
    )

    seances = relationship(
        "Seance",
        back_populates="course",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )