"""Read, write, and incrementally update profile.yaml."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

DEFAULT_PATH = Path(__file__).parent / "profile.yaml"


def load_profile(path: Path = DEFAULT_PATH) -> dict[str, Any]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    return yaml.safe_load(text) or {}


def save_profile(data: dict[str, Any], path: Path = DEFAULT_PATH) -> None:
    path.write_text(
        yaml.dump(data, default_flow_style=False, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )


def update_profile(
    category: str,
    key: str,
    value: Any,
    path: Path = DEFAULT_PATH,
) -> dict[str, Any]:
    """Add or overwrite a single key under *category* and persist."""
    data = load_profile(path)
    if category not in data:
        data[category] = {}
    data[category][key] = value
    save_profile(data, path)
    return data


def get_value(data: dict[str, Any], category: str, key: str) -> Any | None:
    return data.get(category, {}).get(key)
