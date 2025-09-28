import json
import os
from pathlib import Path
from typing import Any

APP_NAME = "CopperBrowserV1"

def app_root() -> Path:
    base = Path(os.getenv("APPDATA")) / APP_NAME
    (base / "profiles" / "default" / "data").mkdir(parents=True, exist_ok=True)
    return base

def profile_root(profile: str = "default") -> Path:
    return app_root() / "profiles" / profile

def data_file(name: str, profile: str = "default") -> Path:
    return profile_root(profile) / "data" / f"{name}.json"

def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default