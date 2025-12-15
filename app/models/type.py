from  sqlalchemy import Column, String, Integer , ForeignKey
from app.database.db import  Base, engine
from sqlalchemy.orm import relationship

class Type(Base):
    __tablename__ = 'types'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    courses = relationship('Course', secondary='course_type_association', back_populates='types',cascade="all, delete")