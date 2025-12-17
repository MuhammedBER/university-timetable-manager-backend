from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database.db import Base

class Field(Base):
    __tablename__ = "fields"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="fields",
        passive_deletes=True,
    )
    courses = relationship(
        "Course",
        secondary="course_field_association",
        back_populates="fields",
    )

    seances = relationship(
        "Seance",
        back_populates="field",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
