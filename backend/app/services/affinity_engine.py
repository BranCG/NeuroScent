from typing import Dict, List, Tuple
import numpy as np
from app.models.test_result import OlfactoryProfile
from app.models.perfume import PerfumeVector, Perfume


class AffinityEngine:
    """Service for calculating affinity between user profiles and perfumes"""
    
    @staticmethod
    def cosine_similarity(vector_a: List[float], vector_b: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        vec_a = np.array(vector_a)
        vec_b = np.array(vector_b)
        
        dot_product = np.dot(vec_a, vec_b)
        magnitude_a = np.linalg.norm(vec_a)
        magnitude_b = np.linalg.norm(vec_b)
        
        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0
        
        return float(dot_product / (magnitude_a * magnitude_b))
    
    @staticmethod
    def check_rejected_families(
        rejected: List[str], 
        perfume_vector: PerfumeVector
    ) -> float:
        """
        Check if perfume contains rejected families.
        Returns rejection score (0-1), where 1 = highly rejected.
        """
        if not rejected:
            return 0.0
        
        family_map = {
            "citrus": perfume_vector.citrus or 0.0,
            "floral": perfume_vector.floral or 0.0,
            "woody": perfume_vector.woody or 0.0,
            "sweet": perfume_vector.sweet or 0.0,
            "spicy": perfume_vector.spicy or 0.0,
            "green": perfume_vector.green or 0.0,
            "aquatic": perfume_vector.aquatic or 0.0
        }
        
        rejection_intensity = 0.0
        for family in rejected:
            family_lower = family.lower()
            for key in family_map:
                if key in family_lower:
                    rejection_intensity += family_map[key]
        
        return min(rejection_intensity / max(len(rejected), 1), 1.0)
    
    @staticmethod
    def calculate_context_match(
        user_occasions: List[str],
        user_times: List[str],
        user_season: str,
        perfume_occasions: List[str],
        perfume_times: List[str],
        perfume_season: str
    ) -> float:
        """Calculate context matching score"""
        # Occasion matching
        if user_occasions and perfume_occasions:
            occasion_matches = len(set(user_occasions) & set(perfume_occasions))
            occasion_score = occasion_matches / max(len(user_occasions), 1)
        else:
            occasion_score = 0.5  # Neutral if data missing
        
        # Time matching
        if user_times and perfume_times:
            time_matches = len(set(user_times) & set(perfume_times))
            time_score = time_matches / max(len(user_times), 1)
        else:
            time_score = 0.5
        
        # Season matching
        if user_season and perfume_season:
            season_score = 1.0 if (user_season == perfume_season or perfume_season == "all_year") else 0.5
        else:
            season_score = 0.5
        
        # Weighted average
        return (occasion_score * 0.4 + time_score * 0.4 + season_score * 0.2)
    
    @staticmethod
    def calculate_affinity(
        user_profile: OlfactoryProfile,
        perfume: Perfume,
        perfume_vector: PerfumeVector
    ) -> Tuple[float, Dict[str, float]]:
        """
        Calculate affinity score between user profile and perfume.
        
        Returns:
            Tuple of (affinity_score, key_matches_dict)
        """
        # 1. Check for rejected families (immediate disqualification)
        rejection_score = AffinityEngine.check_rejected_families(
            user_profile.rejected_families or [],
            perfume_vector
        )
        
        if rejection_score > 0.7:  # More than 70% match with rejected families
            return 0.0, {}
        
        # 2. Vector similarity (40% weight)
        user_vector = user_profile.to_vector()
        perfume_vec = perfume_vector.to_vector()
        vector_similarity = AffinityEngine.cosine_similarity(user_vector, perfume_vec)
        weighted_vector_score = vector_similarity * 0.40
        
        # 3. Context match (30% weight)
        context_score = AffinityEngine.calculate_context_match(
            user_occasions=user_profile.occasions or [],
            user_times=user_profile.time_of_day or [],
            user_season=user_profile.season or "",
            perfume_occasions=perfume_vector.suitable_occasions or [],
            perfume_times=perfume_vector.suitable_times or [],
            perfume_season=perfume_vector.season or ""
        )
        weighted_context_score = context_score * 0.30
        
        # 4. Intensity and longevity match (20% weight)
        intensity_match = 1 - abs((user_profile.intensity or 0.5) - (perfume_vector.intensity or 0.5))
        longevity_match = 1 - abs((user_profile.longevity or 0.5) - (perfume_vector.longevity or 0.5))
        persistence_score = (intensity_match + longevity_match) / 2
        weighted_persistence_score = persistence_score * 0.20
        
        # 5. Emotion match (10% weight) - simplified for MVP
        emotion_score = 0.5  # Neutral for now, can be enhanced with emotion-to-profile mapping
        weighted_emotion_score = emotion_score * 0.10
        
        # 6. Calculate final score
        final_score = (
            weighted_vector_score +
            weighted_context_score +
            weighted_persistence_score +
            weighted_emotion_score
        ) * 100
        
        # Apply rejection penalty
        final_score = final_score * (1 - rejection_score * 0.3)
        
        # Get key matches for description generation
        key_matches = {
            "citrus": min((user_profile.citrus or 0) * (perfume_vector.citrus or 0), 1.0),
            "floral": min((user_profile.floral or 0) * (perfume_vector.floral or 0), 1.0),
            "woody": min((user_profile.woody or 0) * (perfume_vector.woody or 0), 1.0),
            "sweet": min((user_profile.sweet or 0) * (perfume_vector.sweet or 0), 1.0),
            "spicy": min((user_profile.spicy or 0) * (perfume_vector.spicy or 0), 1.0),
            "green": min((user_profile.green or 0) * (perfume_vector.green or 0), 1.0),
            "aquatic": min((user_profile.aquatic or 0) * (perfume_vector.aquatic or 0), 1.0)
        }
        
        return round(final_score, 2), key_matches
