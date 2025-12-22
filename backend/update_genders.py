"""
Script para actualizar el género de los perfumes existentes.
"""

from sqlalchemy import text
from app.database import SessionLocal, engine

# Clasificación de géneros por perfume
GENDER_CLASSIFICATION = {
    # Masculinos
    "Bharara King": "male",
    "Vulcan Feu": "male",
    "Club de Nuit Intense Man": "male",
    "9PM": "male",
    "Khamrah": "male",
    "Asad": "male",
    "Club de Nuit Sillage": "unisex",
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
    """Actualiza el género de los perfumes existentes usando SQL directo"""
    
    with engine.connect() as conn:
        print("🔄 Actualizando géneros de perfumes...")
        
        # Agregar columna si no existe
        try:
            conn.execute(text("ALTER TABLE perfumes ADD COLUMN gender VARCHAR(20) DEFAULT 'unisex'"))
            conn.commit()
            print("✅ Columna 'gender' agregada")
        except Exception as e:
            print(f"ℹ️  Columna ya existe: {str(e)[:50]}")
        
        updated_count = 0
        
        for name, gender in GENDER_CLASSIFICATION.items():
            result = conn.execute(
                text("UPDATE perfumes SET gender = :gender WHERE name = :name"),
                {"gender": gender, "name": name}
            )
            
            if result.rowcount > 0:
                updated_count += 1
                print(f"✅ '{name}' → {gender}")
            else:
                print(f"⚠️  No encontrado: '{name}'")
        
        conn.commit()
        print(f"\n🎉 {updated_count} perfumes actualizados con género.")
        
        # Mostrar resumen
        male = conn.execute(text("SELECT COUNT(*) FROM perfumes WHERE gender = 'male'")).scalar()
        female = conn.execute(text("SELECT COUNT(*) FROM perfumes WHERE gender = 'female'")).scalar()
        unisex = conn.execute(text("SELECT COUNT(*) FROM perfumes WHERE gender = 'unisex'")).scalar()
        
        print(f"\n📊 Resumen:")
        print(f"   Masculinos: {male}")
        print(f"   Femeninos: {female}")
        print(f"   Unisex: {unisex}")


if __name__ == "__main__":
    print("=" * 50)
    print("   ACTUALIZACIÓN DE GÉNEROS")
    print("=" * 50)
    update_genders()
