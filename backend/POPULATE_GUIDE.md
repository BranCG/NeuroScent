# Guía de Ejecución - Población de Perfumes

## Pasos para ejecutar el script

### 1. Asegurarse que la base de datos esté creada

```sql
-- Conectar a PostgreSQL y ejecutar:
CREATE DATABASE neuroscent_db;
CREATE USER neuroscent_user WITH PASSWORD 'neuroscent_pass';
GRANT ALL PRIVILEGES ON DATABASE neuroscent_db TO neuroscent_user;
```

### 2. Verificar que el backend esté configurado

```bash
cd backend
# Asegurarse de tener el .env configurado
cat .env
```

### 3. Ejecutar el script de población

```bash
# Desde el directorio backend/
python populate_perfumes.py
```

## Salida esperada

```
============================================================
   NEUROSCENT - POBLACIÓN DE PERFUMES ÁRABES
============================================================
🚀 Iniciando población de base de datos...
📦 Insertando 30 perfumes...
✅ 'Bharara King' - Bharara
✅ 'Vulcan Feu' - ORIENTFRAGANCE
✅ 'Club de Nuit Intense Man' - Armaf
...
🎉 ¡Completado! 30 perfumes insertados exitosamente.
📊 Total de perfumes en base de datos: 30
```

## Perfumes incluidos

- **Bharara**: King
- **Lattafa**: Khamrah, Yara, Yara Candy, Bade'e Al Oud For Glory, Ana Abyedh, Ansaam Gold, Asad, Musaman White, Fakhar Black, Ajwad
- **Armaf**: Club de Nuit Intense Man, Yum Yum, Club de Nuit Sillage, Club de Nuit Iconic, Odyssey Mandarin Sky, Ombre Oud Intense, Oros Oumo, Le Femme
- **Afnan**: 9PM, Supremacy Gold
- **Al Haramain**: Amber Oud Gold Edition, Amber Oud Black Edition, French Collection Rouge, Royal Musk, L'Aventure, Ultra Violet
- **Arabiyat Prestige**: Blueberry Musk
- **Asdaaf**: Buthaina
- **ORIENTFRAGANCE**: Vulcan Feu

## Vectores Olfativos Asignados

Cada perfume tiene:
- **Intensidad**: 0.6 - 0.95 (mayoría son intensos, típico de perfumes árabes)
- **Familias**: citrus, floral, woody, sweet, spicy, green, aquatic (0.0 - 1.0)
- **Ocasiones**: work, daily, special_events, romantic, night, sports, any
- **Momentos**: morning, afternoon, night
- **Estación**: spring, summer, autumn, winter, all_year
- **Longevidad**: 0.6 - 0.95 (mayoría 0.7+, muy duraderos)
- **Concentración**: eau_de_toilette, eau_de_parfum, parfum

## Notas sobre las clasificaciones

### Perfumes Más Dulces (sweet > 0.9)
- Khamrah (0.95)
- Yara Candy (0.95)
- Blueberry Musk (0.95)
- Yum Yum (0.9)

### Perfumes Más Amaderados (woody > 0.9)
- Bade'e Al Oud For Glory (0.95)
- Amber Oud Black Edition (0.95)
- Ombre Oud Intense (0.95)
- Fakhar Black (0.9)

### Perfumes Más Versátiles (all_year)
- Club de Nuit Intense Man
- Club de Nuit Iconic
- Club de Nuit Sillage
- Yara
- Royal Musk
- L'Aventure

### Perfumes Para Verano
- Vulcan Feu
- Ana Abyedh
- Odyssey Mandarin Sky
- Musaman White
- Blueberry Musk

## Solución de Problemas

### Error: "could not connect to server"
```bash
# Verificar que PostgreSQL esté corriendo
# Windows:
Get-Service postgresql*

# Si no está corriendo, iniciar el servicio
```

### Error: "relation does not exist"
```bash
# Las tablas se crean automáticamente al ejecutar el script
# Si hay problemas, verificar que main.py tenga:
# Base.metadata.create_all(bind=engine)
```

### Error: "UNIQUE constraint failed"
```bash
# El perfume ya existe en la base de datos
# El script salta automáticamente duplicados
```
