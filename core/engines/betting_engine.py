from pydantic import BaseModel
from typing import List, Dict
from core.models.match_state import MatchState
from core.utils.logger import sovereign_logger as logger

class Odds(BaseModel):
    home: float
    away: float

class Volatility(BaseModel):
    label: str
    score: float

class ProjectedTotal(BaseModel):
    projected_total: float

class BettingMetrics(BaseModel):
    decimal_odds: Odds
    market_volatility: Volatility
    over_under_lines: List[ProjectedTotal]

class BettingEngine:
    """
    Calculates betting metrics and market volatility from win probabilities.
    """
    
    @staticmethod
    def calculate_metrics(win_prob: float, state: MatchState) -> BettingMetrics:
        """
        Derives betting odds and projections.
        """
        logger.debug(f"Calculating betting metrics for win_prob {win_prob}")
        
        # Decimal odds calculation (1/p)
        home_odds = round(1.0 / win_prob, 2) if win_prob > 0 else 100.0
        away_odds = round(1.0 / (1.0 - win_prob), 2) if win_prob < 1 else 100.0
        
        # Volatility estimation based on state
        volatility_score = 0.5 + (state.wickets_fallen * 0.05)
        vol_label = "HIGH" if volatility_score > 0.7 else "MEDIUM" if volatility_score > 0.4 else "LOW"
        
        return BettingMetrics(
            decimal_odds=Odds(home=home_odds, away=away_odds),
            market_volatility=Volatility(label=vol_label, score=volatility_score),
            over_under_lines=[ProjectedTotal(projected_total=state.total_runs * 1.2)] # Simple heuristic
        )
