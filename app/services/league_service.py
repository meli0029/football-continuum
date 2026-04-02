from sqlalchemy.orm import Session
from app.models.master import MasterCompetition, MasterTeam, MasterStadium, MasterPlayer
from app.models.league import (
    League,
    LeagueCompetition,
    LeagueTeam,
    LeagueStadium,
    LeaguePlayer,
)


def create_league_universe(db: Session, name: str, competition_ids: list[int]) -> League:
    league = League(name=name, status="creating")
    db.add(league)
    db.flush()

    competitions = (
        db.query(MasterCompetition)
        .filter(MasterCompetition.id.in_(competition_ids))
        .all()
    )

    for comp in competitions:
        db.add(LeagueCompetition(league_id=league.id, master_competition_id=comp.id))

    teams = (
        db.query(MasterTeam)
        .filter(MasterTeam.competition_id.in_(competition_ids))
        .all()
    )

    team_ids = [t.id for t in teams]

    stadiums = db.query(MasterStadium).filter(MasterStadium.master_team_id.in_(team_ids)).all()
    players = db.query(MasterPlayer).filter(MasterPlayer.master_team_id.in_(team_ids)).all()

    for team in teams:
        db.add(
            LeagueTeam(
                league_id=league.id,
                master_team_id=team.id,
                name=team.name,
            )
        )

    for stadium in stadiums:
        db.add(
            LeagueStadium(
                league_id=league.id,
                master_stadium_id=stadium.id,
                name=stadium.name,
            )
        )

    for player in players:
        db.add(
            LeaguePlayer(
                league_id=league.id,
                master_player_id=player.id,
                team_master_id=player.master_team_id,
                name=player.name,
                position=player.position,
                overall=player.overall,
            )
        )

    league.status = "ready"
    db.commit()
    db.refresh(league)
    return league