# FastAPI CRUD Prueba Técnica

## Local Setup
1. pip install -r requirements.txt
2. alembic upgrade head
3. uvicorn app.main:app --reload

## Endpoints
- POST /auth/register
- POST /auth/login
- CRUD /users, /posts, /tags (auth required)

## Docker
1. docker-compose up -d db  # Spin DB
2. docker-compose run app alembic upgrade head  # Migraciones
3. docker-compose up app  # App