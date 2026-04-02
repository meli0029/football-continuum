from fastapi import FastAPI
from app.db import Base, engine
from app.api.health import router as health_router
from app.api.seed import router as seed_router
from app.api.leagues import router as leagues_router
from app.api.users import router as users_router
import app.models.master
import app.models.league
import app.models.user


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Soccer Universe API")
app.include_router(health_router)
app.include_router(seed_router)
app.include_router(leagues_router)
app.include_router(users_router)
