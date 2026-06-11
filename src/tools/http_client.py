"""Shared HTTP helpers for academic API calls."""

from __future__ import annotations

import requests

from config import NETWORK_PROXY


def get_request_proxies() -> dict[str, str] | None:
    """Return requests-compatible proxy settings from .env, if configured."""
    if not NETWORK_PROXY:
        return None
    return {
        "http": NETWORK_PROXY,
        "https": NETWORK_PROXY,
    }


def describe_request_error(exc: requests.RequestException) -> str:
    """Return a short, safe error message without leaking API keys in URLs."""
    status_code = getattr(exc.response, "status_code", None)
    if status_code:
        return f"HTTP {status_code}"
    return exc.__class__.__name__
