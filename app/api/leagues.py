from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.league import CreateLeagueRequest
from app.models.league import League
from app.services.league_service import create_league_universe
from app.models.league import LeagueTeam
from app.models.user import User
from app.models.league import LeagueTeam


router = APIRouter(prefix="/leagues", tags=["leagues"])


@router.post("")
def create_league(payload: CreateLeagueRequest, db: Session = Depends(get_db)):

    # 👇 ADD THIS RIGHT HERE (first line inside function)
    if not payload.competition_ids:
        raise HTTPException(status_code=400, detail="competition_ids required")

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


@router.post("/{league_id}/teams/{team_id}/claim")
def claim_team(league_id: int, team_id: int, user_id: int, db: Session = Depends(get_db)):
    team = (
        db.query(LeagueTeam)
        .filter(
            LeagueTeam.id == team_id,
            LeagueTeam.league_id == league_id,
        )
        .first()
    )

    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    if team.user_id is not None:
        raise HTTPException(status_code=400, detail="Team already claimed")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    team.user_id = user_id
    db.commit()

    return {
        "team_id": team.id,
        "team_name": team.name,
        "user_id": user_id,
    }


@router.get("/{league_id}/teams")
def get_league_teams(league_id: int, db: Session = Depends(get_db)):
    teams = (
        db.query(LeagueTeam)
        .filter(LeagueTeam.league_id == league_id)
        .all()
    )

    return [
        {
            "id": team.id,
            "name": team.name,
            "master_team_id": team.master_team_id,
        }
        for team in teams
    ]

@router.get("/{league_id}/summary")
def league_summary(league_id: int, db: Session = Depends(get_db)):
    # total teams
    total_teams = (
        db.query(LeagueTeam)
        .filter(LeagueTeam.league_id == league_id)
        .count()
    )

    # claimed teams
    claimed_teams = (
        db.query(LeagueTeam)
        .filter(
            LeagueTeam.league_id == league_id,
            LeagueTeam.user_id.isnot(None),
        )
        .count()
    )

    # total players
    total_players = (
        db.query(LeaguePlayer)
        .filter(LeaguePlayer.league_id == league_id)
        .count()
    )

    return {
        "league_id": league_id,
        "total_teams": total_teams,
        "claimed_teams": claimed_teams,
        "total_players": total_players,
    }