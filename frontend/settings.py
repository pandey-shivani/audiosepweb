import os
from pathlib import Path
from typing import Optional, List, Any, Dict

import yaml
from pydantic import field_validator, ValidationInfo
from pydantic_settings import BaseSettings
from functools import lru_cache



class Settings(BaseSettings):
    
    base_api_url: str
        
    @classmethod
    def load_from_yaml(cls, yaml_path: str = None) -> "Settings":
        if yaml_path is None:
            root_path = Path(__file__).parent
            yaml_path = root_path / f"settings.yaml"

        if not yaml_path.exists():
            msg = f"Not found config file: {yaml_path!s}"
            raise FileNotFoundError(msg)

        with yaml_path.open("r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f)

        return cls(**config_data)





