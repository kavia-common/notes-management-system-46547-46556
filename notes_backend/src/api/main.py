from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.db.session import engine
from src.db.models import Base
from src.api.routes_notes import router as notes_router


openapi_tags = [
    {
        "name": "Notes",
        "description": "Operations for creating, listing, retrieving, updating, and deleting notes.",
    }
]

app = FastAPI(
    title="Notes Backend API",
    description="Backend API for managing notes with SQLite persistence.",
    version="0.1.0",
    openapi_tags=openapi_tags,
)

# CORS: explicitly allow frontend on port 3000 and localhost variants, keep permissive for dev
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://vscode-internal-35107-qa.qa01.cloud.kavia.ai:3000",
    "*",  # Keep permissive in this environment; narrow in production
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
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


@app.get("/", tags=["Notes"], summary="Health Check", description="Health check endpoint to validate service availability.\n\nReturns:\n    JSON object with a simple status message.")
def health_check():
    """
    Health check endpoint to validate service availability.

    Returns:
        JSON object with a simple status message.
    """
    return {"message": "Healthy"}


# Include routes
app.include_router(notes_router)
