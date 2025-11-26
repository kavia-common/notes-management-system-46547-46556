from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.db.session import engine
from src.db.models import Base


app = FastAPI(
    title="Notes Backend API",
    description="Backend API for managing notes with SQLite persistence.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Development-friendly CORS; adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    """
    FastAPI startup hook to initialize the database schema.

    Creates all tables if they do not exist, ensuring the SQLite DB is ready
    without requiring migrations for development environments.
    """
    Base.metadata.create_all(bind=engine)


@app.get("/")
def health_check():
    """
    Health check endpoint to validate service availability.

    Returns:
        JSON object with a simple status message.
    """
    return {"message": "Healthy"}
