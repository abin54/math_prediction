import os
from pathlib import Path
from typing import Union

class PathManager:
    """
    Centralized path management for the Sovereign AI project.
    Resolves paths relative to the project root, ensuring portability.
    """
    
    ROOT = Path(__file__).parent.parent.parent.absolute()
    
    # Core directories
    CORE = ROOT / "core"
    DATA = ROOT / "data"
    MODELS = ROOT / "models"
    CONFIG = ROOT / "config"
    LOGS = ROOT / "logs"
    ENGINES = ROOT / "engines"
    
    @classmethod
    def get_data_path(cls, filename: str) -> Path:
        """Returns the absolute path to a file in the data directory."""
        return cls.DATA / filename
    
    @classmethod
    def get_model_path(cls, filename: str) -> Path:
        """Returns the absolute path to a file in the models directory."""
        return cls.MODELS / filename
    
    @classmethod
    def get_config_path(cls, filename: str) -> Path:
        """Returns the absolute path to a file in the config directory."""
        return cls.CONFIG / filename
    
    @classmethod
    def ensure_dirs(cls):
        """Ensures all core directories exist."""
        for path in [cls.DATA, cls.MODELS, cls.CONFIG, cls.LOGS, cls.ENGINES]:
            path.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    print(f"Project Root: {PathManager.ROOT}")
    PathManager.ensure_dirs()
