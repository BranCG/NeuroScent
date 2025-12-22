"""
Script para poblar la base de datos de NeuroScent con perfumes árabes.
Ejecutar después de tener la base de datos configurada.
"""

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base

# Import ALL models to ensure they are registered with Base
from app.models.user import User
from app.models.test_result import TestResult, OlfactoryProfile
from app.models.perfume import Perfume, PerfumeVector, AffinityResult
import uuid

# Crear todas las tablas si no existen
Base.metadata.create_all(bind=engine)

# Datos de perfumes árabes con vectores olfativos
PERFUMES_DATA = [
    {
        "name": "Bharara King",
        "brand": "Bharara",
        "description": "Aromático frutal amaderado masculino popular con gran proyección y longevidad.",
        "vector": {
            "intensity": 0.8,
            "citrus": 0.3,
            "floral": 0.2,
            "woody": 0.8,
            "sweet": 0.6,
            "spicy": 0.5,
            "green": 0.3,
            "aquatic": 0.1,
            "suitable_occasions": ["special_events", "night", "romantic"],
            "suitable_times": ["night", "afternoon"],
            "season": "autumn",
            "longevity": 0.9,
            "concentration": "eau_de_parfum"
        }
    },
    {
        "name": "Vulcan Feu",
        "brand": "ORIENTFRAGANCE",
        "description": "Perfume árabe con notas tropicales y mango, dulce y exótico.",
        "vector": {
            "intensity": 0.7,
            "citrus": 0.4,
            "floral": 0.3,
            "woody": 0.3,
            "sweet": 0.9,
            "spicy": 0.4,
            "green": 0.2,
            "aquatic": 0.2,
            "suitable_occasions": ["daily", "special_events"],
            "suitable_times": ["afternoon", "night"],
            "season": "summer",
            "longevity": 0.7,
            "concentration": "eau_de_parfum"
        }
    },
    {
        "name": "Club de Nuit Intense Man",
        "brand": "Armaf",
        "description": "Cítrico amaderado masculino muy conocido, alternativa popular con gran rendimiento.",
        "vector": {
            "intensity": 0.9,
            "citrus": 0.7,
            "floral": 0.2,
            "woody": 0.8,
            "sweet": 0.4,
            "spicy": 0.6,
            "green": 0.3,
            "aquatic": 0.3,
            "suitable_occasions": ["work", "special_events", "any"],
            "suitable_times": ["morning", "afternoon", "night"],
            "season": "all_year",
            "longevity": 0.9,
            "concentration": "eau_de_parfum"
        }
    },
    {
        "name": "9PM",
        "brand": "Afnan",
        "description": "Oriental ambar masculino dulce, perfecto para la noche.",
        "vector": {
            "intensity": 0.8,
            "citrus": 0.2,
            "floral": 0.3,
            "woody": 0.7,
            "sweet": 0.8,
            "spicy": 0.7,
            "green": 0.1,
            "aquatic": 0.1,
            "suitable_occasions": ["night", "romantic", "special_events"],
            "suitable_times": ["night"],
            "season": "winter",
            "longevity": 0.8,
            "concentration": "eau_de_parfum"
        }
    },
    {
        "name": "Khamrah",
        "brand": "Lattafa",
        "description": "Yogurt especiado dulce con gran popularidad. Notas gourmand únicas.",
        "vector": {
            "intensity": 0.9,
            "citrus": 0.2,
            "floral": 0.2,
            "woody": 0.6,
            "sweet": 0.95,
            "spicy": 0.8,
            "green": 0.1,
            "aquatic": 0.0,
            "suitable_occasions": ["special_events", "romantic", "night"],
            "suitable_times": ["night"],
            "season": "autumn",
            "longevity": 0.95,
            "concentration": "parfum"
        }
    },
    {
        "name": "Yum Yum",
        "brand": "Armaf",
        "description": "Fragancia dulce y golosa del catálogo árabe con notas gourmand.",
        "vector": {
            "intensity": 0.7,
            "citrus": 0.3,
            "floral": 0.4,
            "woody": 0.3,
            "sweet": 0.9,
            "spicy": 0.3,
            "green": 0.1,
            "aquatic": 0.1,
            "suitable_occasions": ["daily", "romantic"],
            "suitable_times": ["afternoon", "night"],
            "season": "all_year",
            "longevity": 0.7,
            "concentration": "eau_de_parfum"
        }
    },
    {
        "name": "Asad",
        "brand": "Lattafa",
        "description": "Ambar especiado fuerte para hombre, presencia imponente.",
        "vector": {
            "intensity": 0.95,
            "citrus": 0.2,
            "floral": 0.1,
            "woody": 0.8,
            "sweet": 0.6,
            "spicy": 0.9,
            "green": 0.1,
            "aquatic": 0.0,
            "suitable_occasions": ["special_events", "night"],
            "suitable_times": ["night"],
            "season": "winter",
            "longevity": 0.9,
            "concentration": "parfum"
        }
    },
    {
        "name": "Yara Candy",
        "brand": "Lattafa",
        "description": "Dulce y powdery femenino con notas de caramelo y flores suaves.",
        "vector": {
            "intensity": 0.6,
            "citrus": 0.2,
            "floral": 0.6,
            "woody": 0.2,
            "sweet": 0.95,
            "spicy": 0.2,
            "green": 0.1,
            "aquatic": 0.1,
            "suitable_occasions": ["daily", "romantic"],
            "suitable_times": ["afternoon", "night"],
            "season": "spring",
            "longevity": 0.7,
            "concentration": "eau_de_parfum"
        }
    },
    {
        "name": "Yara",
        "brand": "Lattafa",
        "description": "Muy vendido en mercados globales, floral dulce femenino elegante.",
        "vector": {
            "intensity": 0.7,
            "citrus": 0.3,
            "floral": 0.8,
            "woody": 0.3,
            "sweet": 0.7,
            "spicy": 0.3,
            "green": 0.2,
            "aquatic": 0.2,
            "suitable_occasions": ["work", "daily", "special_events"],
            "suitable_times": ["morning", "afternoon", "night"],
            "season": "all_year",
            "longevity": 0.8,
            "concentration": "eau_de_parfum"
        }
    },
    {
        "name": "Bade'e Al Oud For Glory",
        "brand": "Lattafa",
        "description": "Oud con dulzor oriental, intenso y duradero.",
        "vector": {
            "intensity": 0.9,
            "citrus": 0.1,
            "floral": 0.3,
            "woody": 0.95,
            "sweet": 0.7,
            "spicy": 0.7,
            "green": 0.1,
            "aquatic": 0.0,
            "suitable_occasions": ["special_events", "night"],
            "suitable_times": ["night"],
            "season": "winter",
            "longevity": 0.95,
            "concentration": "parfum"
        }
    },
    {
        "name": "Ana Abyedh",
        "brand": "Lattafa",
        "description": "Floral blanco fresco y limpio, elegante y refinado.",
        "vector": {
            "intensity": 0.6,
            "citrus": 0.4,
            "floral": 0.9,
            "woody": 0.2,
            "sweet": 0.5,
            "spicy": 0.2,
            "green": 0.3,
            "aquatic": 0.3,
            "suitable_occasions": ["work", "daily"],
            "suitable_times": ["morning", "afternoon"],
            "season": "summer",
            "longevity": 0.6,
            "concentration": "eau_de_parfum"
        }
    },
    {
        "name": "Ansaam Gold",
        "brand": "Lattafa",
        "description": "Oriental floral en edición oro, lujoso y sofisticado.",
        "vector": {
            "intensity": 0.75,
            "citrus": 0.3,
            "floral": 0.7,
            "woody": 0.5,
            "sweet": 0.6,
            "spicy": 0.6,
            "green": 0.2,
            "aquatic": 0.1,
            "suitable_occasions": ["special_events", "romantic"],
            "suitable_times": ["afternoon", "night"],
            "season": "autumn",
            "longevity": 0.8,
            "concentration": "eau_de_parfum"
        }
    },
    {
        "name": "Club de Nuit Sillage",
        "brand": "Armaf",
        "description": "Amaderado almizclado unisex con gran estela.",
        "vector": {
            "intensity": 0.85,
            "citrus": 0.3,
            "floral": 0.4,
            "woody": 0.85,
            "sweet": 0.5,
            "spicy": 0.6,
            "green": 0.3,
            "aquatic": 0.2,
            "suitable_occasions": ["work", "special_events", "any"],
            "suitable_times": ["morning", "afternoon", "night"],
            "season": "all_year",
            "longevity": 0.9,
            "concentration": "eau_de_parfum"
        }
    },
    {
        "name": "Odyssey Mandarin Sky",
        "brand": "Armaf",
        "description": "Cítrico dulzón fresco y vibrante con mandarina prominente.",
        "vector": {
            "intensity": 0.6,
            "citrus": 0.9,
            "floral": 0.3,
            "woody": 0.3,
            "sweet": 0.6,
            "spicy": 0.2,
            "green": 0.4,
            "aquatic": 0.3,
            "suitable_occasions": ["daily", "work", "sports"],
            "suitable_times": ["morning", "afternoon"],
            "season": "summer",
            "longevity": 0.6,
            "concentration": "eau_de_toilette"
        }
    },
    {
        "name": "Ombre Oud Intense",
        "brand": "Armaf",
        "description": "Oud intenso masculino con gran profundidad y complejidad.",
        "vector": {
            "intensity": 0.95,
            "citrus": 0.2,
            "floral": 0.2,
            "woody": 0.95,
            "sweet": 0.4,
            "spicy": 0.8,
            "green": 0.1,
            "aquatic": 0.0,
            "suitable_occasions": ["special_events", "night"],
            "suitable_times": ["night"],
            "season": "winter",
            "longevity": 0.95,
            "concentration": "parfum"
        }
    },
    {
        "name": "Oros Oumo",
        "brand": "Armaf",
        "description": "Amaderado oriental con toques especiados elegantes.",
        "vector": {
            "intensity": 0.75,
            "citrus": 0.3,
            "floral": 0.3,
            "woody": 0.8,
            "sweet": 0.5,
            "spicy": 0.7,
            "green": 0.2,
            "aquatic": 0.1,
            "suitable_occasions": ["work", "special_events"],
            "suitable_times": ["afternoon", "night"],
            "season": "autumn",
            "longevity": 0.8,
            "concentration": "eau_de_parfum"
        }
    },
    {
        "name": "Club de Nuit Iconic",
        "brand": "Armaf",
        "description": "Variante popular de la línea CDN con gran rendimiento.",
        "vector": {
            "intensity": 0.85,
            "citrus": 0.6,
            "floral": 0.3,
            "woody": 0.7,
            "sweet": 0.4,
            "spicy": 0.6,
            "green": 0.3,
            "aquatic": 0.3,
            "suitable_occasions": ["work", "special_events", "any"],
            "suitable_times": ["morning", "afternoon", "night"],
            "season": "all_year",
            "longevity": 0.85,
            "concentration": "eau_de_parfum"
        }
    },
    {
        "name": "Le Femme",
        "brand": "Armaf",
        "description": "Perfil femenino floral dulce elegante y versátil.",
        "vector": {
            "intensity": 0.65,
            "citrus": 0.4,
            "floral": 0.8,
            "woody": 0.3,
            "sweet": 0.7,
            "spicy": 0.3,
            "green": 0.2,
            "aquatic": 0.2,
            "suitable_occasions": ["work", "daily", "romantic"],
            "suitable_times": ["morning", "afternoon", "night"],
            "season": "spring",
            "longevity": 0.7,
            "concentration": "eau_de_parfum"
        }
    },
    {
        "name": "Amber Oud Gold Edition",
        "brand": "Al Haramain",
        "description": "Ambarado oriental unisex con notas de oud lujosas.",
        "vector": {
            "intensity": 0.85,
            "citrus": 0.2,
            "floral": 0.3,
            "woody": 0.9,
            "sweet": 0.7,
            "spicy": 0.7,
            "green": 0.1,
            "aquatic": 0.0,
            "suitable_occasions": ["special_events", "night"],
            "suitable_times": ["night"],
            "season": "winter",
            "longevity": 0.9,
            "concentration": "parfum"
        }
    },
    {
        "name": "Amber Oud Black Edition",
        "brand": "Al Haramain",
        "description": "Oud intenso con profundidad oscura y misteriosa.",
        "vector": {
            "intensity": 0.95,
            "citrus": 0.1,
            "floral": 0.2,
            "woody": 0.95,
            "sweet": 0.5,
            "spicy": 0.8,
            "green": 0.1,
            "aquatic": 0.0,
            "suitable_occasions": ["special_events", "night"],
            "suitable_times": ["night"],
            "season": "winter",
            "longevity": 0.95,
            "concentration": "parfum"
        }
    },
    {
        "name": "French Collection Rouge",
        "brand": "Al Haramain",
        "description": "Floral frutal fresco y romántico de inspiración francesa.",
        "vector": {
            "intensity": 0.65,
            "citrus": 0.5,
            "floral": 0.8,
            "woody": 0.3,
            "sweet": 0.7,
            "spicy": 0.3,
            "green": 0.3,
            "aquatic": 0.2,
            "suitable_occasions": ["daily", "romantic", "work"],
            "suitable_times": ["morning", "afternoon"],
            "season": "spring",
            "longevity": 0.7,
            "concentration": "eau_de_parfum"
        }
    },
    {
        "name": "Royal Musk",
        "brand": "Al Haramain",
        "description": "Almizclado clásico suave y envolvente.",
        "vector": {
            "intensity": 0.6,
            "citrus": 0.2,
            "floral": 0.5,
            "woody": 0.5,
            "sweet": 0.6,
            "spicy": 0.4,
            "green": 0.2,
            "aquatic": 0.2,
            "suitable_occasions": ["daily", "work", "any"],
            "suitable_times": ["morning", "afternoon", "night"],
            "season": "all_year",
            "longevity": 0.7,
            "concentration": "eau_de_parfum"
        }
    },
    {
        "name": "L'Aventure",
        "brand": "Al Haramain",
        "description": "Cítrico amaderado inspirado en clásicos occidentales, versátil.",
        "vector": {
            "intensity": 0.8,
            "citrus": 0.8,
            "floral": 0.3,
            "woody": 0.7,
            "sweet": 0.4,
            "spicy": 0.6,
            "green": 0.4,
            "aquatic": 0.3,
            "suitable_occasions": ["work", "daily", "special_events"],
            "suitable_times": ["morning", "afternoon", "night"],
            "season": "all_year",
            "longevity": 0.8,
            "concentration": "eau_de_parfum"
        }
    },
    {
        "name": "Ultra Violet",
        "brand": "Al Haramain",
        "description": "Floral con oud suave, equilibrado y moderno.",
        "vector": {
            "intensity": 0.7,
            "citrus": 0.3,
            "floral": 0.7,
            "woody": 0.6,
            "sweet": 0.6,
            "spicy": 0.5,
            "green": 0.2,
            "aquatic": 0.2,
            "suitable_occasions": ["work", "daily", "romantic"],
            "suitable_times": ["afternoon", "night"],
            "season": "spring",
            "longevity": 0.75,
            "concentration": "eau_de_parfum"
        }
    },
    {
        "name": "Supremacy Gold",
        "brand": "Afnan",
        "description": "Oriental con presencia de especias doradas y lujosas.",
        "vector": {
            "intensity": 0.85,
            "citrus": 0.3,
            "floral": 0.4,
            "woody": 0.7,
            "sweet": 0.6,
            "spicy": 0.85,
            "green": 0.2,
            "aquatic": 0.1,
            "suitable_occasions": ["special_events", "night"],
            "suitable_times": ["night"],
            "season": "autumn",
            "longevity": 0.85,
            "concentration": "eau_de_parfum"
        }
    },
    {
        "name": "Musaman White",
        "brand": "Lattafa",
        "description": "Oud especiado ligero con notas blancas refrescantes.",
        "vector": {
            "intensity": 0.65,
            "citrus": 0.4,
            "floral": 0.5,
            "woody": 0.7,
            "sweet": 0.5,
            "spicy": 0.6,
            "green": 0.3,
            "aquatic": 0.2,
            "suitable_occasions": ["daily", "work"],
            "suitable_times": ["morning", "afternoon"],
            "season": "summer",
            "longevity": 0.7,
            "concentration": "eau_de_parfum"
        }
    },
    {
        "name": "Fakhar Black",
        "brand": "Lattafa",
        "description": "Amaderado especiado con carácter masculino fuerte.",
        "vector": {
            "intensity": 0.85,
            "citrus": 0.3,
            "floral": 0.2,
            "woody": 0.9,
            "sweet": 0.5,
            "spicy": 0.8,
            "green": 0.2,
            "aquatic": 0.1,
            "suitable_occasions": ["special_events", "night"],
            "suitable_times": ["night"],
            "season": "winter",
            "longevity": 0.85,
            "concentration": "eau_de_parfum"
        }
    },
    {
        "name": "Ajwad",
        "brand": "Lattafa",
        "description": "Inspiración oriental frutal fresco y moderno.",
        "vector": {
            "intensity": 0.7,
            "citrus": 0.6,
            "floral": 0.4,
            "woody": 0.5,
            "sweet": 0.7,
            "spicy": 0.5,
            "green": 0.3,
            "aquatic": 0.3,
            "suitable_occasions": ["daily", "work", "romantic"],
            "suitable_times": ["morning", "afternoon"],
            "season": "spring",
            "longevity": 0.7,
            "concentration": "eau_de_parfum"
        }
    },
    {
        "name": "Blueberry Musk",
        "brand": "Arabiyat Prestige",
        "description": "Dulce musk con arándanos, gourmand único y atractivo.",
        "vector": {
            "intensity": 0.7,
            "citrus": 0.3,
            "floral": 0.5,
            "woody": 0.3,
            "sweet": 0.95,
            "spicy": 0.3,
            "green": 0.2,
            "aquatic": 0.1,
            "suitable_occasions": ["daily", "romantic"],
            "suitable_times": ["afternoon", "night"],
            "season": "summer",
            "longevity": 0.7,
            "concentration": "eau_de_parfum"
        }
    },
    {
        "name": "Buthaina",
        "brand": "Asdaaf",
        "description": "Floral oriental elegante y femenino con gran sofisticación.",
        "vector": {
            "intensity": 0.75,
            "citrus": 0.3,
            "floral": 0.85,
            "woody": 0.4,
            "sweet": 0.7,
            "spicy": 0.6,
            "green": 0.2,
            "aquatic": 0.2,
            "suitable_occasions": ["special_events", "romantic", "work"],
            "suitable_times": ["afternoon", "night"],
            "season": "spring",
            "longevity": 0.75,
            "concentration": "eau_de_parfum"
        }
    },
]


def populate_database():
    """Pobla la base de datos con perfumes árabes"""
    db = SessionLocal()
    
    try:
        print("🚀 Iniciando población de base de datos...")
        print(f"📦 Insertando {len(PERFUMES_DATA)} perfumes...")
        
        inserted_count = 0
        
        for perfume_data in PERFUMES_DATA:
            # Verificar si el perfume ya existe
            existing = db.query(Perfume).filter(
                Perfume.name == perfume_data["name"],
                Perfume.brand == perfume_data["brand"]
            ).first()
            
            if existing:
                print(f"⏭️  '{perfume_data['name']}' ya existe, saltando...")
                continue
            
            # Crear perfume
            perfume = Perfume(
                name=perfume_data["name"],
                brand=perfume_data["brand"],
                description=perfume_data["description"],
                is_active=True
            )
            
            db.add(perfume)
            db.flush()  # Para obtener el ID
            
            # Crear vector del perfume
            vector_data = perfume_data["vector"]
            perfume_vector = PerfumeVector(
                perfume_id=perfume.id,
                intensity=vector_data["intensity"],
                citrus=vector_data["citrus"],
                floral=vector_data["floral"],
                woody=vector_data["woody"],
                sweet=vector_data["sweet"],
                spicy=vector_data["spicy"],
                green=vector_data["green"],
                aquatic=vector_data["aquatic"],
                suitable_occasions=vector_data["suitable_occasions"],
                suitable_times=vector_data["suitable_times"],
                season=vector_data["season"],
                longevity=vector_data["longevity"],
                concentration=vector_data["concentration"]
            )
            
            db.add(perfume_vector)
            inserted_count += 1
            print(f"✅ '{perfume_data['name']}' - {perfume_data['brand']}")
        
        db.commit()
        print(f"\n🎉 ¡Completado! {inserted_count} perfumes insertados exitosamente.")
        print(f"📊 Total de perfumes en base de datos: {db.query(Perfume).count()}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("   NEUROSCENT - POBLACIÓN DE PERFUMES ÁRABES")
    print("=" * 60)
    populate_database()
