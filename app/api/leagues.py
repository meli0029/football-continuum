from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.league import CreateLeagueRequest
from app.models.league import League
from app.services.league_service import create_league_universe

router = APIRouter(prefix="/leagues", tags=["leagues"])


@router.post("")
def create_league(payload: CreateLeagueRequest, db: Session = Depends(get_db)):
    existing = db.query(League).filter(League.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="League name already exists")

    league = create_league_universe(db, payload.name, payload.competition_ids)
    return {"id": league.id, "name": league.name, "status": league.status}


@router.get("/{league_id}")
def get_league(league_id: int, db: Session = Depends(get_db)):
    league = db.query(League).filter(League.id == league_id).first()
    if not league:
        raise HTTPException(status_code=404, detail="League not found")
    return {"id": league.id, "name": league.name, "status": league.status}