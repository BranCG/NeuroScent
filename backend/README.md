# NeuroScent Backend API

Backend API for NeuroScent perfume affinity platform.

## Tech Stack

- **Python 3.11+**
- **FastAPI** - Modern web framework
- **PostgreSQL** - Database
- **SQLAlchemy** - ORM
- **Pydantic** - Data validation
- **NumPy** - Vector calculations

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and update:

```bash
cp .env.example .env
```

Edit `.env` with your database credentials.

### 3. Setup Database

Create PostgreSQL database:

```sql
CREATE DATABASE neuroscent_db;
CREATE USER neuroscent_user WITH PASSWORD 'neuroscent_pass';
GRANT ALL PRIVILEGES ON DATABASE neuroscent_db TO neuroscent_user;
```

### 4. Run Migrations

```bash
# The app will auto-create tables on first run
# Or use Alembic for migrations:
alembic upgrade head
```

### 5. Run Development Server

```bash
python -m app.main
```

Or with uvicorn:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, visit:

- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc

## API Endpoints

### Health Check
```
GET /api/v1/health
```

### Calculate Affinity
```
POST /api/v1/test/calculate
```

### Get Test Result
```
GET /api/v1/test/{test_id}
```

### List Perfumes
```
GET /api/v1/perfumes
```

### Get Perfume
```
GET /api/v1/perfumes/{perfume_id}
```

## Project Structure

```
backend/
├── app/
│   ├── models/         # Database models
│   ├── schemas/        # Pydantic schemas
│   ├── routers/        # API endpoints
│   ├── services/       # Business logic
│   ├── database.py     # DB connection
│   ├── config.py       # Settings
│   └── main.py         # FastAPI app
├── requirements.txt
└── .env.example
```

## Testing

```bash
pytest tests/
```

## License

Proprietary - NeuroScent Platform
