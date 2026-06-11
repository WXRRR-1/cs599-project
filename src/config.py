"""Project configuration loaded from environment variables.

The project intentionally keeps all API keys outside source code. Values can be
provided through a local .env file or through system environment variables.
"""

from pathlib import Path
from dotenv import load_dotenv
import os


PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


def _get_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y"}


def _get_int(name: str, default: int, min_value: int = 1) -> int:
    try:
        return max(min_value, int(os.getenv(name, str(default))))
    except (TypeError, ValueError):
        return default


LLM_PROVIDER = os.getenv("LLM_PROVIDER", "deepseek").strip().lower()
LLM_DRY_RUN = _get_bool("LLM_DRY_RUN", True)
MAX_LLM_PAPERS = _get_int("MAX_LLM_PAPERS", 5)
MAX_ABSTRACT_CHARS = _get_int("MAX_ABSTRACT_CHARS", 2000)
LLM_TIMEOUT_SECONDS = _get_int("LLM_TIMEOUT_SECONDS", 30)
LLM_MAX_RETRIES = _get_int("LLM_MAX_RETRIES", 1, min_value=0)
USE_DEMO_FALLBACK = _get_bool("USE_DEMO_FALLBACK", True)

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

OPENALEX_EMAIL = os.getenv("OPENALEX_EMAIL", "")
OPENALEX_BASE_URL = os.getenv("OPENALEX_BASE_URL", "https://api.openalex.org/works")
ARXIV_BASE_URL = os.getenv("ARXIV_BASE_URL", "http://export.arxiv.org/api/query")
NETWORK_PROXY = os.getenv("NETWORK_PROXY", "").strip()
