from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime


class TestAnswers(BaseModel):
    """Schema for test answers submission"""
    
    q1_intensity: int = Field(..., ge=1, le=5, description="Intensity preference (1-5)")
    q2_preferred_families: List[str] = Field(..., min_length=1, max_length=7)
    q3_rejected_families: Optional[List[str]] = Field(default=[])
    q4_emotion: str = Field(..., description="Desired emotion")
    q5_time_of_day: List[str] = Field(..., min_length=1)
    q6_occasions: List[str] = Field(..., min_length=1)
    q7_season: str = Field(..., description="Preferred season")
    q8_longevity: int = Field(..., ge=1, le=5, description="Longevity preference (1-5)")
    q9_concentration: Optional[str] = Field(default=None)
    q10_reference: Optional[str] = Field(default=None, description="Reference perfume name")
    session_id: str = Field(..., description="User session identifier")
    
    class Config:
        json_schema_extra = {
            "example": {
                "q1_intensity": 3,
                "q2_preferred_families": ["citrus", "aquatic", "woody"],
                "q3_rejected_families": ["sweet"],
                "q4_emotion": "freshness",
                "q5_time_of_day": ["morning", "afternoon"],
                "q6_occasions": ["work", "daily"],
                "q7_season": "summer",
                "q8_longevity": 4,
                "q9_concentration": "eau_de_toilette",
                "q10_reference": None,
                "session_id": "abc123xyz"
            }
        }


class OlfactoryProfileResponse(BaseModel):
    """Schema for olfactory profile response"""
    
    id: str
    intensity: float
    citrus: float
    floral: float
    woody: float
    sweet: float
    spicy: float
    green: float
    aquatic: float
    emotion: Optional[str]
    season: Optional[str]
    
    class Config:
        from_attributes = True


class TestResultResponse(BaseModel):
    """Schema for test result response"""
    
    id: str
    user_id: str
    completed_at: datetime
    profile: OlfactoryProfileResponse
    
    class Config:
        from_attributes = True
