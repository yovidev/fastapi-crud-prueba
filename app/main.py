from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from .core.database import engine
from .models.base import BaseModel
from .routers.auth import router as auth_router
from .routers.users import router as users_router
from .routers.posts import router as posts_router
from .routers.tags import router as tags_router

app = FastAPI(title="crud_fastapi - prueba tecnica", version="1.0.0")

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(posts_router, prefix="/posts", tags=["posts"])
app.include_router(tags_router, prefix="/tags", tags=["tags"])

@app.on_event("startup")
async def startup():
        async with engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.create_all)

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        import time
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

app.add_middleware(TimingMiddleware)

@app.get("/")
async def root():
    return {"message": "API funcionando correctamente"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}