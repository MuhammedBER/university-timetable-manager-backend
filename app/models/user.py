from  sqlalchemy import Column, String, Integer
from app.database.db import  Base, engine
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

    professors = relationship("Professor",back_populates="user",cascade="all, delete-orphan", passive_deletes=True)
    rooms = relationship("Room",back_populates="user",cascade="all, delete-orphan", passive_deletes=True)
    fields = relationship("Field",back_populates="user",cascade="all, delete-orphan", passive_deletes=True)
    courses = relationship("Course",back_populates="user",cascade="all, delete-orphan", passive_deletes=True)
    seances = relationship("Seance",back_populates="user",cascade="all, delete-orphan", passive_deletes=True)
