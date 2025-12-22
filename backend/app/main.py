from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import test_router, perfume_router, health_router
from app.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    debug=settings.DEBUG
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router.router, prefix=settings.API_V1_STR, tags=["health"])
app.include_router(test_router.router, prefix=settings.API_V1_STR, tags=["test"])
app.include_router(perfume_router.router, prefix=settings.API_V1_STR, tags=["perfumes"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "NeuroScent API",
        "version": "1.0.0",
        "docs": f"{settings.API_V1_STR}/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
