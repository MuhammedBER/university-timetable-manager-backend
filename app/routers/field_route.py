from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user_id
from app.schemas.field import FieldCreate, FieldUpdate, FieldRead
from app.services.field_service import field_service


router = APIRouter(
    prefix="/fields",
    tags=["Fields"],
)


@router.post(
    "/",
    response_model=FieldRead,
    status_code=status.HTTP_201_CREATED,
)
def create_field(
    field_in: FieldCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    field_with_user = FieldCreate(**field_in.model_dump())
    db_field = field_service.create(db, field_with_user, user_id)
    if db_field is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Field already exists for this user and university year",
        )
    return db_field


@router.get(
    "/",
    response_model=list[FieldRead],
)
def get_fields(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    all_fields = field_service.get_all(db)
    return [item for item in all_fields if item.user_id == user_id]


@router.get(
    "/{field_id}",
    response_model=FieldRead,
)
def get_field(
    field_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    db_field = field_service.get_by_id(db, field_id)
    if db_field is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Field not found",
        )
    if db_field.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return db_field


@router.put(
    "/{field_id}",
    response_model=FieldRead,
)
def update_field(
    field_id: int,
    field_in: FieldUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    db_field = field_service.get_by_id(db, field_id)
    if not db_field:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Field not found")
    if db_field.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    db_field = field_service.update(db, field_id, field_in)
    if db_field is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Field not found",
        )
    return db_field


@router.delete(
    "/{field_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_field(
    field_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    db_field = field_service.get_by_id(db, field_id)
    if not db_field:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Field not found")
    if db_field.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    db_field = field_service.delete(db, field_id)
    if db_field is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Field not found",
        )
    return None