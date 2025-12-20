from fastapi import FastAPI
from app.routers.professor_routes import router as professor_router
from app.routers.course_routes import router as course_router
from app.routers.room_routes import router as room_router
from fastapi.middleware.cors import CORSMiddleware
from app.routers.room_routes import router as room_router
from app.routers.auth import router as auth_router
from app.routers.user import router as user_router
from app.routers.field_route import router as field_router
from app.routers.time_table_routes import router as time_table_router
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(auth_router)
app.include_router(user_router, prefix="/api", tags=["Users"])
app.include_router(professor_router, prefix="/api")
app.include_router(course_router, prefix="/api")
app.include_router(room_router, prefix="/api")
app.include_router(field_router, prefix="/api")
app.include_router(time_table_router, prefix="/api")