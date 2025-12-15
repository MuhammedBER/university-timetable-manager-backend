from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database.db import Base

course_type_association = Table(
    "course_type_association",
    Base.metadata,
    Column("course_id", Integer, ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True, nullable=False),
    Column("type_id", Integer, ForeignKey("types.id", ondelete="CASCADE"), primary_key=True, nullable=False),
    Column("nbr_hours", Integer, nullable=False)
)