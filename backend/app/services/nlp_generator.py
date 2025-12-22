from typing import Dict
from app.models.test_result import OlfactoryProfile
from app.models.perfume import Perfume, PerfumeVector


class NLPGenerator:
    """Service for generating personalized descriptions in natural language"""
    
    FAMILY_DESCRIPTIONS = {
        "citrus": "notas cítricas refrescantes",
        "floral": "un corazón floral elegante",
        "woody": "una base amaderada cálida",
        "sweet": "toques dulces envolventes",
        "spicy": "especias que añaden carácter",
        "green": "frescura verde natural",
        "aquatic": "brisa acuática revitalizante"
    }
    
    EMOTION_TEXTS = {
        "freshness": "Te aportará frescura y energía",
        "elegance": "Proyectará elegancia y sofisticación",
        "sensuality": "Evocará sensualidad y calidez",
        "calm": "Transmitirá calma y serenidad",
        "joy": "Inspirará alegría y optimismo",
        "confidence": "Reforzará confianza y poder"
    }
    
    SEASON_TEXTS = {
        "spring": "primavera",
        "summer": "verano",
        "autumn": "otoño",
        "winter": "invierno",
        "all_year": "todo el año"
    }
    
    @staticmethod
    def generate_description(
        user_profile: OlfactoryProfile,
        perfume: Perfume,
        perfume_vector: PerfumeVector,
        affinity_score: float,
        key_matches: Dict[str, float]
    ) -> str:
        """Generate personalized sensory description"""
        
        # Intro based on affinity score
        if affinity_score >= 80:
            intro = "Este perfume encaja perfectamente con tus preferencias."
        elif affinity_score >= 60:
            intro = "Este perfume tiene buena compatibilidad contigo."
        elif affinity_score >= 40:
            intro = "Este perfume podría interesarte, aunque no es tu match ideal."
        else:
            intro = "Este perfume tiene características diferentes a tus preferencias."
        
        # Get dominant families
        dominant_families = sorted(
            key_matches.items(),
            key=lambda x: x[1],
            reverse=True
        )[:2]
        
        # Build sensory description
        sensory_parts = []
        for family, score in dominant_families:
            if score > 0.3:  # Only mention significant families
                sensory_parts.append(NLPGenerator.FAMILY_DESCRIPTIONS.get(family, ""))
        
        if sensory_parts:
            description = f"{intro} Destaca por {', '.join(sensory_parts)}. "
        else:
            description = f"{intro} "
        
        # Add intensity information
        if perfume_vector.intensity and perfume_vector.intensity > 0.7:
            description += "Su presencia es intensa y duradera. "
        elif perfume_vector.intensity and perfume_vector.intensity < 0.3:
            description += "Es una fragancia sutil y discreta. "
        
        # Add emotion
        emotion_key = user_profile.emotion
        if emotion_key and emotion_key in NLPGenerator.EMOTION_TEXTS:
            description += NLPGenerator.EMOTION_TEXTS[emotion_key] + "."
        
        return description
    
    @staticmethod
    def generate_recommendation(
        user_profile: OlfactoryProfile,
        perfume: Perfume,
        perfume_vector: PerfumeVector
    ) -> str:
        """Generate usage recommendation"""
        
        recommendations = []
        
        # Time of day
        suitable_times = perfume_vector.suitable_times or []
        if "morning" in suitable_times:
            recommendations.append("ideal para empezar el día")
        if "night" in suitable_times:
            recommendations.append("perfecto para la noche")
        
        # Occasions
        suitable_occasions = perfume_vector.suitable_occasions or []
        if "work" in suitable_occasions:
            recommendations.append("apropiado para el trabajo")
        if "special_events" in suitable_occasions:
            recommendations.append("excelente para eventos especiales")
        if "romantic" in suitable_occasions:
            recommendations.append("romántico para citas")
        
        # Season
        if perfume_vector.season and perfume_vector.season in NLPGenerator.SEASON_TEXTS:
            season_text = NLPGenerator.SEASON_TEXTS[perfume_vector.season]
            recommendations.append(f"mejor en {season_text}")
        
        if recommendations:
            return "Recomendado " + ", ".join(recommendations) + "."
        else:
            return "Versátil para múltiples ocasiones."
