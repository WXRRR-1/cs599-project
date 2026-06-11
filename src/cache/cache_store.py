"""Small JSON cache used to reduce repeated academic and LLM API calls."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from config import PROJECT_ROOT


CACHE_DIR = PROJECT_ROOT / "src" / "outputs" / "cache"
CACHE_FILES = {
    "search": CACHE_DIR / "search_cache.json",
    "summary": CACHE_DIR / "summary_cache.json",
}


def _cache_path(cache_name: str) -> Path:
    return CACHE_FILES.get(cache_name, CACHE_DIR / f"{cache_name}_cache.json")


def load_cache(cache_name: str) -> dict:
    """Load one cache dictionary, returning an empty cache on failure."""
    path = _cache_path(cache_name)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_text("{}", encoding="utf-8")
            return {}
        data = json.loads(path.read_text(encoding="utf-8") or "{}")
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError) as exc:
        print(f"缓存读取失败：{cache_name} {exc.__class__.__name__}")
        return {}


def save_cache(cache_name: str, data: dict) -> None:
    """Save one cache dictionary, swallowing write errors."""
    path = _cache_path(cache_name)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError as exc:
        print(f"缓存写入失败：{cache_name} {exc.__class__.__name__}")


def make_cache_key(*parts: Any) -> str:
    """Create a stable cache key without storing sensitive values."""
    payload = json.dumps(parts, ensure_ascii=False, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def get_cached_value(cache_name: str, key: str):
    """Read one cached value by key."""
    return load_cache(cache_name).get(key)


def set_cached_value(cache_name: str, key: str, value) -> None:
    """Set one cached value by key."""
    data = load_cache(cache_name)
    data[key] = value
    save_cache(cache_name, data)
