from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db
from app.schemas.time_table import TimeTableCreate, TimeTableUpdate, TimeTableRead
from app.services.time_table_service import time_table_service

router = APIRouter(prefix="/time-tables", tags=["time_tables"])

@router.post("", response_model=TimeTableRead, status_code=status.HTTP_201_CREATED)
def create_time_table(time_table_in: TimeTableCreate, db: Session = Depends(get_db)):
    return time_table_service.create(db, time_table_in)

@router.get("", response_model=List[TimeTableRead])
def get_time_tables(db: Session = Depends(get_db)):
    return time_table_service.get_all(db)

@router.get("/{id}", response_model=TimeTableRead)
def get_time_table(id: int, db: Session = Depends(get_db)):
    time_table = time_table_service.get_by_id(db, id)
    if not time_table:
        raise HTTPException(status_code=404, detail="TimeTable not found")
    return time_table

@router.put("/{id}", response_model=TimeTableRead)
def update_time_table(id: int, time_table_in: TimeTableUpdate, db: Session = Depends(get_db)):
    time_table = time_table_service.update(db, id, time_table_in)
    if not time_table:
        raise HTTPException(status_code=404, detail="TimeTable not found")
    return time_table

@router.delete("/{id}", response_model=TimeTableRead)
def delete_time_table(id: int, db: Session = Depends(get_db)):
    time_table = time_table_service.delete(db, id)
    if not time_table:
        raise HTTPException(status_code=404, detail="TimeTable not found")
    return time_table
