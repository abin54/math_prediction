import yaml
from pathlib import Path
from typing import Any, Dict, Optional
from core.utils.path_manager import PathManager

class ConfigManager:
    """
    Loads and provides access to configuration settings.
    """
    
    _config: Dict[str, Any] = {}
    
    @classmethod
    def load(cls, config_file: str = "settings.yaml"):
        """Loads configuration from a YAML file."""
        path = PathManager.get_config_path(config_file)
        if not path.exists():
            # Create default config if it doesn't exist
            cls._create_default_config(path)
            
        with open(path, 'r') as f:
            cls._config = yaml.safe_load(f)
            
    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """Retrieves a configuration value by key (supports dot notation)."""
        keys = key.split('.')
        value = cls._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            if value is None:
                return default
        return value

    @classmethod
    def _create_default_config(cls, path: Path):
        """Creates a default settings.yaml file."""
        default_config = {
            "project": {
                "name": "Sovereign AI Math Prediction",
                "version": "1.0.0"
            },
            "models": {
                "hybrid_path": "models/hybrid_ensemble",
                "ollama": {
                    "model_name": "llama3.2:3b",
                    "url": "http://localhost:11434/api/generate"
                }
            },
            "inference": {
                "confidence_threshold": 0.85
            },
            "logging": {
                "level": "INFO",
                "file_output": True
            }
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False)

# Initialize on import
ConfigManager.load()
