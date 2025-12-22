import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

from app.core.config import settings

class GeminiService:
    def __init__(self):
        api_key = settings.GEMINI_API_KEY
        if not api_key:
             # Fallback to os.getenv just in case user used API_KEY in env but not in Settings (unlikely given the error)
             # But the error showed gemini_api_key was present.
            api_key = os.getenv("API_KEY")
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-flash-latest')

    def generate_timetable(self, data: dict) -> dict:
        prompt = f"""
        Act as a university timetable scheduler.
        I will provide you with JSON data containing:
        - Professors (with their id, name, weekly hours check 'hours_for_week')
        - Courses (with their id, name, and type constraints if any)
        - Rooms (with their id, capacity, type)
        - Fields (study fields)
        - Types (course types like TP, TD, Cours)
        - Join Tables:
          - course_professors: [{{ "course_id": ..., "professor_id": ... }}, ...] linking courses to eligible professors.
          - course_fields: [{{ "course_id": ..., "field_id": ..., "semester": "S1" }}, ...] linking courses to fields AND semesters.
          - course_types: [{{ "course_id": ..., "type_id": ..., "nbr_hours": ... }}, ...] linking courses to types (TD, TP, Cours) with weekly hours.
        
        Here is the Data:
        {json.dumps(data)}

        YOUR TASK:
        Generate a set of "Seances" (Sessions) that satisfy these constraints:
        1. Professors cannot be in two places at once.
        2. Rooms cannot be used by two classes at once.
        3. Respect the total hours required for each course/professor if specified.
        4. Output MUST be a strictly valid JSON object with a single key "seances".
        5. COVERAGE: You MUST generate a full week of sessions (Monday-Saturday) for EVERY combination of (Field + Semester) present in the input.
        6. GLOBAL CONFLICTS: While generating for each field/semester, ensure that shared resources (Professors and Rooms) are NOT double-booked across different fields/semesters.
        
        DAY CONSTRAINTS:
        The value of "day" must be one of the following only:
        - Monday
        - Tuesday
        - Wednesday
        - Thursday
        - Friday
        - Saturday

        TIME SLOT CONSTRAINTS:
        The timetable must use ONLY these time slots:
        1) start_time: "08:30" — end_time: "10:15"
        2) start_time: "10:30" — end_time: "12:15"
        3) start_time: "14:30" — end_time: "16:15"
        4) start_time: "16:30" — end_time: "18:15"

        OUTPUT JSON FORMAT:
        {{
          "seances": [
            {{
              "field_id": <valid field_id>,
              "semester": "S1",  <-- MUST be one of S1, S2, S3, S4, S5
              "schedule": [
                {{
                  "day": "Monday",
                  "start_time": "08:30",
                  "end_time": "10:15",
                  "user_id": <the user_id associated with the data>,
                  "professor_id": <valid professor_id>,
                  "course_id": <valid course_id>,
                  "room_id": <valid room_id>,
                  "type_id": <valid type_id>
                }}
              ]
            }}
          ]
        }}
        
        IMPORTANT:
        - Group seances by field_id AND semester.
        - Use the IDs provided in the input data.
        - Ensure you assign a valid "type_id" (e.g. for TP, TD, Cours) based on the course_types association.
        - Ensure user_id matches the one found in the input data (all data belongs to one user_id, you can pick it from any entity).
        - Do not include any explanations, markdown formatting (like ```json), or extra text. JUST the JSON object.
        """

        response = self.model.generate_content(prompt)
        
        try:
            # Clean response text if it contains markdown code blocks
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
            
            return json.loads(text)
        except json.JSONDecodeError:
             # Basic error handling, maybe return empty list or raise
            print("Error decoding Gemini response:", response.text)
            return {"seances": []}

gemini_service = GeminiService()
