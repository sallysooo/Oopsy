import yaml
import os

DEFAULT_CONFIG = {
    "enabled_rules": None,
    "log_enabled": True,
    "auto_mode": False
}

def load_config():
    path = os.path.expanduser("~/.oopsyrc")
    if not os.path.exists(path):
        return DEFAULT_CONFIG
    try:
        with open(path, "r") as f:
            user_config = yaml.safe_load(f)
            return {**DEFAULT_CONFIG, **(user_config or {})}
    except Exception as e:
        print(f"[ERROR] Failed to load .oopsyrc: {e}")
        return DEFAULT_CONFIG
