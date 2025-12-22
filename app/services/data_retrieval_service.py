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
    def get_all_user_data(self, db: Session, user_id: int, semester_group: int) -> dict:
        # Determine semesters to include
        semesters_to_include = []
        if semester_group == 1:
            semesters_to_include = ["S1", "S3", "S5"]
        elif semester_group == 2:
            semesters_to_include = ["S2", "S4"]

        # Fetch basic data filtered by user_id
        # Note: We fetch ALL first, then will filter courses down based on valid semester association
        all_user_courses = [c for c in course_service.get_all(db) if c.user_id == user_id]
        professors = [p for p in professor_service.get_all(db) if p.user_id == user_id]
        fields = [f for f in field_service.get_all(db) if f.user_id == user_id]
        
        # RoomRepository needs instantiation
        room_repo = RoomRepository(db)
        rooms = [r for r in room_repo.get_all() if r.user_id == user_id]

        # Fetch Types
        types = db.query(Type).all()

        # Fetch Association Data (Join Tables) & Apply Semester Filter
        user_course_ids = [c.id for c in all_user_courses]
        
        course_professors_rows = []
        course_fields_rows = []
        enrollment_rows = []
        
        valid_course_ids = []

        if user_course_ids:
            # 1. Fetch CourseFields filtered by User's Courses AND Selected Semesters
            query = db.query(CourseField).filter(
                CourseField.course_id.in_(user_course_ids)
            )
            
            if semesters_to_include:
                query = query.filter(CourseField.semester.in_(semesters_to_include))
            
            course_fields_rows = query.all()
            
            # 2. Extract Valid Course IDs (those that have a matching semester)
            valid_course_ids = list(set([row.course_id for row in course_fields_rows]))
            
            # 3. Filter other associations by Valid Course IDs
            if valid_course_ids:
                course_professors_rows = db.query(course_professor_association).filter(
                    course_professor_association.c.course_id.in_(valid_course_ids)
                ).all()
                
                enrollment_rows = db.query(Enrollment).filter( 
                    Enrollment.course_id.in_(valid_course_ids)
                ).all()

        # Filter Courses Object List to only those in valid_course_ids
        final_courses = [c for c in all_user_courses if c.id in valid_course_ids]

        # Serialization
        professors_data = [ProfessorRead.model_validate(p).model_dump() for p in professors]
        courses_data = [CourseRead.model_validate(c).model_dump() for c in final_courses]
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
            "courses": courses_data, # Return filtered courses
            "fields": fields_data,
            "rooms": rooms_data,
            "types": types_data,
            "course_professors": course_professors_data,
            "course_fields": course_fields_data,
            "course_types": course_types_data
        }

data_retrieval_service = DataRetrievalService()
