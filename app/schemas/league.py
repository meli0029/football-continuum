from pydantic import BaseModel


class CreateLeagueRequest(BaseModel):
    name: str
    competition_ids: list[int]