from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.course import CourseCreate, CourseUpdate, CourseRead
from app.services.course_service import course_service


router = APIRouter(prefix="/courses", tags=["Courses"])


@router.post("/", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
def create_course(course_in: CourseCreate, db: Session = Depends(get_db)):
    return course_service.create(db, course_in)


@router.get("/", response_model=list[CourseRead])
def get_courses(db: Session = Depends(get_db)):
    return course_service.get_all(db)


@router.get("/{course_id}", response_model=CourseRead)
def get_course(course_id: int, db: Session = Depends(get_db)):
    db_course = course_service.get_by_id(db, course_id)
    if db_course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return db_course


@router.put("/{course_id}", response_model=CourseRead)
def update_course(course_id: int, course_in: CourseUpdate, db: Session = Depends(get_db)):
    db_course = course_service.update(db, course_id, course_in)
    if db_course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return db_course


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    db_course = course_service.delete(db, course_id)
    if db_course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return None
