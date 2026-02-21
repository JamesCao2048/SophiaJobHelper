#!/usr/bin/env python3
"""
paper_metadata.py -- 论文 metadata 抓取工具

三步流程：
  1. DBLP 两步法：author search 确认 PID → XML 拿论文列表
  2. OpenAlex：批量拉 title + abstract（无需 API key）
  3. 输出 JSON，供 LLM 选 top 3 相关论文，再决定是否下载 PDF

用法:
  # 1. 查找 DBLP PID（带机构确认，防同名混淆）
  python src/paper_metadata.py find-pid \\
    --name "Burkhard Wuensche" --affil "Auckland"

  # 2. 从 DBLP PID 拉近 N 年论文列表 + DOI
  python src/paper_metadata.py fetch-dblp \\
    --pid "w/WuenscheBurkhard" --years 3

  # 3. 对标题列表批量拉 OpenAlex 摘要
  python src/paper_metadata.py fetch-abstracts \\
    --titles "Title One|Title Two|Title Three" \\
    --output raw/faculty_profiles/wuensche_abstracts.json

  # 一键：find-pid + fetch-dblp + fetch-abstracts（最常用）
  python src/paper_metadata.py all \\
    --name "Burkhard Wuensche" --affil "Auckland" \\
    --years 3 \\
    --output raw/faculty_profiles/wuensche_abstracts.json
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: requests not found. Run: pip install requests", file=sys.stderr)
    sys.exit(1)

try:
    from web_fetch_utils import log
except ImportError:
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    from web_fetch_utils import log

OPENALEX_MAILTO = "sophia-pipeline@example.com"
DBLP_TIMEOUT = 15
OPENALEX_TIMEOUT = 10
OPENALEX_DELAY = 0.6  # seconds between requests

# ---------------------------------------------------------------------------
# DBLP helpers
# ---------------------------------------------------------------------------

def dblp_find_pid(name: str, affil: str) -> str | None:
    """
    DBLP author search，带机构关键词过滤，返回确认 PID 或 None。
    防止同名不同机构的混淆。

    注意：DBLP search API 的 q 参数按词加通配符，affil 关键词不能直接放进 q 里
    （会被当作名字搜索）。正确做法：先按姓名搜，再从返回 metadata 里核查机构。
    """
    url = "https://dblp.org/search/author/api"
    # Search by name only — DBLP doesn't support affiliation filtering via q
    params = {"q": name, "format": "json", "h": 10}
    log(f"DBLP author search: {name!r} (affil check: {affil!r})")
    try:
        resp = requests.get(url, params=params, timeout=DBLP_TIMEOUT)
        data = resp.json()
        hits = data.get("result", {}).get("hits", {}).get("hit", [])
        if not hits:
            log("  ✗ No DBLP results")
            return None

        affil_lower = affil.lower()

        # Pass 1: look for affiliation confirmation in returned metadata
        for hit in hits:
            info = hit.get("info", {})
            pid = info.get("url", "").replace("https://dblp.org/pid/", "").rstrip("/")
            author_name = info.get("author", "")
            notes = json.dumps(info).lower()
            if affil_lower in notes:
                log(f"  ✓ PID confirmed (affil in metadata): {pid} ({author_name})")
                return pid

        # Pass 2: if only one result, trust it with a warning
        if len(hits) == 1:
            info = hits[0].get("info", {})
            pid = info.get("url", "").replace("https://dblp.org/pid/", "").rstrip("/")
            author_name = info.get("author", "")
            log(f"  ⚠ Single result, affil not in metadata; returning: {pid} ({author_name})")
            log(f"    Manually verify at: https://dblp.org/pid/{pid}")
            return pid

        # Pass 3: multiple results, affil unconfirmed — return first with strong warning
        info = hits[0].get("info", {})
        pid = info.get("url", "").replace("https://dblp.org/pid/", "").rstrip("/")
        author_name = info.get("author", "")
        log(f"  ⚠ {len(hits)} results, affil unconfirmed. Returning first: {pid} ({author_name})")
        log(f"    *** SAME-NAME RISK — verify manually: https://dblp.org/pid/{pid} ***")
        return pid

    except Exception as e:
        log(f"  ✗ DBLP author search failed: {e}")
        return None


def dblp_fetch_papers(pid: str, years: int = 3) -> list[dict]:
    """
    从 DBLP PID 拉 XML，提取近 N 年论文（title, year, doi/url）。
    """
    url = f"https://dblp.org/pid/{pid}.xml"
    log(f"DBLP XML: {url}")
    try:
        resp = requests.get(url, timeout=DBLP_TIMEOUT)
        xml = resp.text
    except Exception as e:
        log(f"  ✗ DBLP XML fetch failed: {e}")
        return []

    from xml.etree import ElementTree as ET
    try:
        root = ET.fromstring(xml)
    except ET.ParseError as e:
        log(f"  ✗ XML parse error: {e}")
        return []

    import datetime
    cutoff = datetime.date.today().year - years

    papers = []
    for entry in root.iter():
        if entry.tag not in ("article", "inproceedings", "proceedings", "book", "incollection"):
            continue
        year_el = entry.find("year")
        if year_el is None:
            continue
        try:
            year = int(year_el.text)
        except (ValueError, TypeError):
            continue
        if year < cutoff:
            continue

        title_el = entry.find("title")
        title = "".join(title_el.itertext()).strip() if title_el is not None else ""
        if not title:
            continue

        # DOI / URL from <ee> tags
        doi = ""
        for ee in entry.findall("ee"):
            val = (ee.text or "").strip()
            if "doi.org" in val:
                doi = val
                break
            elif not doi and val.startswith("http"):
                doi = val

        papers.append({"title": title, "year": year, "doi": doi})

    log(f"  ✓ {len(papers)} papers (last {years} years)")
    return papers


# ---------------------------------------------------------------------------
# OpenAlex helpers
# ---------------------------------------------------------------------------

def _reconstruct_abstract(inverted_index: dict | None) -> str:
    """倒排索引 → 正常文本"""
    if not inverted_index:
        return ""
    words: dict[int, str] = {}
    for word, positions in inverted_index.items():
        for pos in positions:
            words[pos] = word
    return " ".join(words[k] for k in sorted(words))


def _sanitize_title_for_search(title: str) -> str:
    """Strip characters that break OpenAlex filter query (colons, commas, quotes, etc.)"""
    # Remove characters that cause HTTP 400 in OpenAlex title.search filter
    cleaned = re.sub(r'[":,\(\)\[\]{}\\]', ' ', title)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    # Truncate to avoid overly long queries
    return cleaned[:120]


def openalex_fetch_abstract(title: str) -> dict | None:
    """
    按标题搜 OpenAlex，返回 {title, abstract, year, venue, oa_url} 或 None。
    """
    url = "https://api.openalex.org/works"
    search_title = _sanitize_title_for_search(title)
    params = {
        "filter": f"title.search:{search_title}",
        "select": "title,abstract_inverted_index,publication_year,primary_location,open_access",
        "per-page": 1,
        "mailto": OPENALEX_MAILTO,
    }
    try:
        resp = requests.get(url, params=params, timeout=OPENALEX_TIMEOUT)
        if resp.status_code == 429:
            log(f"  ⚠ OpenAlex rate limit; waiting 5s")
            time.sleep(5)
            resp = requests.get(url, params=params, timeout=OPENALEX_TIMEOUT)
        if resp.status_code != 200:
            log(f"  ✗ OpenAlex HTTP {resp.status_code} for: {title[:60]}")
            return None

        results = resp.json().get("results", [])
        if not results:
            log(f"  ✗ OpenAlex: no results for: {title[:60]}")
            return None

        p = results[0]
        abstract = _reconstruct_abstract(p.get("abstract_inverted_index"))
        loc = p.get("primary_location") or {}
        venue = (loc.get("source") or {}).get("display_name", "")
        oa_url = (p.get("open_access") or {}).get("oa_url", "")

        return {
            "title": p.get("title", title),
            "year": p.get("publication_year"),
            "venue": venue,
            "abstract": abstract,
            "oa_url": oa_url,
        }
    except Exception as e:
        log(f"  ✗ OpenAlex error for {title[:60]}: {e}")
        return None


def fetch_abstracts_batch(papers: list[dict]) -> list[dict]:
    """
    对论文列表批量拉 OpenAlex 摘要，合并回原 dict。
    """
    results = []
    for i, paper in enumerate(papers):
        title = paper.get("title", "")
        log(f"OpenAlex [{i+1}/{len(papers)}]: {title[:60]}")
        meta = openalex_fetch_abstract(title)
        merged = {**paper}
        if meta:
            merged["abstract"] = meta.get("abstract", "")
            merged["venue"] = merged.get("venue") or meta.get("venue", "")
            if meta.get("oa_url"):
                merged["oa_url"] = meta["oa_url"]
            log(f"  ✓ abstract={len(merged['abstract'])} chars")
        else:
            merged["abstract"] = ""
        results.append(merged)
        if i < len(papers) - 1:
            time.sleep(OPENALEX_DELAY)
    return results


# ---------------------------------------------------------------------------
# CLI subcommands
# ---------------------------------------------------------------------------

def cmd_find_pid(args):
    pid = dblp_find_pid(args.name, args.affil)
    if pid:
        print(pid)
    else:
        sys.exit(1)


def cmd_fetch_dblp(args):
    papers = dblp_fetch_papers(args.pid, args.years)
    print(json.dumps(papers, ensure_ascii=False, indent=2))


def cmd_fetch_abstracts(args):
    titles = [t.strip() for t in args.titles.split("|") if t.strip()]
    papers = [{"title": t} for t in titles]
    results = fetch_abstracts_batch(papers)
    out = json.dumps(results, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(out, encoding="utf-8")
        log(f"Saved to {args.output}")
    else:
        print(out)


def cmd_all(args):
    """一键：find-pid → fetch-dblp → fetch-abstracts → 输出 JSON"""
    # Step 1: Find PID
    pid = dblp_find_pid(args.name, args.affil)
    if not pid:
        log("DBLP PID not found; will use WebSearch fallback (manual step required)")
        papers = []
    else:
        # Step 2: Fetch papers from DBLP
        papers = dblp_fetch_papers(pid, args.years)

    if not papers:
        log("No papers from DBLP. Add titles manually via --titles if needed.")
        result = {"pid": pid, "papers": []}
    else:
        # Step 3: Fetch abstracts from OpenAlex
        log(f"\nFetching abstracts for {len(papers)} papers via OpenAlex...")
        papers_with_abstracts = fetch_abstracts_batch(papers)
        result = {"pid": pid, "papers": papers_with_abstracts}

    out = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(out, encoding="utf-8")
        log(f"\nSaved to {args.output}")
    else:
        print(out)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Paper metadata fetcher (DBLP + OpenAlex)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # find-pid
    p1 = sub.add_parser("find-pid", help="DBLP author search → PID")
    p1.add_argument("--name", required=True, help='Full name, e.g. "Burkhard Wuensche"')
    p1.add_argument("--affil", required=True, help='Affiliation keyword, e.g. "Auckland"')
    p1.set_defaults(func=cmd_find_pid)

    # fetch-dblp
    p2 = sub.add_parser("fetch-dblp", help="Fetch papers from DBLP XML by PID")
    p2.add_argument("--pid", required=True, help='DBLP PID, e.g. "w/WuenscheBurkhard"')
    p2.add_argument("--years", type=int, default=3, help="How many recent years (default: 3)")
    p2.set_defaults(func=cmd_fetch_dblp)

    # fetch-abstracts
    p3 = sub.add_parser("fetch-abstracts", help="OpenAlex batch abstract fetch by titles")
    p3.add_argument("--titles", required=True, help="Pipe-separated list of paper titles")
    p3.add_argument("--output", help="Output JSON file path")
    p3.set_defaults(func=cmd_fetch_abstracts)

    # all-in-one
    p4 = sub.add_parser("all", help="find-pid + fetch-dblp + fetch-abstracts in one shot")
    p4.add_argument("--name", required=True, help='Full name')
    p4.add_argument("--affil", required=True, help='Affiliation keyword')
    p4.add_argument("--years", type=int, default=3, help="Recent years (default: 3)")
    p4.add_argument("--output", help="Output JSON file path")
    p4.set_defaults(func=cmd_all)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
