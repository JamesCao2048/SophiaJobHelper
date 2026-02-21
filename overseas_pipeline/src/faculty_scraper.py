#!/usr/bin/env python3
"""
faculty_scraper.py -- 教授个人信息抓取 & 论文下载

针对 faculty_data.json 中的教授列表，批量抓取个人主页、Google Scholar、DBLP，
以及按需下载论文 PDF。Python 负责数据获取，研究背景分类（major/minor）由 LLM 完成。

用法:
  # 批量抓取教授个人信息（主页 + Scholar + DBLP）
  python faculty_scraper.py profiles \
    --input output/{school_id}/{dept_id}/faculty_data.json \
    --output-dir output/{school_id}/{dept_id}/raw/faculty_profiles/

  # 下载单篇论文 PDF
  python faculty_scraper.py download-paper \
    --url "https://arxiv.org/pdf/2401.12345" \
    --output output/{school_id}/{dept_id}/papers/Smith_2024_title.pdf

  # 批量下载论文（从 JSON manifest）
  python faculty_scraper.py download-papers \
    --manifest papers_to_download.json \
    --output-dir output/{school_id}/{dept_id}/papers/
"""

import argparse
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse, quote_plus

try:
    import requests
except ImportError:
    print("ERROR: requests library not found. Please run: pip install requests", file=sys.stderr)
    sys.exit(1)

try:
    from web_fetch_utils import fetch_with_fallback, log, BROWSER_HEADERS
except ImportError:
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    from web_fetch_utils import fetch_with_fallback, log, BROWSER_HEADERS

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PAPER_DOWNLOAD_TIMEOUT = 60
POLITE_DELAY = 1.5  # seconds between requests


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def slugify(name: str, max_len: int = 40) -> str:
    """Convert a name to a filesystem-safe slug."""
    s = name.lower().strip()
    s = re.sub(r"[^a-z0-9\s]", "", s)
    s = re.sub(r"\s+", "_", s)
    return s[:max_len]


def extract_lastname(full_name: str) -> str:
    """Extract last name from full name for file naming."""
    parts = full_name.strip().split()
    titles = {"prof.", "professor", "dr.", "dr", "associate", "assistant"}
    clean_parts = [p for p in parts if p.lower().rstrip(".") not in titles]
    return clean_parts[-1] if clean_parts else parts[-1]


def save_content(content: str, output_path: Path, url: str, method: str):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    meta_path = output_path.with_suffix(".meta.json")
    meta = {
        "source_url": url,
        "fetch_method": method,
        "fetch_date": datetime.now().strftime("%Y-%m-%d"),
        "char_count": len(content),
    }
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Profile scraping
# ---------------------------------------------------------------------------

def build_scholar_url(scholar_link: str) -> str | None:
    """Extract or build a Google Scholar profile URL."""
    if not scholar_link:
        return None
    if "scholar.google" in scholar_link:
        return scholar_link
    return None


def build_dblp_search_url(name: str) -> str:
    """Build a DBLP author search URL."""
    return f"https://dblp.org/search?q={quote_plus(name)}"


def scrape_single_profile(faculty: dict, output_dir: Path) -> dict:
    """
    Scrape all available pages for a single faculty member.
    Returns a result dict with status for each source.
    """
    name = faculty.get("name", "Unknown")
    lastname = extract_lastname(name)
    slug = slugify(lastname)

    result = {
        "name": name,
        "homepage": {"status": "skipped", "path": None},
        "scholar": {"status": "skipped", "path": None},
        "dblp": {"status": "skipped", "path": None},
    }

    # 1. Homepage
    homepage = faculty.get("homepage")
    if homepage:
        out_path = output_dir / f"{slug}_homepage.md"
        if out_path.exists():
            log(f"  [{name}] homepage: already exists, skipping")
            result["homepage"] = {"status": "cached", "path": str(out_path)}
        else:
            content, method = fetch_with_fallback(homepage)
            if content:
                save_content(content, out_path, homepage, method)
                log(f"  [{name}] homepage: ✓ ({method}, {len(content)} chars)")
                result["homepage"] = {"status": "ok", "path": str(out_path), "method": method}
            else:
                log(f"  [{name}] homepage: ✗ ({method})")
                result["homepage"] = {"status": "failed", "method": method, "url": homepage}
            time.sleep(POLITE_DELAY)

    # 2. Google Scholar
    scholar_url = build_scholar_url(faculty.get("google_scholar", ""))
    if scholar_url:
        # Append sortby=pubdate to get recent publications
        sep = "&" if "?" in scholar_url else "?"
        recent_url = f"{scholar_url}{sep}sortby=pubdate&view_op=list_works&pagesize=20"
        out_path = output_dir / f"{slug}_scholar.md"
        if out_path.exists():
            log(f"  [{name}] scholar: already exists, skipping")
            result["scholar"] = {"status": "cached", "path": str(out_path)}
        else:
            content, method = fetch_with_fallback(recent_url)
            if content:
                save_content(content, out_path, recent_url, method)
                log(f"  [{name}] scholar: ✓ ({method}, {len(content)} chars)")
                result["scholar"] = {"status": "ok", "path": str(out_path), "method": method}
            else:
                log(f"  [{name}] scholar: ✗ ({method})")
                result["scholar"] = {"status": "failed", "method": method, "url": recent_url}
            time.sleep(POLITE_DELAY)

    # 3. DBLP
    dblp_url = build_dblp_search_url(name)
    out_path = output_dir / f"{slug}_dblp.md"
    if out_path.exists():
        log(f"  [{name}] dblp: already exists, skipping")
        result["dblp"] = {"status": "cached", "path": str(out_path)}
    else:
        content, method = fetch_with_fallback(dblp_url)
        if content:
            save_content(content, out_path, dblp_url, method)
            log(f"  [{name}] dblp: ✓ ({method}, {len(content)} chars)")
            result["dblp"] = {"status": "ok", "path": str(out_path), "method": method}
        else:
            log(f"  [{name}] dblp: ✗ ({method})")
            result["dblp"] = {"status": "failed", "method": method, "url": dblp_url}
        time.sleep(POLITE_DELAY)

    return result


def cmd_profiles(args):
    """Batch scrape faculty profiles from faculty_data.json."""
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: {input_path} not found", file=sys.stderr)
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    faculty_list = data.get("faculty", [])
    if not faculty_list:
        print("WARNING: No faculty entries found in JSON", file=sys.stderr)
        sys.exit(0)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    log(f"=== Faculty Profile Scraping ===")
    log(f"Input: {input_path}")
    log(f"Faculty count: {len(faculty_list)}")
    log(f"Output dir: {output_dir}")

    results = []
    stats = {"ok": 0, "failed": 0, "cached": 0, "skipped": 0}

    for i, faculty in enumerate(faculty_list):
        name = faculty.get("name", f"Unknown_{i}")
        log(f"\n[{i+1}/{len(faculty_list)}] {name}")
        result = scrape_single_profile(faculty, output_dir)
        results.append(result)

        for source in ["homepage", "scholar", "dblp"]:
            status = result[source]["status"]
            if status in stats:
                stats[status] += 1

    # Write summary
    summary_path = output_dir / "_scrape_summary.json"
    summary = {
        "scrape_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "input_file": str(input_path),
        "faculty_count": len(faculty_list),
        "stats": stats,
        "results": results,
    }
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    # Print summary
    print(f"\n{'='*60}")
    print(f"Profile scraping complete!")
    print(f"  OK: {stats['ok']}  |  Cached: {stats['cached']}  |  Failed: {stats['failed']}  |  Skipped: {stats['skipped']}")
    print(f"  Summary: {summary_path}")

    # Report failures for web-fetch-fallback skill
    failed_urls = []
    for r in results:
        for source in ["homepage", "scholar", "dblp"]:
            if r[source]["status"] == "failed" and "url" in r[source]:
                failed_urls.append({"name": r["name"], "source": source, "url": r[source]["url"]})

    if failed_urls:
        print(f"\n⚠ {len(failed_urls)} URLs failed (use web-fetch-fallback skill for these):")
        for item in failed_urls:
            print(f"  - [{item['name']}] {item['source']}: {item['url']}")


# ---------------------------------------------------------------------------
# Paper downloading
# ---------------------------------------------------------------------------

def download_single_paper(url: str, output_path: Path) -> bool:
    """Download a single paper PDF."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists():
        log(f"  Already exists: {output_path.name}")
        return True

    # Try direct download first (most paper sources support this)
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        resp = requests.get(url, headers=headers, timeout=PAPER_DOWNLOAD_TIMEOUT, stream=True)
        resp.raise_for_status()

        # Check content type
        content_type = resp.headers.get("Content-Type", "")
        if "pdf" in content_type or url.endswith(".pdf"):
            with open(output_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            size_kb = output_path.stat().st_size / 1024
            log(f"  ✓ Downloaded: {output_path.name} ({size_kb:.0f} KB)")
            return True
        else:
            # Might be HTML redirect (e.g., ACM paywall)
            log(f"  ✗ Not a PDF (Content-Type: {content_type})")
            return False

    except requests.exceptions.RequestException as e:
        log(f"  ✗ Download failed: {e}")
        return False


def cmd_download_paper(args):
    """Download a single paper PDF."""
    output_path = Path(args.output)
    log(f"=== Download Paper ===")
    log(f"URL: {args.url}")
    log(f"Output: {output_path}")

    success = download_single_paper(args.url, output_path)
    if not success:
        print(f"\n✗ Failed to download. Try manually or use web-fetch-fallback skill.", file=sys.stderr)
        sys.exit(1)


def cmd_download_papers(args):
    """Batch download papers from a JSON manifest.

    Manifest format:
    [
      {"url": "https://arxiv.org/pdf/...", "filename": "Smith_2024_title.pdf"},
      ...
    ]
    """
    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"ERROR: {manifest_path} not found", file=sys.stderr)
        sys.exit(1)

    with open(manifest_path, "r", encoding="utf-8") as f:
        papers = json.load(f)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    log(f"=== Batch Paper Download ===")
    log(f"Manifest: {manifest_path}")
    log(f"Papers: {len(papers)}")
    log(f"Output dir: {output_dir}")

    ok, failed = 0, 0
    failed_list = []

    for i, paper in enumerate(papers):
        url = paper["url"]
        filename = paper.get("filename", f"paper_{i}.pdf")
        output_path = output_dir / filename

        log(f"\n[{i+1}/{len(papers)}] {filename}")
        success = download_single_paper(url, output_path)
        if success:
            ok += 1
        else:
            failed += 1
            failed_list.append({"url": url, "filename": filename})
        time.sleep(POLITE_DELAY)

    print(f"\n{'='*60}")
    print(f"Download complete: {ok} ok, {failed} failed")
    if failed_list:
        print(f"\n⚠ Failed downloads:")
        for item in failed_list:
            print(f"  - {item['filename']}: {item['url']}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="faculty_scraper.py -- 教授个人信息抓取 & 论文下载",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # profiles
    p_profiles = subparsers.add_parser(
        "profiles",
        help="Batch scrape faculty profiles (homepage + Scholar + DBLP)",
    )
    p_profiles.add_argument("--input", required=True, help="Path to faculty_data.json")
    p_profiles.add_argument("--output-dir", required=True, help="Output directory for profile markdown files")

    # download-paper
    p_single = subparsers.add_parser(
        "download-paper",
        help="Download a single paper PDF",
    )
    p_single.add_argument("--url", required=True, help="Paper PDF URL")
    p_single.add_argument("--output", required=True, help="Output file path")

    # download-papers
    p_batch = subparsers.add_parser(
        "download-papers",
        help="Batch download papers from a JSON manifest",
    )
    p_batch.add_argument("--manifest", required=True, help="JSON manifest file path")
    p_batch.add_argument("--output-dir", required=True, help="Output directory for paper PDFs")

    args = parser.parse_args()

    if args.command == "profiles":
        cmd_profiles(args)
    elif args.command == "download-paper":
        cmd_download_paper(args)
    elif args.command == "download-papers":
        cmd_download_papers(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
