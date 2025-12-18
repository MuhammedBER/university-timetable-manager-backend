from fastapi import FastAPI
from app.routers.professor_routes import router as professor_router
from app.routers.course_routes import router as course_router
from app.routers.room_routes import router as room_router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(professor_router, prefix="/api")
app.include_router(course_router, prefix="/api")
app.include_router(room_router, prefix="/api")





