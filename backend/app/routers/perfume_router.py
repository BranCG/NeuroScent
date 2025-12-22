from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.perfume import Perfume, PerfumeVector


router = APIRouter()


@router.get("/perfumes", status_code=status.HTTP_200_OK)
async def get_all_perfumes(
    skip: int = 0,
    limit: int = 50,
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """Get all perfumes with pagination"""
    
    query = db.query(Perfume)
    
    if active_only:
        query = query.filter(Perfume.is_active == True)
    
    perfumes = query.offset(skip).limit(limit).all()
    
    # Format response manually
    result = []
    for perfume in perfumes:
        result.append({
            "id": perfume.id,
            "name": perfume.name,
            "brand": perfume.brand,
            "description": perfume.description,
            "image_url": perfume.image_url,
            "purchase_url": perfume.purchase_url,
            "is_active": perfume.is_active
        })
    
    return result


@router.get("/perfumes/{perfume_id}", status_code=status.HTTP_200_OK)
async def get_perfume(
    perfume_id: str,
    db: Session = Depends(get_db)
):
    """Get perfume by ID"""
    
    perfume = db.query(Perfume).filter(Perfume.id == perfume_id).first()
    
    if not perfume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfume not found"
        )
    
    # Get vector
    vector = db.query(PerfumeVector).filter(PerfumeVector.perfume_id == perfume_id).first()
    
    result = {
        "id": perfume.id,
        "name": perfume.name,
        "brand": perfume.brand,
        "description": perfume.description,
        "image_url": perfume.image_url,
        "purchase_url": perfume.purchase_url,
        "is_active": perfume.is_active
    }
    
    if vector:
        result["vector"] = {
            "intensity": vector.intensity,
            "citrus": vector.citrus,
            "floral": vector.floral,
            "woody": vector.woody,
            "sweet": vector.sweet,
            "spicy": vector.spicy,
            "green": vector.green,
            "aquatic": vector.aquatic
        }
    
    return result
