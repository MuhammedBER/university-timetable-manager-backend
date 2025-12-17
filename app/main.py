from fastapi import FastAPI
<<<<<<< HEAD
from app.routers.professor_routes import router as professor_router
from app.routers.course_routes import router as course_router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(professor_router)
app.include_router(course_router)


@app.get("/")
def read_root():
    return {"message": "Hello World"}
=======
from app.routers.room_routes import router as room_router

app = FastAPI()

app.include_router(room_router, prefix="/api", tags=["Rooms"])
>>>>>>> mohamed
