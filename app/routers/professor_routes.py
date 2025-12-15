from  fastapi import APIRouter , Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db

from app.schemas.professor import (ProfessorCreate, ProfessorUpdate,ProfessorRead)