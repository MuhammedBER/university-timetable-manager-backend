from  sqlalchemy import Column, String, Integer , ForeignKey
from app.database.db import  Base, engine
from sqlalchemy.orm import relationship

class Professor(Base):
    __tablename__ = "professors"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    hours_for_week = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="professors", passive_deletes=True)
    courses = relationship('Course', secondary='course_professor_association', back_populates='professors',cascade="all, delete")
    seances = relationship('Seance', back_populates='professor',cascade="all, delete-orphan",passive_deletes=True)