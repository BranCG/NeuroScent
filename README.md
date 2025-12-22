# NeuroScent Platform

Plataforma web para reducir la incertidumbre al comprar perfumes online mediante IA y análisis sensorial.

## 🎯 Descripción

NeuroScent es un sistema de recomendación de perfumes basado en inteligencia artificial que:
- Evalúa las preferencias sensoriales del usuario mediante un test de 2-3 minutos
- Calcula afinidad olfativa usando algoritmos de similitud vectorial
- Genera descripciones personalizadas en lenguaje natural
- Proporciona recomendaciones contextualizadas de uso

## 📁 Estructura del Proyecto

```
NeuroScent/
├── backend/              # FastAPI + PostgreSQL
│   ├── app/
│   │   ├── models/      # Modelos de base de datos
│   │   ├── schemas/     # Esquemas Pydantic
│   │   ├── routers/     # Endpoints API
│   │   ├── services/    # Lógica de negocio
│   │   ├── database.py
│   │   ├── config.py
│   │   └── main.py
│   ├── requirements.txt
│   └── README.md
│
└── frontend/            # React + TypeScript
    ├── src/
    │   ├── pages/      # Páginas principales
    │   ├── components/ # Componentes React
    │   ├── services/   # Servicios API
    │   ├── types/      # Tipos TypeScript
    │   └── App.tsx
    ├── package.json
    └── README.md
```

## 🚀 Quick Start

### Backend Setup

1. Navegar al directorio backend:
```bash
cd backend
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus credenciales de PostgreSQL
```

4. Crear base de datos PostgreSQL:
```sql
CREATE DATABASE neuroscent_db;
CREATE USER neuroscent_user WITH PASSWORD 'neuroscent_pass';
GRANT ALL PRIVILEGES ON DATABASE neuroscent_db TO neuroscent_user;
```

5. Ejecutar servidor:
```bash
python -m app.main
```

API disponible en: `http://localhost:8000`
Documentación: `http://localhost:8000/api/v1/docs`

### Frontend Setup

1. Navegar al directorio frontend:
```bash
cd frontend
```

2. Instalar dependencias:
```bash
npm install
```

3. Configurar variables de entorno:
```bash
# Crear archivo .env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

4. Ejecutar servidor de desarrollo:
```bash
npm run dev
```

App disponible en: `http://localhost:5173`

## 🧪 Funcionalidades Principales

### 1. Test Sensorial (10 preguntas)
- Intensidad olfativa preferida
- Familias olfativas favoritas
- Aromas rechazados
- Asociación emocional
- Contexto de uso (momento, ocasión, estación)
- Persistencia deseada
- Tipo de concentración
- Referencia de perfume (opcional)

### 2. Motor de Afinidad
- Cálculo de similitud vectorial (coseno)
- Ponderación de contexto de uso (30%)
- Matching de intensidad y persistencia (20%)
- Validación de rechazos
- Score de afinidad 0-100%

### 3. Generación de Descripciones
- Descripciones sensoriales personalizadas en español
- Recomendaciones de uso contextual
- Nivel de afinidad (excellent/good/moderate/low)

## 📚 Documentación Completa

Ver `neuroscent_architecture.md` en el directorio artifacts para:
- Arquitectura completa del sistema
- Diagramas de flujo
- Modelo de datos detallado
- Pseudocódigo del motor de afinidad
- Roadmap de escalabilidad

## 🛠️ Stack Tecnológico

**Backend:**
- Python 3.11+
- FastAPI
- PostgreSQL 15+
- SQLAlchemy
- NumPy (cálculos vectoriales)

**Frontend:**
- React 18
- TypeScript
- Vite
- React Router
- Framer Motion
- Axios

## 📝 API Endpoints

### Health
- `GET /api/v1/health` - Health check

### Test
- `POST /api/v1/test/calculate` - Enviar respuestas y calcular afinidad
- `GET /api/v1/test/{test_id}` - Obtener resultados del test

### Perfumes
- `GET /api/v1/perfumes` - Listar perfumes
- `GET /api/v1/perfumes/{perfume_id}` - Obtener perfume por ID
- `POST /api/v1/perfumes` - Crear perfume (Admin)

## 🎨 Diseño UX

- **Landing Page**: Introducción con CTA claro
- **Test Flow**: Progreso visual, validación en tiempo real
- **Results Page**: Visualización de afinidad con animaciones

## 📄 Licencia

Proprietary - NeuroScent Platform

## 👥 Autor

Desarrollado para NeuroScent - Sistema de recomendación de perfumes con IA
