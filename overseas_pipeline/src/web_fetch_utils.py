"""
web_fetch_utils.py -- 共享的五层 fallback 抓取工具

被 page_scraper.py、faculty_scraper.py、course_catalog_scraper.py 导入。
对应 web-fetch-fallback skill 的五层策略：

  Layer 1:   curl + browser UA
  Layer 1.5: Jina Reader (r.jina.ai，免费，适合 Cloudflare 场景)
  Layer 2:   Tavily Extract API ($TAVILY_API_KEY)
  Layer 2.5: Wayback Machine (web.archive.org，适合博客/个人网站)
  Layer 3:   Tavily Search API (间接获取内容摘要)
"""

import os
import re
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    raise ImportError("requests library not found. Run: pip install requests")

# Load .env from overseas_pipeline/ root (two levels up from src/)
_env_path = Path(__file__).resolve().parent.parent / ".env"
if _env_path.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(_env_path, override=False)
    except ImportError:
        # Manual fallback if python-dotenv is not installed
        with open(_env_path) as _f:
            for _line in _f:
                _line = _line.strip()
                if _line and not _line.startswith("#") and "=" in _line:
                    _k, _v = _line.split("=", 1)
                    os.environ.setdefault(_k.strip(), _v.strip())

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TIMEOUT = 20

BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def log(msg: str) -> None:
    import sys
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", file=sys.stderr, flush=True)


def is_blocked(text: str) -> bool:
    """Check for Cloudflare/WAF blocks, empty responses, or JS SPA shells with no content."""
    if len(text) < 300:
        return True
    low = text.lower()
    signals = [
        "just a moment", "cf_chl_opt", "challenge-platform",
        "enable javascript", "403 forbidden", "access denied",
    ]
    if any(s in low for s in signals):
        return True
    # Detect JS SPA shells: page has <div id="app"></div> or <div id="root"></div>
    # with no meaningful text content (body text under 200 chars after stripping tags)
    if '<div id="app"></div>' in text or '<div id="root"></div>' in text:
        import re as _re
        body_text = _re.sub(r"<[^>]+>", " ", text)
        body_text = _re.sub(r"\s+", " ", body_text).strip()
        if len(body_text) < 200:
            return True
    return False


# ---------------------------------------------------------------------------
# Individual layers
# ---------------------------------------------------------------------------

def layer1_curl(url: str) -> str | None:
    log(f"Layer 1: curl {url}")
    try:
        resp = requests.get(url, headers=BROWSER_HEADERS, timeout=TIMEOUT)
        if is_blocked(resp.text):
            log("  ✗ Blocked (Cloudflare/WAF)")
            return None
        log(f"  ✓ {len(resp.text)} chars")
        return resp.text
    except Exception as e:
        log(f"  ✗ {e}")
        return None


def layer1_5_jina(url: str) -> str | None:
    log(f"Layer 1.5: Jina Reader")
    try:
        resp = requests.get(
            f"https://r.jina.ai/{url}",
            headers={"User-Agent": BROWSER_HEADERS["User-Agent"], "Accept": "text/plain"},
            timeout=TIMEOUT,
        )
        text = resp.text
        if len(text) < 500 or "error" in text[:200].lower():
            log("  ✗ Short/error response")
            return None
        log(f"  ✓ {len(text)} chars")
        return text
    except Exception as e:
        log(f"  ✗ {e}")
        return None


def layer2_tavily_extract(url: str) -> str | None:
    if not TAVILY_API_KEY:
        log("  ⚠ TAVILY_API_KEY not set, skipping Layer 2")
        return None
    log("Layer 2: Tavily Extract")
    try:
        resp = requests.post(
            "https://api.tavily.com/extract",
            headers={
                "Authorization": f"Bearer {TAVILY_API_KEY}",
                "Content-Type": "application/json",
            },
            json={"urls": [url]},
            timeout=TIMEOUT,
        )
        results = resp.json().get("results", [])
        if not results:
            log("  ✗ No results")
            return None
        content = results[0].get("raw_content", "")
        log(f"  ✓ {len(content)} chars")
        return content if content else None
    except Exception as e:
        log(f"  ✗ {e}")
        return None


def layer2_5_wayback(url: str) -> str | None:
    log("Layer 2.5: Wayback Machine")
    for year in ["2024", "2023"]:
        wayback_url = f"https://web.archive.org/web/{year}/{url}"
        try:
            resp = requests.get(wayback_url, headers=BROWSER_HEADERS, timeout=TIMEOUT)
            if not is_blocked(resp.text) and len(resp.text) > 500:
                log(f"  ✓ {len(resp.text)} chars (year={year})")
                return resp.text
        except Exception as e:
            log(f"  ✗ year={year}: {e}")
    return None


def layer3_tavily_search(url: str, search_hint: str = "") -> str | None:
    if not TAVILY_API_KEY:
        log("  ⚠ TAVILY_API_KEY not set, skipping Layer 3")
        return None
    domain = url.split("/")[2] if "//" in url else url
    query = search_hint if search_hint else f"site:{domain}"
    log(f"Layer 3: Tavily Search '{query}'")
    try:
        resp = requests.post(
            "https://api.tavily.com/search",
            headers={
                "Authorization": f"Bearer {TAVILY_API_KEY}",
                "Content-Type": "application/json",
            },
            json={"query": query, "max_results": 5, "include_raw_content": True},
            timeout=TIMEOUT,
        )
        results = resp.json().get("results", [])
        if not results:
            log("  ✗ No results")
            return None
        combined = "\n\n".join(r.get("content", "") for r in results)
        log(f"  ✓ {len(combined)} chars from {len(results)} results")
        return combined if combined else None
    except Exception as e:
        log(f"  ✗ {e}")
        return None


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def fetch_with_fallback(url: str, search_hint: str = "") -> tuple[str | None, str]:
    """
    五层 fallback 抓取，返回 (content, layer_used)。

    Args:
        url:         目标 URL
        search_hint: Layer 3 Tavily Search 的搜索词（留空则用 site:{domain}）

    Returns:
        (content, layer_used) — content 为 None 表示全部失败
    """
    for fn, label in [
        (lambda: layer1_curl(url),                         "layer1_curl"),
        (lambda: layer1_5_jina(url),                       "layer1.5_jina"),
        (lambda: layer2_tavily_extract(url),               "layer2_tavily_extract"),
        (lambda: layer2_5_wayback(url),                    "layer2.5_wayback"),
        (lambda: layer3_tavily_search(url, search_hint),   "layer3_tavily_search"),
    ]:
        content = fn()
        if content:
            return content, label

    return None, "all_failed"


# ── CLI entry point ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    import sys

    ap = argparse.ArgumentParser(
        description=(
            "Five-layer fallback fetch (Layer 1→1.5→2→2.5→3). "
            "Prints fetched content to stdout. Layer used is shown in the first line."
        )
    )
    ap.add_argument("url", help="Target URL to fetch")
    ap.add_argument(
        "--search-hint", default="",
        metavar="HINT",
        help="Search keywords for Layer 3 Tavily Search (default: site:{domain})",
    )
    args = ap.parse_args()

    content, layer = fetch_with_fallback(args.url, args.search_hint)
    if content:
        print(f"<!-- fetched via: {layer} -->")
        print(content)
    else:
        print("ERROR: all layers failed", file=sys.stderr)
        sys.exit(1)
