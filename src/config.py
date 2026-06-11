"""Project configuration loaded from environment variables.

The project intentionally keeps all API keys outside source code. Values can be
provided through a local .env file or through system environment variables.
"""

from pathlib import Path
from dotenv import load_dotenv
import os


PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


LLM_PROVIDER = os.getenv("LLM_PROVIDER", "deepseek").strip().lower()
USE_DEMO_FALLBACK = os.getenv("USE_DEMO_FALLBACK", "true").strip().lower() in {
    "1",
    "true",
    "yes",
    "y",
}

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

OPENALEX_EMAIL = os.getenv("OPENALEX_EMAIL", "")
OPENALEX_BASE_URL = os.getenv("OPENALEX_BASE_URL", "https://api.openalex.org/works")
ARXIV_BASE_URL = os.getenv("ARXIV_BASE_URL", "http://export.arxiv.org/api/query")
NETWORK_PROXY = os.getenv("NETWORK_PROXY", "").strip()
