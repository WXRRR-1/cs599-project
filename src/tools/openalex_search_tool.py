"""Paper search tool based on OpenAlex Works API.

OpenAlex provides broad scholarly metadata across disciplines. This tool can
send an optional OPENALEX_EMAIL value as a polite-pool contact parameter.
"""

from __future__ import annotations

import requests

from cache.cache_store import get_cached_value, make_cache_key, set_cached_value
from config import OPENALEX_BASE_URL, OPENALEX_EMAIL
from tools.http_client import describe_request_error, get_request_proxies


_LAST_CACHE_HIT = False


def get_last_openalex_cache_hit() -> bool:
    """Return whether the latest OpenAlex search was served from cache."""
    return _LAST_CACHE_HIT


def _restore_abstract(inverted_index: dict | None) -> str:
    """Restore OpenAlex abstract text from its inverted-index representation."""
    if not inverted_index:
        return ""

    positions: list[tuple[int, str]] = []
    for word, indexes in inverted_index.items():
        if not isinstance(indexes, list):
            continue
        for index in indexes:
            if isinstance(index, int):
                positions.append((index, word))

    return " ".join(word for _, word in sorted(positions))


def _extract_authors(work: dict) -> str:
    names = []
    for authorship in work.get("authorships") or []:
        author = authorship.get("author") or {}
        name = author.get("display_name")
        if name:
            names.append(name)
    return ", ".join(names)


def _extract_url(work: dict) -> str:
    primary_location = work.get("primary_location") or {}
    best_oa_location = work.get("best_oa_location") or {}
    ids = work.get("ids") or {}

    return (
        primary_location.get("landing_page_url")
        or best_oa_location.get("landing_page_url")
        or ids.get("doi")
        or work.get("doi")
        or work.get("id")
        or ""
    )


def _extract_venue(work: dict) -> str:
    primary_location = work.get("primary_location") or {}
    source = primary_location.get("source") or {}
    return source.get("display_name") or "OpenAlex"


def search_openalex_papers(query: str, limit: int = 10) -> list[dict]:
    """Search papers from OpenAlex and return normalized paper records."""
    global _LAST_CACHE_HIT
    _LAST_CACHE_HIT = False

    if not query.strip():
        print("请输入有效的 OpenAlex 检索主题。")
        return []

    normalized_limit = max(1, min(limit, 100))
    cache_key = make_cache_key("openalex", query.strip().lower(), normalized_limit)
    cached = get_cached_value("search", cache_key)
    if isinstance(cached, list):
        _LAST_CACHE_HIT = True
        return cached

    params = {
        "search": query,
        "per_page": normalized_limit,
        "sort": "relevance_score:desc",
        "select": ",".join(
            [
                "id",
                "doi",
                "display_name",
                "publication_year",
                "authorships",
                "cited_by_count",
                "primary_location",
                "best_oa_location",
                "ids",
                "abstract_inverted_index",
            ]
        ),
    }
    if OPENALEX_EMAIL:
        params["mailto"] = OPENALEX_EMAIL

    try:
        response = requests.get(
            OPENALEX_BASE_URL,
            params=params,
            proxies=get_request_proxies(),
            timeout=20,
        )
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as exc:
        print(f"OpenAlex API 请求失败：{describe_request_error(exc)}")
        return []
    except ValueError as exc:
        print(f"OpenAlex API 返回内容无法解析：{exc}")
        return []

    papers = []
    for work in data.get("results", []):
        title = work.get("display_name") or ""
        abstract = _restore_abstract(work.get("abstract_inverted_index"))
        if not title or not abstract:
            continue

        papers.append(
            {
                "title": title,
                "authors": _extract_authors(work),
                "year": work.get("publication_year") or "N/A",
                "abstract": abstract,
                "citationCount": work.get("cited_by_count") or 0,
                "url": _extract_url(work),
                "venue": _extract_venue(work),
                "source": "OpenAlex",
            }
        )

    if papers:
        set_cached_value("search", cache_key, papers)

    return papers
