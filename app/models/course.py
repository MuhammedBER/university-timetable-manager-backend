from  sqlalchemy import Column, String, Integer , ForeignKey
from app.database.db import  Base
from sqlalchemy.orm import relationship

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE") , nullable=False)

    user = relationship("User", back_populates="courses", passive_deletes=True)

    types = relationship('Type', secondary='course_type_association', back_populates='courses',cascade="all, delete")
    professors = relationship('Professor', secondary='course_professor_association', back_populates='courses',cascade="all, delete")

    seances = relationship('Seance', back_populates='course',cascade="all, delete-orphan",passive_deletes=True)