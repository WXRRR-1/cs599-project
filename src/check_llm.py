"""Check DeepSeek connectivity without printing secrets."""

from __future__ import annotations

import sys

from config import (
    DEEPSEEK_API_KEY,
    DEEPSEEK_BASE_URL,
    DEEPSEEK_MODEL,
    LLM_DRY_RUN,
    LLM_PROVIDER,
    LLM_TIMEOUT_SECONDS,
    NETWORK_PROXY,
)


def _build_http_client():
    """Create a DeepSeek-only HTTP client using NETWORK_PROXY when configured."""
    if not NETWORK_PROXY:
        return None

    import httpx

    try:
        return httpx.Client(proxy=NETWORK_PROXY, timeout=LLM_TIMEOUT_SECONDS)
    except TypeError:
        return httpx.Client(proxies=NETWORK_PROXY, timeout=LLM_TIMEOUT_SECONDS)


def main() -> int:
    """Print safe LLM config and optionally make a tiny DeepSeek request."""
    print(f"LLM_PROVIDER={LLM_PROVIDER}")
    print(f"LLM_DRY_RUN={LLM_DRY_RUN}")
    print(f"DEEPSEEK_BASE_URL={DEEPSEEK_BASE_URL}")
    print(f"DEEPSEEK_MODEL={DEEPSEEK_MODEL}")
    print(f"NETWORK_PROXY enabled={bool(NETWORK_PROXY)}")
    print(f"DEEPSEEK_API_KEY configured={bool(DEEPSEEK_API_KEY)}")

    if LLM_PROVIDER != "deepseek":
        print("Skip real call: LLM_PROVIDER is not deepseek.")
        return 0

    if LLM_DRY_RUN:
        print("Skip real call: LLM_DRY_RUN=true.")
        return 0

    if not DEEPSEEK_API_KEY:
        print("Skip real call: DEEPSEEK_API_KEY is not configured.")
        return 1

    from openai import OpenAI

    http_client = _build_http_client()
    client_kwargs = {
        "api_key": DEEPSEEK_API_KEY,
        "base_url": DEEPSEEK_BASE_URL,
        "timeout": LLM_TIMEOUT_SECONDS,
    }
    if http_client is not None:
        client_kwargs["http_client"] = http_client

    client = OpenAI(**client_kwargs)

    try:
        response = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=[
                {"role": "user", "content": "请只回复：DeepSeek API connected"},
            ],
            temperature=0,
            max_tokens=20,
        )
        content = response.choices[0].message.content or ""
        print(f"DeepSeek test response: {content.strip()}")
        return 0
    except Exception as exc:
        print(f"DeepSeek test failed: {exc.__class__.__name__}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
