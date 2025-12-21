from sqlalchemy.orm import Session
from app.services.professor_service import professor_service
from app.services.course_service import course_service
from app.services.field_service import field_service
from app.repository.room_repository import RoomRepository
from app.models.type import Type
from app.models.enrollment import Enrollment
from app.models.course_professor import course_professor_association
from app.models.course_field import CourseField
from app.schemas.professor import ProfessorRead
from app.schemas.course import CourseRead
from app.schemas.field import FieldRead
from app.schemas.room import RoomRead
from app.schemas.shared import TypeSimple

class DataRetrievalService:
    def get_all_user_data(self, db: Session, user_id: int) -> dict:
        # Fetch data filtered by user_id
        professors = [p for p in professor_service.get_all(db) if p.user_id == user_id]
        courses = [c for c in course_service.get_all(db) if c.user_id == user_id]
        fields = [f for f in field_service.get_all(db) if f.user_id == user_id]
        
        # RoomRepository needs instantiation
        room_repo = RoomRepository(db)
        rooms = [r for r in room_repo.get_all() if r.user_id == user_id]

        # Fetch Types
        types = db.query(Type).all()

        # Fetch Association Data (Join Tables)
        # Filter by courses belonging to the user
        course_ids = [c.id for c in courses]
        
        course_professors_rows = []
        course_fields_rows = []
        enrollment_rows = []
        
        if course_ids:
            course_professors_rows = db.query(course_professor_association).filter(
                course_professor_association.c.course_id.in_(course_ids)
            ).all()
            
            course_fields_rows = db.query(CourseField).filter(
                CourseField.course_id.in_(course_ids)
            ).all()
            
            enrollment_rows = db.query(Enrollment).filter( 
                Enrollment.course_id.in_(course_ids)
            ).all()

        # Serialization
        professors_data = [ProfessorRead.model_validate(p).model_dump() for p in professors]
        courses_data = [CourseRead.model_validate(c).model_dump() for c in courses]
        fields_data = [FieldRead.model_validate(f).model_dump() for f in fields]
        rooms_data = [RoomRead.model_validate(r).model_dump() for r in rooms]
        types_data = [TypeSimple.model_validate(t).model_dump() for t in types]
        
        # Manually serialize association rows
        course_professors_data = [{"course_id": row.course_id, "professor_id": row.professor_id} for row in course_professors_rows]
        course_fields_data = [{"course_id": row.course_id, "field_id": row.field_id, "semester": row.semester} for row in course_fields_rows]
        # Serialize Enrollments (Type association with hours)
        course_types_data = [{"course_id": e.course_id, "type_id": e.type_id, "nbr_hours": e.nbr_hours} for e in enrollment_rows]

        return {
            "professors": professors_data,
            "courses": courses_data,
            "fields": fields_data,
            "rooms": rooms_data,
            "types": types_data,
            "course_professors": course_professors_data,
            "course_fields": course_fields_data,
            "course_types": course_types_data
        }

data_retrieval_service = DataRetrievalService()
