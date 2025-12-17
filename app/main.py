from fastapi import FastAPI
from app.routers.room_routes import router as room_router

app = FastAPI()

app.include_router(room_router, prefix="/api", tags=["Rooms"])
