from pydantic import BaseModel

class Prediction(BaseModel):
    player: str
    team: str
    matchup: str
    predicted_points: float
    actual_points: float | None = None
    predicted_outcome: str | None = None