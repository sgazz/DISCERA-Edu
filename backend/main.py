from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1 import auth, users, documents, tests, ai

# Create database tables
Base.metadata.create_all(bind=engine)

# Create uploads directory
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Digital Intelligent System for Comprehensive Exam Review & Assessment",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["Documents"])
app.include_router(tests.router, prefix="/api/v1/tests", tags=["Tests"])
app.include_router(ai.router, prefix="/api/v1/ai", tags=["AI"])


@app.get("/")
async def root():
    return {
        "message": "Welcome to DISCERA API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "app": settings.APP_NAME}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=settings.DEBUG
    ) 