"""
Script para actualizar el género de los perfumes existentes.
"""

from app.database import SessionLocal, engine, Base
from app.models.perfume import Perfume

# Clasificación de géneros por perfume
GENDER_CLASSIFICATION = {
    # Masculinos
    "Bharara King": "male",
    "Vulcan Feu": "male",
    "Club de Nuit Intense Man": "male",
    "9PM": "male",
    "Khamrah": "male",
    "Asad": "male",
    "Club de Nuit Sillage": "unisex",  # Unisex según descripción
    "Odyssey Mandarin Sky": "male",
    "Ombre Oud Intense": "male",
    "Oros Oumo": "male",
    "Club de Nuit Iconic": "male",
    "Amber Oud Gold Edition": "unisex",
    "Amber Oud Black Edition": "male",
    "Royal Musk": "unisex",
    "L'Aventure": "male",
    "Ultra Violet": "unisex",
    "Supremacy Gold": "male",
    "Musaman White": "male",
    "Fakhar Black": "male",
    "Ajwad": "male",
    "Bade'e Al Oud For Glory": "male",
    
    # Femeninos
    "Yara Candy": "female",
    "Yara": "female",
    "Ana Abyedh": "female",
    "Ansaam Gold": "female",
    "Le Femme": "female",
    "French Collection Rouge": "female",
    "Blueberry Musk": "female",
    "Buthaina": "female",
    "Yum Yum": "female",
}

def update_genders():
    """Actualiza el género de los perfumes existentes"""
    db = SessionLocal()
    
    try:
        print("🔄 Actualizando géneros de perfumes...")
        
        # Primero, agregar la columna si no existe (SQLite)
        try:
            db.execute("ALTER TABLE perfumes ADD COLUMN gender VARCHAR(20) DEFAULT 'unisex'")
            db.commit()
            print("✅ Columna 'gender' agregada")
        except Exception as e:
            print(f"ℹ️  Columna ya existe o error: {e}")
            db.rollback()
        
        updated_count = 0
        
        for name, gender in GENDER_CLASSIFICATION.items():
            perfume = db.query(Perfume).filter(Perfume.name == name).first()
            
            if perfume:
                perfume.gender = gender
                updated_count += 1
                print(f"✅ '{name}' → {gender}")
            else:
                print(f"⚠️  No encontrado: '{name}'")
        
        db.commit()
        print(f"\n🎉 {updated_count} perfumes actualizados con género.")
        
        # Mostrar resumen
        male_count = db.query(Perfume).filter(Perfume.gender == "male").count()
        female_count = db.query(Perfume).filter(Perfume.gender == "female").count()
        unisex_count = db.query(Perfume).filter(Perfume.gender == "unisex").count()
        
        print(f"\n📊 Resumen:")
        print(f"   Masculinos: {male_count}")
        print(f"   Femeninos: {female_count}")
        print(f"   Unisex: {unisex_count}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 50)
    print("   ACTUALIZACIÓN DE GÉNEROS")
    print("=" * 50)
    update_genders()
