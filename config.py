import json
import os
from typing import Dict, Any


class Config:
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self._config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Configuration file {self.config_file} not found")

        with open(self.config_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get(self, key: str, default=None):
        """Get configuration value by dot-separated key (e.g., 'database.path')"""
        keys = key.split('.')
        value = self._config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    @property
    def database_path(self):
        return self.get('database.path', 'dop_fx.db')

    @property
    def central_bank_url(self):
        return self.get('sources.central_bank.url')

    @property
    def request_timeout(self):
        return self.get('sources.central_bank.timeout', 30)


# Global config instance
config = Config()