from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.db import Base, engine
from app.models import field  # pour que les tables soient connues
from app.routers import field_route as field_router


# Création des tables (si Alembic n’est pas encore utilisé)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Gestion Emplois Backend",
    version="1.0.0",
    description="API pour la gestion des filières (fields), emplois du temps, etc."
)

# CORS pour autoriser le frontend React
origins = [
    "http://localhost:3000",  # create-react-app
    "http://localhost:5173",  # Vite (si jamais)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "API backend is running"}


# Enregistrer ton router Field sous /api/v1/fields/...
app.include_router(field_router.router, prefix="/api/v1")
