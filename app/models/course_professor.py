from  sqlalchemy import Column, String, Integer , ForeignKey , Table
from app.database.db import  Base
from sqlalchemy.orm import relationship

course_professor_association = Table(
    "course_professor_association",
    Base.metadata,
    Column("course_id", Integer, ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True , nullable=False),
    Column("professor_id", Integer, ForeignKey("professors.id", ondelete="CASCADE"), primary_key=True, nullable=False),
)