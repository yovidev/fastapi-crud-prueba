from fastapi import FastAPI
from .routers import auth, users, posts, tags
from .core.database import engine
from .models.entities import Base

app = FastAPI(title="crud_fastapi - prueba tecnica", version="1.0.0")


