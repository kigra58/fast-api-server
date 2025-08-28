import os
from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.middleware import setup_middleware
from app.api.v1.api import api_router
from app.db.session import engine
from app.db.base import Base


# Setup logging
setup_logging()

# Setup Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Create tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="User Management API with FastAPI",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Setup custom middleware
setup_middleware(app)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root(request: Request):
    logger.info("Root endpoint accessed")
    return templates.TemplateResponse("welcome.html", {"request": request, "message": "Welcome to the FastAPI application on staging environment!"})

@app.get("/health")
def health_check():
    logger.info("Health check endpoint accessed")
    return {"status": "healthy"}

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown")
