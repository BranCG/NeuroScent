from typing import Dict, List, Any
from app.models.test_result import OlfactoryProfile


class TestEngine:
    """Service for processing test answers and building olfactory profiles"""
    
    @staticmethod
    def build_profile(answers: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build olfactory profile from test answers.
        
        Args:
            answers: Dictionary containing test answers
            
        Returns:
            Dictionary with profile data ready for OlfactoryProfile model
        """
        profile_data = {
            "intensity": 0.0,
            "citrus": 0.0,
            "floral": 0.0,
            "woody": 0.0,
            "sweet": 0.0,
            "spicy": 0.0,
            "green": 0.0,
            "aquatic": 0.0,
            "rejected_families": [],
            "emotion": None,
            "time_of_day": [],
            "occasions": [],
            "season": None,
            "longevity": 0.0,
            "concentration": None,
            "reference_perfume": None
        }
        
        # Question 1: Intensity (1-5 scale)
        if "q1_intensity" in answers:
            profile_data["intensity"] = (answers["q1_intensity"] - 1) / 4  # Normalize to 0-1
        
        # Question 2: Preferred families (multiple choice)
        if "q2_preferred_families" in answers:
            families = answers["q2_preferred_families"]
            for family in families:
                family_key = family.lower().replace(" ", "_")
                # Map display names to vector keys
                family_map = {
                    "citrus": "citrus",
                    "floral": "floral",
                    "woody": "woody",
                    "sweet": "sweet",
                    "spicy": "spicy",
                    "green": "green",
                    "aquatic": "aquatic"
                }
                for key, value in family_map.items():
                    if key in family_key:
                        profile_data[value] = 1.0
        
        # Question 3: Rejected families
        if "q3_rejected_families" in answers:
            profile_data["rejected_families"] = answers["q3_rejected_families"]
        
        # Question 4: Emotion
        if "q4_emotion" in answers:
            profile_data["emotion"] = answers["q4_emotion"]
        
        # Question 5: Time of day
        if "q5_time_of_day" in answers:
            profile_data["time_of_day"] = answers["q5_time_of_day"]
        
        # Question 6: Occasions
        if "q6_occasions" in answers:
            profile_data["occasions"] = answers["q6_occasions"]
        
        # Question 7: Season
        if "q7_season" in answers:
            profile_data["season"] = answers["q7_season"]
        
        # Question 8: Longevity (1-5 scale)
        if "q8_longevity" in answers:
            profile_data["longevity"] = (answers["q8_longevity"] - 1) / 4  # Normalize to 0-1
        
        # Question 9: Concentration type
        if "q9_concentration" in answers:
            profile_data["concentration"] = answers["q9_concentration"]
        
        # Question 10: Reference perfume
        if "q10_reference" in answers:
            profile_data["reference_perfume"] = answers["q10_reference"]
        
        return profile_data
    
    @staticmethod
    def validate_answers(answers: Dict[str, Any]) -> tuple[bool, List[str]]:
        """
        Validate test answers.
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        required_questions = ["q1_intensity", "q2_preferred_families", "q4_emotion", 
                            "q5_time_of_day", "q6_occasions", "q7_season", "q8_longevity"]
        
        for question in required_questions:
            if question not in answers or answers[question] is None:
                errors.append(f"Missing required answer: {question}")
        
        # Validate intensity range
        if "q1_intensity" in answers:
            if not (1 <= answers["q1_intensity"] <= 5):
                errors.append("Intensity must be between 1 and 5")
        
        # Validate longevity range
        if "q8_longevity" in answers:
            if not (1 <= answers["q8_longevity"] <= 5):
                errors.append("Longevity must be between 1 and 5")
        
        return len(errors) == 0, errors
