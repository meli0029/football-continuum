from sqlalchemy.orm import Session
from app.models.master import MasterCompetition, MasterTeam, MasterStadium, MasterPlayer


def seed_demo_data(db: Session) -> None:
    if db.query(MasterCompetition).count() > 0:
        return

    premier = MasterCompetition(name="Premier League")
    championship = MasterCompetition(name="Championship")
    db.add_all([premier, championship])
    db.flush()

    teams = [
        MasterTeam(name="Northbridge FC", competition_id=premier.id),
        MasterTeam(name="Rivergate United", competition_id=premier.id),
        MasterTeam(name="Kingsport City", competition_id=premier.id),
        MasterTeam(name="Easthaven Rovers", competition_id=premier.id),
        MasterTeam(name="Harbor Athletic", competition_id=championship.id),
        MasterTeam(name="Stoneford Town", competition_id=championship.id),
        MasterTeam(name="Westmere Albion", competition_id=championship.id),
        MasterTeam(name="Red Valley FC", competition_id=championship.id),
    ]
    db.add_all(teams)
    db.flush()

    for team in teams:
        db.add(MasterStadium(master_team_id=team.id, name=f"{team.name} Stadium"))
        for i in range(20):
            position = ["GK", "DEF", "MID", "FWD"][i % 4]
            db.add(
                MasterPlayer(
                    master_team_id=team.id,
                    name=f"{team.name} Player {i+1}",
                    position=position,
                    overall=60 + (i % 20),
                )
            )

    db.commit()