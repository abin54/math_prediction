import logging
import os
from datetime import datetime

class ForensicLogger:
    """
    Unified Logger for the Sovereign Hub.
    Handles persistent logs and formatted console output.
    """
    
    def __init__(self, name="SovereignHub", log_dir="logs"):
        self.name = name
        self.log_dir = log_dir
        
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
            
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)
        
        # Prevent duplicate handlers if singleton is reused
        if not self.logger.handlers:
            self._setup_handlers()

    def _setup_handlers(self):
        """Configure file and console logging."""
        log_file = os.path.join(self.log_dir, f"{datetime.now().strftime('%Y-%m-%d')}_audit.log")
        
        # File Handler (Full Detail)
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)
        
        # Console Handler (High-Level Status)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Formatting
        formatter = logging.Formatter('  [%(levelname)s] %(message)s')
        fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        ch.setFormatter(formatter)
        
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def log_phase(self, phase_name, message):
        """Special formatting for Phase-Gate transitions."""
        self.logger.info(f"Phase {phase_name}: {message}")

    def log_evidence(self, engine_name, evidence):
        """Formats and logs historical evidence from engines."""
        self.logger.debug(f"{engine_name} Evidence: {evidence}")

    def info(self, msg): self.logger.info(msg)
    def error(self, msg): self.logger.error(msg)
    def debug(self, msg): self.logger.debug(msg)
    def warning(self, msg): self.logger.warning(msg)
