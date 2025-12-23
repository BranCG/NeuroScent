from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.test_schema import TestAnswers, TestResultResponse
from app.schemas.perfume_schema import AffinityResultResponse
from app.models.user import User
from app.models.test_result import TestResult, OlfactoryProfile
from app.models.perfume import Perfume, PerfumeVector, AffinityResult
from app.services.test_engine import TestEngine
from app.services.affinity_engine import AffinityEngine
from app.services.nlp_generator import NLPGenerator


router = APIRouter()


@router.post("/test/calculate", response_model=dict, status_code=status.HTTP_200_OK)
async def calculate_affinity(
    test_data: TestAnswers,
    db: Session = Depends(get_db)
):
    """
    Calculate affinity for submitted test answers.
    
    Returns top perfume recommendations with affinity scores.
    """
    
    # 1. Validate answers
    is_valid, errors = TestEngine.validate_answers(test_data.model_dump())
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Invalid test answers", "errors": errors}
        )
    
    # 2. Get or create user
    user = db.query(User).filter(User.session_id == test_data.session_id).first()
    if not user:
        user = User(session_id=test_data.session_id)
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # 3. Save test result
    test_result = TestResult(
        user_id=user.id,
        answers=test_data.model_dump()
    )
    db.add(test_result)
    db.commit()
    db.refresh(test_result)
    
    # 4. Build olfactory profile
    profile_data = TestEngine.build_profile(test_data.model_dump())
    profile = OlfactoryProfile(
        test_result_id=test_result.id,
        **profile_data
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    
    # 5. Get active perfumes filtered by gender (include unisex for both)
    user_gender = test_data.q0_gender  # "male" or "female"
    perfumes = db.query(Perfume).filter(
        Perfume.is_active == True,
        Perfume.gender.in_([user_gender, "unisex"])
    ).all()
    
    if not perfumes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No perfumes available for matching"
        )
    
    # 6. Calculate affinity for each perfume
    affinity_results = []
    
    for perfume in perfumes:
        # Get perfume vector
        perfume_vector = db.query(PerfumeVector).filter(
            PerfumeVector.perfume_id == perfume.id
        ).first()
        
        if not perfume_vector:
            continue
        
        # Calculate affinity
        affinity_score, key_matches = AffinityEngine.calculate_affinity(
            profile, perfume, perfume_vector
        )
        
        # Generate description and recommendation
        description = NLPGenerator.generate_description(
            profile, perfume, perfume_vector, affinity_score, key_matches
        )
        
        recommendation = NLPGenerator.generate_recommendation(
            profile, perfume, perfume_vector
        )
        
        # Determine affinity level
        if affinity_score >= 80:
            level = "excellent"
        elif affinity_score >= 60:
            level = "good"
        elif affinity_score >= 40:
            level = "moderate"
        else:
            level = "low"
        
        # Save affinity result
        affinity_result = AffinityResult(
            profile_id=profile.id,
            perfume_id=perfume.id,
            affinity_score=affinity_score,
            personalized_description=description,
            usage_recommendation=recommendation
        )
        db.add(affinity_result)
        
        affinity_results.append({
            "perfume": perfume,
            "perfume_vector": perfume_vector,
            "affinity_score": affinity_score,
            "level": level,
            "description": description,
            "recommendation": recommendation
        })
    
    db.commit()
    
    # 7. Sort by affinity score and get top 3
    affinity_results.sort(key=lambda x: x["affinity_score"], reverse=True)
    top_results = affinity_results[:3]
    
    # 8. Format response
    results = []
    for result in top_results:
        results.append({
            "perfume": {
                "id": str(result["perfume"].id),
                "name": result["perfume"].name,
                "brand": result["perfume"].brand,
                "description": result["perfume"].description,
                "image_url": result["perfume"].image_url,
                "purchase_url": result["perfume"].purchase_url
            },
            "affinity": {
                "score": result["affinity_score"],
                "level": result["level"],
                "description": result["description"],
                "recommendation": result["recommendation"]
            }
        })
    
    return {
        "status": "success",
        "data": {
            "test_id": str(test_result.id),
            "user_id": str(user.id),
            "profile_id": str(profile.id),
            "olfactory_profile": {
                "id": str(profile.id),
                "intensity": profile.intensity,
                "citrus": profile.citrus,
                "floral": profile.floral,
                "woody": profile.woody,
                "sweet": profile.sweet,
                "spicy": profile.spicy,
                "green": profile.green,
                "aquatic": profile.aquatic,
                "emotion": profile.emotion,
                "season": profile.season
            },
            "results": results,
            "metadata": {
                "total_perfumes_analyzed": len(perfumes),
                "top_match_count": len(results),
                "test_completed_at": test_result.completed_at.isoformat()
            }
        }
    }


@router.get("/test/{test_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def get_test_result(
    test_id: str,
    db: Session = Depends(get_db)
):
    """Get test results by test ID"""
    
    test_result = db.query(TestResult).filter(TestResult.id == test_id).first()
    
    if not test_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test result not found"
        )
    
    # Get profile
    profile = db.query(OlfactoryProfile).filter(
        OlfactoryProfile.test_result_id == test_id
    ).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Olfactory profile not found"
        )
    
    # Get affinity results
    affinity_results = db.query(AffinityResult).filter(
        AffinityResult.profile_id == profile.id
    ).order_by(AffinityResult.affinity_score.desc()).limit(3).all()
    
    results = []
    for affinity in affinity_results:
        perfume = db.query(Perfume).filter(Perfume.id == affinity.perfume_id).first()
        
        if perfume:
            results.append({
                "perfume": {
                    "id": str(perfume.id),
                    "name": perfume.name,
                    "brand": perfume.brand,
                    "description": perfume.description,
                    "image_url": perfume.image_url,
                    "purchase_url": perfume.purchase_url
                },
                "affinity": {
                    "score": affinity.affinity_score,
                    "level": "excellent" if affinity.affinity_score >= 80 else "good" if affinity.affinity_score >= 60 else "moderate",
                    "description": affinity.personalized_description,
                    "recommendation": affinity.usage_recommendation
                }
            })
    
    return {
        "status": "success",
        "data": {
            "test_id": str(test_result.id),
            "user_id": str(test_result.user_id),
            "profile_id": str(profile.id),
            "olfactory_profile": {
                "id": str(profile.id),
                "intensity": profile.intensity,
                "citrus": profile.citrus,
                "floral": profile.floral,
                "woody": profile.woody,
                "sweet": profile.sweet,
                "spicy": profile.spicy,
                "green": profile.green,
                "aquatic": profile.aquatic,
                "emotion": profile.emotion,
                "season": profile.season
            },
            "results": results,
            "metadata": {
                "top_match_count": len(results),
                "test_completed_at": test_result.completed_at.isoformat()
            }
        }
    }
