from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict
import yaml
import os

@dataclass
class ModelConfig:
    type: str = "hybrid_ensemble"
    parameters: Dict[str, Any] = field(default_factory=dict)
    path: str = "models/hybrid_ensemble"

@dataclass
class DataConfig:
    raw_path: str = "data/raw"
    processed_path: str = "data/processed"
    features: list[dict[str, Any]] = field(default_factory=list)

@dataclass
class APIConfig:
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4
    cors_origins: list[str] = field(default_factory=lambda: ["*"])

@dataclass
class Config:
    model: ModelConfig
    data: DataConfig
    api: APIConfig
    
    @classmethod
    def from_yaml(cls, path: Path) -> "Config":
        with open(path) as f:
            raw = yaml.safe_load(f)
        return cls(
            model=ModelConfig(**raw.get("model", {})),
            data=DataConfig(**raw.get("data", {})),
            api=APIConfig(**raw.get("api", {})),
        )
    
    @classmethod
    def from_env(cls) -> "Config":
        config_path = Path(os.getenv("CONFIG_PATH", "configs/base.yaml"))
        if config_path.exists():
            return cls.from_yaml(config_path)
        return cls.get_default()

    @classmethod
    def get_default(cls) -> "Config":
        return cls(
            model=ModelConfig(),
            data=DataConfig(),
            api=APIConfig()
        )

def get_config() -> Config:
    return Config.from_env()
