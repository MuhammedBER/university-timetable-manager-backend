from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user_id
from app.repository.seance_repository import seance_repository
from typing import List, Dict, Any

router = APIRouter(prefix="/seances", tags=["Seances"])

@router.post("/bulk")
def bulk_create_seances(
    seances_data: Dict[str, List[Dict[str, Any]]], # Expecting {"seances": [...]}
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """
    Bulk create seances from ID-based JSON.
    Payload: { "seances": [ { "field_id": X, "schedule": [...] }, ... ] }
    """
    try:
        grouped_seances = seances_data.get("seances", [])
        if not grouped_seances:
             raise HTTPException(status_code=400, detail="No seances provided")
             
        created_seances = seance_repository.bulk_create(db, grouped_seances)
        return {"message": "Seances created successfully", "count": len(created_seances)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/")
def delete_all_seances(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """
    Deletes all seances for the current user.
    """
    try:
        seance_repository.delete_all(db, user_id)
        return {"message": "All seances deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
