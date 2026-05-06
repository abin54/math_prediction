from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class MatchState(BaseModel):
    """
    Standardized IPL Match State with validation.
    """
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "over": 15.2,
                "ball": 2,
                "runs_scored": 1,
                "wickets_fallen": 4,
                "total_runs": 142,
                "striker_runs": 45,
                "striker_balls": 30,
                "non_striker_runs": 12,
                "non_striker_balls": 8,
                "is_wicket_ball": False,
                "venue": "Wankhede Stadium, Mumbai",
                "chasing_target": 185,
                "bowler_wickets": 2,
                "bowler_runs": 24,
                "bowler_overs": 3.2
            }
        }
    )

    over: float = Field(..., ge=0, le=20, description="Current over number")
    ball: int = Field(..., ge=1, le=6, description="Current ball in over")
    runs_scored: int = Field(..., ge=0, description="Runs scored in current ball")
    wickets_fallen: int = Field(..., ge=0, le=10, description="Total wickets fallen")
    total_runs: int = Field(..., ge=0, description="Current total runs")
    striker_runs: int = Field(..., ge=0)
    striker_balls: int = Field(..., ge=0)
    non_striker_runs: int = Field(..., ge=0)
    non_striker_balls: int = Field(..., ge=0)
    is_wicket_ball: bool = False
    venue: str = Field(..., min_length=3)
    chasing_target: Optional[int] = Field(None, ge=0)
    bowler_wickets: int = Field(..., ge=0)
    bowler_runs: int = Field(..., ge=0)
    bowler_overs: float = Field(..., ge=0, le=4)
