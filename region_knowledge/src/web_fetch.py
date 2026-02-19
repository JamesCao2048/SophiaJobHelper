#!/usr/bin/env python3
"""
Web content fetcher with fallback strategy.

Strategy:
  1. Direct fetch with browser User-Agent
  1.5. Jina Reader (renders JS, bypasses Medium/Cloudflare)
  2. Tavily Extract API
  2.5. Wayback Machine (for Medium/blogs with archived snapshots)
  3. Tavily Search API (if search_query provided)

Usage:
  python web_fetch.py <url>                    # fetch single URL
  python web_fetch.py <url> --query "extra context"  # fetch with search context
  python web_fetch.py --search "query string"  # search only (no direct fetch)

Output: markdown content to stdout
"""

import sys
import os
import argparse
import subprocess
import json

TAVILY_API_KEY = os.environ.get(
    "TAVILY_API_KEY",
    "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",
)

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

TIMEOUT = 15


# ── Layer 1: Direct fetch via curl ──────────────────────────

def direct_fetch(url: str) -> str | None:
    """Fetch URL content using curl with browser User-Agent."""
    try:
        result = subprocess.run(
            [
                "curl", "-s", "-L",
                "-H", f"User-Agent: {USER_AGENT}",
                "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "-H", "Accept-Language: en-US,en;q=0.9",
                "--max-time", str(TIMEOUT),
                url,
            ],
            capture_output=True,
            text=True,
            timeout=TIMEOUT + 5,
        )
        if result.returncode != 0:
            print(f"[web_fetch] curl failed with code {result.returncode}", file=sys.stderr)
            return None

        content = result.stdout.strip()
        if not content:
            print("[web_fetch] curl returned empty content", file=sys.stderr)
            return None

        # Check for common block indicators
        lower = content.lower()
        block_signals = [
            "403 forbidden", "access denied", "blocked", "captcha",
            "just a moment", "cf_chl_opt", "challenge-platform",
            "enable javascript and cookies to continue",
            "checking your browser", "ddos protection",
        ]
        if any(w in lower for w in block_signals):
            print(f"[web_fetch] blocked by server (Cloudflare/WAF)", file=sys.stderr)
            return None

        return content

    except (subprocess.TimeoutExpired, Exception) as e:
        print(f"[web_fetch] direct fetch error: {e}", file=sys.stderr)
        return None


# ── Layer 1.5: Jina Reader ───────────────────────────────────

JINA_BASE = "https://r.jina.ai/"

def jina_fetch(url: str) -> str | None:
    """Fetch URL via Jina Reader, which renders JS and returns clean markdown.
    Free, no API key required. Works well against Medium, Cloudflare sites."""
    jina_url = JINA_BASE + url
    try:
        result = subprocess.run(
            [
                "curl", "-s", "-L",
                "-H", f"User-Agent: {USER_AGENT}",
                "-H", "Accept: text/plain,text/markdown,*/*;q=0.9",
                "--max-time", str(TIMEOUT + 5),
                jina_url,
            ],
            capture_output=True,
            text=True,
            timeout=TIMEOUT + 10,
        )
        if result.returncode != 0:
            print(f"[web_fetch] Jina curl failed with code {result.returncode}", file=sys.stderr)
            return None

        content = result.stdout.strip()
        if not content:
            print("[web_fetch] Jina returned empty content", file=sys.stderr)
            return None

        lower = content.lower()
        if "error" in lower[:200] or "not found" in lower[:200]:
            print("[web_fetch] Jina returned error response", file=sys.stderr)
            return None

        return content

    except (subprocess.TimeoutExpired, Exception) as e:
        print(f"[web_fetch] Jina fetch error: {e}", file=sys.stderr)
        return None


# ── Layer 2: Tavily Extract API ─────────────────────────────

def tavily_extract(url: str) -> str | None:
    """Use Tavily Extract API to get content from a specific URL."""
    try:
        import requests
    except ImportError:
        print("[web_fetch] requests not installed, cannot use Tavily", file=sys.stderr)
        return None

    try:
        resp = requests.post(
            "https://api.tavily.com/extract",
            json={"urls": [url]},
            headers={
                "Authorization": f"Bearer {TAVILY_API_KEY}",
                "Content-Type": "application/json",
            },
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results", [])
        if results:
            return results[0].get("raw_content") or results[0].get("content", "")
        print("[web_fetch] Tavily extract returned no results", file=sys.stderr)
        return None
    except Exception as e:
        print(f"[web_fetch] Tavily extract error: {e}", file=sys.stderr)
        return None


def tavily_search(query: str, max_results: int = 5) -> str | None:
    """Use Tavily Search API to search for information."""
    try:
        import requests
    except ImportError:
        print("[web_fetch] requests not installed, cannot use Tavily", file=sys.stderr)
        return None

    try:
        resp = requests.post(
            "https://api.tavily.com/search",
            json={
                "query": query,
                "max_results": max_results,
                "include_raw_content": True,
            },
            headers={
                "Authorization": f"Bearer {TAVILY_API_KEY}",
                "Content-Type": "application/json",
            },
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results", [])
        if not results:
            print("[web_fetch] Tavily search returned no results", file=sys.stderr)
            return None

        # Format results as markdown
        lines = []
        for r in results:
            lines.append(f"### [{r.get('title', 'Untitled')}]({r.get('url', '')})")
            lines.append(r.get("content", ""))
            lines.append("")
        return "\n".join(lines)
    except Exception as e:
        print(f"[web_fetch] Tavily search error: {e}", file=sys.stderr)
        return None


# ── Main: fetch with fallback ───────────────────────────────

def fetch_url(url: str, search_query: str | None = None) -> str | None:
    """
    Fetch URL content with fallback strategy:
      1.   Direct curl fetch
      1.5. Jina Reader (JS rendering, bypasses Cloudflare/Medium)
      2.   Tavily Extract API
      3.   Tavily Search API (if search_query provided)
    """
    # Layer 1: direct fetch
    print(f"[web_fetch] Layer 1: direct fetch {url}", file=sys.stderr)
    content = direct_fetch(url)
    if content and len(content) > 500:
        print(f"[web_fetch] Layer 1 success ({len(content)} chars)", file=sys.stderr)
        return content

    # Layer 1.5: Jina Reader
    print(f"[web_fetch] Layer 1.5: Jina Reader {url}", file=sys.stderr)
    content = jina_fetch(url)
    if content and len(content) > 500:
        print(f"[web_fetch] Layer 1.5 success ({len(content)} chars)", file=sys.stderr)
        return content

    # Layer 2: Tavily extract
    print(f"[web_fetch] Layer 2: Tavily extract {url}", file=sys.stderr)
    content = tavily_extract(url)
    if content:
        print(f"[web_fetch] Layer 2 success ({len(content)} chars)", file=sys.stderr)
        return content

    # Layer 3: Tavily search (if query provided)
    if search_query:
        print(f"[web_fetch] Layer 3: Tavily search '{search_query}'", file=sys.stderr)
        content = tavily_search(search_query)
        if content:
            print(f"[web_fetch] Layer 3 success ({len(content)} chars)", file=sys.stderr)
            return content

    print("[web_fetch] All layers failed", file=sys.stderr)
    return None


def main():
    parser = argparse.ArgumentParser(description="Fetch web content with fallback")
    parser.add_argument("url", nargs="?", help="URL to fetch")
    parser.add_argument("--query", "-q", help="Extra search query for Tavily fallback")
    parser.add_argument("--search", "-s", help="Search only (no direct fetch)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if args.search:
        content = tavily_search(args.search)
    elif args.url:
        content = fetch_url(args.url, search_query=args.query)
    else:
        parser.print_help()
        sys.exit(1)

    if content:
        if args.json:
            print(json.dumps({"content": content, "url": args.url or args.search}))
        else:
            print(content)
    else:
        print("[web_fetch] Failed to fetch content", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
