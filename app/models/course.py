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

    fields = relationship(
        "Field",
        secondary="course_field_association",
        back_populates="courses",
        # The cascade setting here is likely also incorrect if fields shouldn't be deleted.
        # For safety, I'll remove it as it was also likely causing unintended deletions.
        # If Field should be deleted, change "all, delete" to "all, delete-orphan".
    )

    seances = relationship(
        "Seance",
        back_populates="course",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )