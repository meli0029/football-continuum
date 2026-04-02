from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.seed import seed_demo_data

router = APIRouter(prefix="/seed", tags=["seed"])


@router.post("/demo-data")
def seed_data(db: Session = Depends(get_db)):
    seed_demo_data(db)
    return {"status": "seeded"}