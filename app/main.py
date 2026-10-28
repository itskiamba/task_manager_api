from fastapi import APIRouter, FastAPI
from sqlalchemy import text

from app.api.deps import DbSession
from app.api.routes import auth, tasks, users
from app.core.config import settings

app = FastAPI(title=settings.project_name, version="1.0.0")

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(tasks.router)

app.include_router(api_router)

@app.get("/health")
def health():
    return {"status":"ok"}

@app.get("/health/db")
def health_db(db: DbSession):
    db.execute(text("SELECT 1"))
    return {"database": "connected"}

