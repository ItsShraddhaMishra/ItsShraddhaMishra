# readme_config.py

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional


ROOT = Path(__file__).resolve().parent

LOCAL_ENV_FILES = [
    ROOT / ".env",
    ROOT / ".secrets" / "readme.env",
]


@dataclass(frozen=True)
class ReadmeConfig:
    github_username: str
    github_token: Optional[str]
    display_name: str
    theme: str
    assets_dir: Path
    data_dir: Path


def _parse_env_file(path: Path) -> Dict[str, str]:
    values: Dict[str, str] = {}

    if not path.exists():
        return values

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()

        if not line or line.startswith("#"):
            continue

        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        if not key:
            continue

        if (
            len(value) >= 2
            and value[0] == value[-1]
            and value[0] in {"'", '"'}
        ):
            value = value[1:-1]

        values[key] = value

    return values


def _load_local_env() -> Dict[str, str]:
    merged: Dict[str, str] = {}

    for env_file in LOCAL_ENV_FILES:
        merged.update(_parse_env_file(env_file))

    return merged


def _get(
    name: str,
    local_env: Dict[str, str],
    default: Optional[str] = None,
) -> Optional[str]:
    value = os.getenv(name)

    if value is not None and value != "":
        return value

    value = local_env.get(name)

    if value is not None and value != "":
        return value

    return default


def load_config() -> ReadmeConfig:
    local_env = _load_local_env()

    github_username = _get(
        "GITHUB_USERNAME",
        local_env,
        "ItsShraddhaMishra",
    )

    github_token = (
        _get("README_GITHUB_TOKEN", local_env)
        or _get("GITHUB_TOKEN", local_env)
        or _get("GH_TOKEN", local_env)
    )

    display_name = _get(
        "README_DISPLAY_NAME",
        local_env,
        "SHRADDHA MISHRA",
    )

    theme = _get(
        "README_THEME",
        local_env,
        "red",
    )

    assets_dir = ROOT / _get(
        "README_ASSETS_DIR",
        local_env,
        "assets",
    )

    data_dir = ROOT / _get(
        "README_DATA_DIR",
        local_env,
        "data",
    )

    return ReadmeConfig(
        github_username=github_username,
        github_token=github_token,
        display_name=display_name,
        theme=theme,
        assets_dir=assets_dir,
        data_dir=data_dir,
    )


def require_github_token() -> str:
    config = load_config()

    if not config.github_token:
        raise RuntimeError(
            "Missing GitHub token. Set README_GITHUB_TOKEN, GITHUB_TOKEN, or GH_TOKEN. "
            "For local use, put it in .env. For GitHub Actions, use repository secrets."
        )

    return config.github_token
