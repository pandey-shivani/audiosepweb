import os
from pathlib import Path
from typing import Optional, List, Any, Dict

import yaml
from pydantic import field_validator, ValidationInfo
from pydantic_settings import BaseSettings
from functools import lru_cache



class Settings(BaseSettings):
    host: Optional[str] = "0.0.0.0"
    port: Optional[int] = 8000

    model_config_path: str
    model_checkpoints_path: str
        

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

        base_fields = set(cls.model_fields.keys())
        base_settings = {}
        extra_settings = {}

        for key, setting in config_data.items():
            if key in base_fields:
                base_settings[key] = setting
            else:
                extra_settings[key] = setting
        try:
            return cls(**base_settings, extra_settings=extra_settings) # TODO support extra_configs

        except Exception as e:
            raise Exception(f"Unable to load settings.\nError: {str(e)}")




