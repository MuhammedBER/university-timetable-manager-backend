from  sqlalchemy import Column, String, Integer , ForeignKey , Table
from app.database.db import  Base
from sqlalchemy.orm import relationship

course_field_association = Table(
    "course_field_association",
    Base.metadata,
    Column("course_id", Integer, ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True , nullable=False),
    Column("field_id", Integer, ForeignKey("fields.id", ondelete="CASCADE"), primary_key=True, nullable=False),
)