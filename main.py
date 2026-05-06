import sys
from core.utils.logger import sovereign_logger as logger
from core.utils.config_manager import ConfigManager
from core.engines.ipl_engine import IPLEngine
from core.engines.forensic_auditor import ForensicAuditor
from core.engines.betting_engine import BettingEngine
from core.models.match_state import MatchState

class SovereignApp:
    """
    Main application orchestrator for Sovereign AI Math Prediction.
    """
    
    def __init__(self):
        logger.info("Initializing Sovereign AI Application")
        self.ipl_engine = IPLEngine()
        self.auditor = ForensicAuditor()
        self.betting_engine = BettingEngine()
        
    def run_ipl_audit(self, batting_team: str = "MI", bowling_team: str = "CSK"):
        """Executes a full forensic audit cycle."""
        logger.info(f"Starting IPL Forensic Audit: {batting_team} vs {bowling_team}")
        
        # 1. Generate/Fetch Match State
        state = self._get_sample_state()
        
        # 2. ML Inference
        win_prob = self.ipl_engine.predict_win_probability(state, batting_team)
        logger.info(f"Hybrid Probability ({batting_team} Win): {win_prob:.2%}")
        
        # 3. Betting Metrics
        metrics = self.betting_engine.calculate_metrics(win_prob, state)
        logger.info(f"Decimal Odds: {metrics.decimal_odds.home} (Home) | {metrics.decimal_odds.away} (Away)")
        
        # 4. Forensic Audit (Ollama)
        audit_res = self.auditor.audit_win_probability(batting_team, win_prob, state.dict())
        logger.info(f"Ollama Audit Result: {audit_res[:100]}...")
        
        # 5. Final Verdict
        self._print_verdict(batting_team, win_prob)
        
    def _get_sample_state(self) -> MatchState:
        """Helper to create a sample match state for demonstration."""
        return MatchState(
            over=15.2,
            ball=2,
            runs_scored=1,
            wickets_fallen=4,
            total_runs=142,
            striker_runs=45,
            striker_balls=30,
            non_striker_runs=12,
            non_striker_balls=8,
            venue="Wankhede Stadium, Mumbai",
            chasing_target=185,
            bowler_wickets=2,
            bowler_runs=24,
            bowler_overs=3.2
        )

    def _print_verdict(self, team: str, prob: float):
        """Prints the final verdict in a structured way."""
        print("\n" + "="*80)
        print(f"  SUPREME VERDICT: {team} WIN PROBABILITY: {prob:.1%}")
        action = 'BACK' if prob > 0.6 else 'LAY' if prob < 0.4 else 'HOLD'
        print(f"  RECOMMENDED ACTION: {action}")
        print("="*80 + "\n")

def main():
    try:
        app = SovereignApp()
        app.run_ipl_audit()
    except KeyboardInterrupt:
        logger.info("Application stopped by user.")
    except Exception as e:
        logger.exception(f"Critical application failure: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
