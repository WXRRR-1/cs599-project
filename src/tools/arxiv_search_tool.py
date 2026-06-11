"""Paper search tool based on the public arXiv API.

The arXiv API does not require an API key and returns Atom XML. This module uses
Python standard library urllib, matching arXiv's official Python example, and
normalizes entries into the same schema used by the rest of the project.
"""

from __future__ import annotations

from datetime import datetime
from urllib.parse import urlencode
from urllib.request import ProxyHandler, Request, build_opener, urlopen
import xml.etree.ElementTree as ET

from config import ARXIV_BASE_URL, NETWORK_PROXY


ARXIV_NS = {"atom": "http://www.w3.org/2005/Atom"}


def _find_text(entry: ET.Element, tag: str) -> str:
    node = entry.find(f"atom:{tag}", ARXIV_NS)
    if node is None or node.text is None:
        return ""
    return " ".join(node.text.split())


def _extract_year(published: str) -> int | str:
    if not published:
        return "N/A"
    try:
        return datetime.fromisoformat(published.replace("Z", "+00:00")).year
    except ValueError:
        return published[:4] if len(published) >= 4 else "N/A"


def _extract_authors(entry: ET.Element) -> str:
    names = []
    for author in entry.findall("atom:author", ARXIV_NS):
        name = author.find("atom:name", ARXIV_NS)
        if name is not None and name.text:
            names.append(" ".join(name.text.split()))
    return ", ".join(names)


def _extract_url(entry: ET.Element) -> str:
    for link in entry.findall("atom:link", ARXIV_NS):
        if link.attrib.get("type") == "text/html":
            return link.attrib.get("href", "")
    return _find_text(entry, "id")


def _open_url(url: str, timeout: int = 30):
    request = Request(url, headers={"User-Agent": "ResearchFlow-Agent/0.1"})
    if not NETWORK_PROXY:
        return urlopen(request, timeout=timeout)

    opener = build_opener(
        ProxyHandler(
            {
                "http": NETWORK_PROXY,
                "https": NETWORK_PROXY,
            }
        )
    )
    return opener.open(request, timeout=timeout)


def search_arxiv_papers(query: str, limit: int = 10) -> list[dict]:
    """Search papers from arXiv and return normalized paper records."""
    if not query.strip():
        print("请输入有效的 arXiv 检索主题。")
        return []

    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max(1, min(limit, 50)),
        "sortBy": "relevance",
        "sortOrder": "descending",
    }
    url = f"{ARXIV_BASE_URL}?{urlencode(params)}"

    try:
        with _open_url(url) as response:
            xml_bytes = response.read()
        root = ET.fromstring(xml_bytes)
    except TimeoutError:
        print("arXiv API 请求失败：TimeoutError")
        return []
    except OSError as exc:
        print(f"arXiv API 请求失败：{exc.__class__.__name__}")
        return []
    except ET.ParseError as exc:
        print(f"arXiv API 返回内容无法解析：{exc}")
        return []

    papers = []
    for entry in root.findall("atom:entry", ARXIV_NS):
        title = _find_text(entry, "title")
        abstract = _find_text(entry, "summary")
        if not title or not abstract:
            continue

        papers.append(
            {
                "title": title,
                "authors": _extract_authors(entry),
                "year": _extract_year(_find_text(entry, "published")),
                "abstract": abstract,
                "citationCount": 0,
                "url": _extract_url(entry),
                "venue": "arXiv",
            }
        )

    return papers
