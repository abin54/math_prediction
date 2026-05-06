import pytest
from core.models.match_state import MatchState
from core.engines.betting_engine import BettingEngine
from core.utils.config_manager import ConfigManager

def test_match_state_validation():
    """Tests that MatchState correctly validates input."""
    valid_data = {
        "over": 10.0, "ball": 1, "runs_scored": 0, "wickets_fallen": 2,
        "total_runs": 80, "striker_runs": 20, "striker_balls": 15,
        "non_striker_runs": 10, "non_striker_balls": 10,
        "venue": "Test Stadium", "bowler_wickets": 1,
        "bowler_runs": 15, "bowler_overs": 2.0
    }
    state = MatchState(**valid_data)
    assert state.over == 10.0
    
    with pytest.raises(ValueError):
        # Invalid over
        MatchState(**{**valid_data, "over": 25.0})

def test_betting_odds_calculation():
    """Tests the logic for calculating decimal odds."""
    state = MatchState(
        over=10.0, ball=1, runs_scored=0, wickets_fallen=2,
        total_runs=80, striker_runs=20, striker_balls=15,
        non_striker_runs=10, non_striker_balls=10,
        venue="Test Stadium", bowler_wickets=1,
        bowler_runs=15, bowler_overs=2.0
    )
    metrics = BettingEngine.calculate_metrics(0.5, state)
    assert metrics.decimal_odds.home == 2.0
    assert metrics.decimal_odds.away == 2.0

def test_config_loading():
    """Tests that ConfigManager loads default values."""
    name = ConfigManager.get("project.name")
    assert name is not None
    assert "Sovereign" in name
