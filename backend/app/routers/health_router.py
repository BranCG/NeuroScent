from fastapi import APIRouter, status
from pydantic import BaseModel
from datetime import datetime


router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response"""
    
    status: str
    timestamp: datetime
    version: str


@router.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "version": "1.0.0"
    }
