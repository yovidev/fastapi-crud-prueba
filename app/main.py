from fastapi import FastAPI
from .router import auth, users, posts, tags
from .core.database import engine
from .models.entities import Base

app = FastAPI(title="crud_fastapi - prueba tecnica", version="1.0.0")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)