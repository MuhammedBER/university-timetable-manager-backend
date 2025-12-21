from sqlalchemy.orm import Session
from app.models.seance import Seance
from typing import List, Dict, Any

class SeanceRepository:
    def bulk_create(self, db: Session, grouped_seances: List[Dict[str, Any]]) -> List[Seance]:
        """
        Takes a list of grouped seances (by field), flattens them, and inserts into DB.
        grouped_seances structure:
        [
            {
                "field_id": 2,
                "schedule": [ { ...seance dict... }, ... ]
            },
            ...
        ]
        """
        all_db_objects = []
        
        for group in grouped_seances:
            schedule = group.get("schedule", [])
            semester = group.get("semester") # Extract semester from group
            field_id = group.get("field_id")
            
            for s in schedule:
                db_obj = Seance(
                    day=s['day'],
                    start_time=s['start_time'],
                    end_time=s['end_time'],
                    user_id=s['user_id'],
                    field_id=field_id, # Use group field_id
                    professor_id=s['professor_id'],
                    course_id=s['course_id'],
                    room_id=s['room_id'],
                    type_id=s['type_id'],
                    semester=semester # Add semester
                )
                db.add(db_obj)
                all_db_objects.append(db_obj)
        
        db.commit()
        # Refreshing all might be expensive, usually just returning success is enough or IDs
        # For now, let's refresh to be safe if number is small
        for obj in all_db_objects:
            db.refresh(obj)
            
        return all_db_objects

seance_repository = SeanceRepository()
