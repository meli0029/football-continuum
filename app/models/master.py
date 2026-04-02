from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base


class MasterCompetition(Base):
    __tablename__ = "master_competition"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)


class MasterTeam(Base):
    __tablename__ = "master_team"

    id: Mapped[int] = mapped_column(primary_key=True)
    competition_id: Mapped[int] = mapped_column(ForeignKey("master_competition.id"), index=True)
    name: Mapped[str] = mapped_column(String(100), index=True)


class MasterStadium(Base):
    __tablename__ = "master_stadium"

    id: Mapped[int] = mapped_column(primary_key=True)
    master_team_id: Mapped[int] = mapped_column(ForeignKey("master_team.id"), unique=True)
    name: Mapped[str] = mapped_column(String(100))


class MasterPlayer(Base):
    __tablename__ = "master_player"

    id: Mapped[int] = mapped_column(primary_key=True)
    master_team_id: Mapped[int] = mapped_column(ForeignKey("master_team.id"), index=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    position: Mapped[str] = mapped_column(String(20), index=True)
    overall: Mapped[int] = mapped_column(Integer)