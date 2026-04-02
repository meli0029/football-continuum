from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base


class League(Base):
    __tablename__ = "league"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    status: Mapped[str] = mapped_column(String(20), default="creating", index=True)


class LeagueCompetition(Base):
    __tablename__ = "league_competition"
    __table_args__ = (UniqueConstraint("league_id", "master_competition_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    league_id: Mapped[int] = mapped_column(ForeignKey("league.id"), index=True)
    master_competition_id: Mapped[int] = mapped_column(ForeignKey("master_competition.id"), index=True)


class LeagueTeam(Base):
    __tablename__ = "league_team"
    __table_args__ = (UniqueConstraint("league_id", "master_team_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    league_id: Mapped[int] = mapped_column(ForeignKey("league.id"), index=True)
    master_team_id: Mapped[int] = mapped_column(ForeignKey("master_team.id"), index=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("user.id"), nullable=True, index=True)


class LeagueStadium(Base):
    __tablename__ = "league_stadium"
    __table_args__ = (UniqueConstraint("league_id", "master_stadium_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    league_id: Mapped[int] = mapped_column(ForeignKey("league.id"), index=True)
    master_stadium_id: Mapped[int] = mapped_column(ForeignKey("master_stadium.id"), index=True)
    name: Mapped[str] = mapped_column(String(100))


class LeaguePlayer(Base):
    __tablename__ = "league_player"
    __table_args__ = (UniqueConstraint("league_id", "master_player_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    league_id: Mapped[int] = mapped_column(ForeignKey("league.id"), index=True)
    master_player_id: Mapped[int] = mapped_column(ForeignKey("master_player.id"), index=True)
    team_master_id: Mapped[int] = mapped_column(ForeignKey("master_team.id"), index=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    position: Mapped[str] = mapped_column(String(20), index=True)
    overall: Mapped[int] = mapped_column(Integer, index=True)
    