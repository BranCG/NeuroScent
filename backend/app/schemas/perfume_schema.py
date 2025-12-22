from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class PerfumeBase(BaseModel):
    """Base schema for perfume"""
    
    name: str = Field(..., max_length=255)
    brand: str = Field(..., max_length=255)
    description: Optional[str] = None
    image_url: Optional[str] = None
    purchase_url: Optional[str] = None


class PerfumeCreate(PerfumeBase):
    """Schema for creating a perfume"""
    pass


class PerfumeVectorBase(BaseModel):
    """Base schema for perfume vector"""
    
    intensity: float = Field(..., ge=0.0, le=1.0)
    citrus: float = Field(default=0.0, ge=0.0, le=1.0)
    floral: float = Field(default=0.0, ge=0.0, le=1.0)
    woody: float = Field(default=0.0, ge=0.0, le=1.0)
    sweet: float = Field(default=0.0, ge=0.0, le=1.0)
    spicy: float = Field(default=0.0, ge=0.0, le=1.0)
    green: float = Field(default=0.0, ge=0.0, le=1.0)
    aquatic: float = Field(default=0.0, ge=0.0, le=1.0)
    suitable_occasions: List[str] = Field(default=[])
    suitable_times: List[str] = Field(default=[])
    season: Optional[str] = None
    longevity: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    concentration: Optional[str] = None


class PerfumeVectorResponse(PerfumeVectorBase):
    """Schema for perfume vector response"""
    
    id: str
    perfume_id: str
    
    class Config:
        from_attributes = True


class PerfumeResponse(PerfumeBase):
    """Schema for perfume response"""
    
    id: str
    is_active: bool
    created_at: datetime
    vector: Optional[PerfumeVectorResponse] = None
    
    class Config:
        from_attributes = True


class AffinityResultResponse(BaseModel):
    """Schema for affinity result"""
    
    perfume: PerfumeResponse
    affinity: dict = Field(..., description="Affinity details including score, level, description, and recommendation")
    
    class Config:
        json_schema_extra = {
            "example": {
                "perfume": {
                    "id": "uuid-string",
                    "name": "Acqua di Giò",
                    "brand": "Giorgio Armani",
                    "image_url": "http://example.com/image.jpg",
                    "purchase_url": "http://example.com/buy"
                },
                "affinity": {
                    "score": 87.5,
                    "level": "excellent",
                    "description": "Este perfume encaja perfectamente...",
                    "recommendation": "Recomendado ideal para empezar el día..."
                }
            }
        }
