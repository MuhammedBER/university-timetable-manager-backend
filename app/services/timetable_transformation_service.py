from typing import List, Dict, Any

class TimetableTransformationService:
    def transform_for_frontend(self, raw_seances_groups: List[Dict[str, Any]], lookups: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transforms grouped seances from Gemini into two structures:
        1. raw_seances: ID-based (for DB) - passed through as is (mostly)
        2. display_timetable: Display-based (for Frontend) - IDs replaced with names
        """
        display_timetable = []
        
        # Lookups
        fields_map = {f['id']: f['name'] for f in lookups['fields']}
        professors_map = {p['id']: f"{p['first_name']} {p['last_name']}" for p in lookups['professors']}
        courses_map = {c['id']: c['name'] for c in lookups['courses']}
        rooms_map = {r['id']: str(r['num']) for r in lookups['rooms']}
        types_map = {t['id']: t['name'] for t in lookups['types']}

        for group in raw_seances_groups:
            field_id = group.get('field_id')
            semester = group.get('semester')
            schedule = group.get('schedule', [])
            
            field_name = fields_map.get(field_id, f"Field {field_id}")
            
            display_group = {
                "field": field_name,
                "semester": semester,
                "schedule": []
            }
            
            for s in schedule:
                display_seance = {
                    "day": s.get('day'),
                    "start_time": s.get('start_time'),
                    "end_time": s.get('end_time'),
                    "course": courses_map.get(s.get('course_id'), str(s.get('course_id'))),
                    "professor": professors_map.get(s.get('professor_id'), str(s.get('professor_id'))),
                    "room": rooms_map.get(s.get('room_id'), str(s.get('room_id'))),
                }
                # Add type if available
                if 'type_id' in s:
                    display_seance['type'] = types_map.get(s.get('type_id'), str(s.get('type_id')))
                
                display_group["schedule"].append(display_seance)
            
            display_timetable.append(display_group)

        return {
            "raw_seances": {"seances": raw_seances_groups},
            "display_timetable": {"timetable": display_timetable}
        }

timetable_transformation_service = TimetableTransformationService()
