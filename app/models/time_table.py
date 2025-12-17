from  sqlalchemy import Column, String, Integer , ForeignKey
from app.database.db import  Base
from sqlalchemy.orm import relationship

class TimeTable(Base):
    __tablename__ = "time_tables"
    id = Column(Integer, primary_key=True)
    university_year = Column(String(100), nullable=False)
    semester = Column(Integer, nullable=False)
    field = Column(String(100), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE") , nullable=False)

    user = relationship("User", back_populates="time_tables", passive_deletes=True)