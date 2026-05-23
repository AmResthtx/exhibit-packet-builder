"""Main FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from loguru import logger

from config import settings

# Create upload and temp directories if they don't exist
Path(settings.UPLOAD_DIR).mkdir(exist_ok=True)
Path(settings.TEMP_DIR).mkdir(exist_ok=True)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="An intelligent tool for building legal exhibit packets",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers
from routes import files, exhibits, rules, packets

# Include routers
app.include_router(
    files.router,
    prefix=f"{settings.API_V1_PREFIX}/files",
    tags=["files"],
)
app.include_router(
    exhibits.router,
    prefix=f"{settings.API_V1_PREFIX}/exhibits",
    tags=["exhibits"],
)
app.include_router(
    rules.router,
    prefix=f"{settings.API_V1_PREFIX}/rules",
    tags=["rules"],
)
app.include_router(
    packets.router,
    prefix=f"{settings.API_V1_PREFIX}/packets",
    tags=["packets"],
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Exhibit Packet Builder",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "app": settings.APP_NAME}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
