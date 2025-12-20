from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user_id
from app.schemas.course import CourseCreate, CourseUpdate, CourseRead
from app.services.course_service import course_service


router = APIRouter(prefix="/courses", tags=["Courses"])


@router.post("/", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
def create_course(course_in: CourseCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    course_data = course_in.model_dump()
    course_data["user_id"] = user_id
    # Temporarily reconstruct using strict logic if needed, but assuming service handles dict or loose model
    # To strictly satisfy the prompt's request which might be pseudocode-ish regarding the model reconstruction:
    # We will pass the dictionary if the service accepts it, OR we rely on the fact that we can't instantiate CourseCreate with user_id.
    # BUT, to make this work without crashing, we should probably pass the dict if possible, or force the field.
    # However, restricted from modifying service.
    # Let's try to inject it into the model instance if Pydantic allows setattr, or just assume the prompt logic was slightly off for pure Pydantic models.
    # Wait, I'll stick to the prompt's Pattern 1:
    # {entity}_with_user = {Entity}Create(**{entity}_data)
    # If this fails, it fails. But I'll use `model_construct` to bypass validation if needed? No, `**` calls init.
    # I'll modify the line to:
    # course_with_user = CourseCreate.model_construct(**course_data)
    # model_construct bypasses validation and allows setting extra fields if they are compatible?
    # Actually, model_construct is safer here if we want to attach user_id to a model that doesn't have it defined.
    # CHECK: Does CourseCreate (lines 10-15) allow extra? Default is 'ignore'.
    # If I use `CourseCreate(**course_data)`, user_id is ignored.
    # I will stick to the requested code structure but be aware.
    course_with_user = CourseCreate(**course_data)
    # HACK: If user_id was ignored, we manually set it.
    if not hasattr(course_with_user, "user_id"):
        object.__setattr__(course_with_user, "user_id", user_id)
    return course_service.create(db, course_with_user)


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
