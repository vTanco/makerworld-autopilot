"""
Configuration manager for MakerWorld Autopilot.
Loads YAML configurations and environment variables with safe defaults.
"""

import os
import json
from pathlib import Path
from typing import Any, Dict

DEFAULT_CONFIG: Dict[str, Any] = {
    "makerworld": {
        "user_id": "",
        "auto_publish": False,
        "session_dir": "data/browser_profile",
        "default_license": "Standard Digital File License",
        "default_category": "Household/Organization",
    },
    "generation": {
        "mode": "procedural",
        "templates": [
            "gridfinity",
            "phone_stand",
            "cable_holder",
            "modular_bracket",
        ],
        "slicing": {
            "filament_type": "PLA",
            "layer_height": 0.20,
            "infill_percentage": 15,
            "brim_type": "auto",
        },
    },
    "rendering": {
        "engine": "internal",
        "blender_path": "/Applications/Blender.app/Contents/MacOS/Blender",
        "width": 1200,
        "height": 900,
        "angles": 4,
    },
    "copywriting": {
        "provider": "builtin",
        "language": "en",
    },
    "distribution": {
        "webhooks": {
            "discord_webhook_url": "",
            "telegram_bot_token": "",
            "telegram_chat_id": "",
        },
        "reddit": {
            "enabled": False,
            "client_id": "",
            "client_secret": "",
            "username": "",
            "password": "",
            "subreddits": ["3Dprinting", "BambuLab", "functionalprint"],
        },
        "pinterest": {
            "enabled": False,
            "access_token": "",
            "board_id": "",
        },
    },
    "scheduler": {
        "interval_hours": 6,
        "max_uploads_per_day": 4,
        "metrics_check_interval": 3,
    },
}


def load_env_file(filepath: Path) -> None:
    """Lightweight .env loader without external dependencies."""
    if not filepath.exists():
        return
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip("'\"")
                if k and k not in os.environ:
                    os.environ[k] = v
    except Exception:
        pass


def deep_merge(target: Dict[str, Any], source: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively merge source dictionary into target dictionary."""
    for key, value in source.items():
        if isinstance(value, dict) and key in target and isinstance(target[key], dict):
            deep_merge(target[key], value)
        else:
            target[key] = value
    return target


class Config:
    def __init__(self, base_dir: Path = None):
        self.base_dir = base_dir or Path(__file__).resolve().parent
        self.config_path = self.base_dir / "config.yaml"
        self.example_config_path = self.base_dir / "config.example.yaml"
        self.env_path = self.base_dir / ".env"
        
        # Load .env
        load_env_file(self.env_path)
        
        # Initialize config with defaults
        import copy
        self.data: Dict[str, Any] = copy.deepcopy(DEFAULT_CONFIG)
        
        # Try loading yaml file
        self._load_yaml()
        self._apply_env_overrides()

    def _load_yaml(self) -> None:
        path_to_load = self.config_path if self.config_path.exists() else self.example_config_path
        if not path_to_load.exists():
            return
        
        try:
            import yaml
            with open(path_to_load, "r", encoding="utf-8") as f:
                loaded = yaml.safe_load(f)
                if isinstance(loaded, dict):
                    deep_merge(self.data, loaded)
        except ImportError:
            # Basic fallback if pyyaml is not yet installed
            pass
        except Exception as e:
            print(f"[Config] Warning: Failed to parse YAML at {path_to_load}: {e}")

    def _apply_env_overrides(self) -> None:
        """Override configuration with environment variables if present."""
        if os.getenv("MAKERWORLD_USER_ID"):
            self.data["makerworld"]["user_id"] = os.getenv("MAKERWORLD_USER_ID")
        if os.getenv("DISCORD_WEBHOOK_URL"):
            self.data["distribution"]["webhooks"]["discord_webhook_url"] = os.getenv("DISCORD_WEBHOOK_URL")
        if os.getenv("TELEGRAM_BOT_TOKEN"):
            self.data["distribution"]["webhooks"]["telegram_bot_token"] = os.getenv("TELEGRAM_BOT_TOKEN")
        if os.getenv("TELEGRAM_CHAT_ID"):
            self.data["distribution"]["webhooks"]["telegram_chat_id"] = os.getenv("TELEGRAM_CHAT_ID")
        if os.getenv("REDDIT_CLIENT_ID"):
            self.data["distribution"]["reddit"]["client_id"] = os.getenv("REDDIT_CLIENT_ID")
            self.data["distribution"]["reddit"]["enabled"] = True
        if os.getenv("REDDIT_CLIENT_SECRET"):
            self.data["distribution"]["reddit"]["client_secret"] = os.getenv("REDDIT_CLIENT_SECRET")
        if os.getenv("REDDIT_USERNAME"):
            self.data["distribution"]["reddit"]["username"] = os.getenv("REDDIT_USERNAME")
        if os.getenv("REDDIT_PASSWORD"):
            self.data["distribution"]["reddit"]["password"] = os.getenv("REDDIT_PASSWORD")

    def get(self, key_path: str, default: Any = None) -> Any:
        keys = key_path.split(".")
        val = self.data
        for k in keys:
            if isinstance(val, dict) and k in val:
                val = val[k]
            else:
                return default
        return val


# Global config singleton
_config_instance = None


def get_config() -> Config:
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance
