from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.seed import seed_demo_data
from app.models.master import MasterTeam


router = APIRouter(prefix="/seed", tags=["seed"])


@router.post("/demo-data")
def seed_data(db: Session = Depends(get_db)):
    seed_demo_data(db)
    return {"status": "seeded"}


@router.get("/debug/teams")
def debug_teams(db: Session = Depends(get_db)):
    teams = db.query(MasterTeam).all()
    return [{"id": t.id, "name": t.name, "competition_id": t.competition_id} for t in teams]