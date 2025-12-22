from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user_id
from app.services.data_retrieval_service import data_retrieval_service
from app.services.gemini_service import gemini_service
from app.services.timetable_transformation_service import timetable_transformation_service

router = APIRouter(prefix="/generation", tags=["Generation"])

@router.get("/data")
def get_user_data_for_generation(
    semester_group: int = 1,
    db: Session = Depends(get_db), 
    user_id: int = Depends(get_current_user_id)
):
    """
    Retrieves all user-specific data formatted for Gemini.
    Used for testing the data retrieval service.
    """
    try:
        data = data_retrieval_service.get_all_user_data(db, user_id, semester_group)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate")
def generate_timetable(
    semester_group: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """
    1. Retrieves user data filtered by semester_group (1: S1/S3/S5, 2: S2/S4).
    2. Sends data to Gemini.
    3. Returns Grouped & Transformed JSON for Frontend.
    """
    try:
        # Step 1: Get Data
        data = data_retrieval_service.get_all_user_data(db, user_id, semester_group)
        
        # Step 2: Generate Timetable
        generated_response = gemini_service.generate_timetable(data)
        raw_seances = generated_response.get("seances", [])
        
        # Step 3: Transform Data (ID-based & Display-based)
        transformed_data = timetable_transformation_service.transform_for_frontend(raw_seances, data)
        
        return transformed_data
    except ValueError as ve:
        raise HTTPException(status_code=500, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")
