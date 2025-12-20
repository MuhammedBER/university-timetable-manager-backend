from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user_id
from app.schemas.course import CourseCreate, CourseUpdate, CourseRead
from app.services.course_service import course_service


router = APIRouter(prefix="/courses", tags=["Courses"])


@router.post("/", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
def create_course(course_in: CourseCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    course_with_user = CourseCreate(**course_in.model_dump())
    return course_service.create(db, course_with_user, user_id)


@router.get("/", response_model=list[CourseRead])
def get_courses(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    all_courses = course_service.get_all(db)
    return [item for item in all_courses if item.user_id == user_id]


@router.get("/{course_id}", response_model=CourseRead)
def get_course(course_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    db_course = course_service.get_by_id(db, course_id)
    if db_course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    if db_course.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return db_course


@router.put("/{course_id}", response_model=CourseRead)
def update_course(course_id: int, course_in: CourseUpdate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    db_course = course_service.get_by_id(db, course_id)
    if not db_course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    if db_course.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    updated_course = course_service.update(db, course_id, course_in)
    if updated_course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return updated_course


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    db_course = course_service.get_by_id(db, course_id)
    if not db_course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    if db_course.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    db_course = course_service.delete(db, course_id)
    if db_course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return None
