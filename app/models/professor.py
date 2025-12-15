from  sqlalchemy import Column, String, Integer
from app.database.db import  Base, engine

class Professor(Base):
    __tablename__ = "professors"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
