#!/usr/bin/env python3
"""
page_scraper.py -- Step 1: Research

使用 Jina Reader API 将院系页面和职位 JD 页面转成 markdown，供 Claude Code 分析。
Python 只负责数据获取，分析和结构化由 Claude Code 完成。

用法:
  # 爬取院系 faculty 列表页
  python page_scraper.py --school "Monash University" --url "https://www.monash.edu/it/about-us/schools/dsai/people"

  # 爬取职位 JD
  python page_scraper.py --url "https://careers.pageuppeople.com/..." --output-type raw

  # 指定输出目录（默认: overseas_pipeline/output/{school_id}/raw/）
  python page_scraper.py --school "Monash University" --url "..." --output-dir /path/to/dir
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

try:
    from web_fetch_utils import fetch_with_fallback, log
except ImportError:
    # Allow running from project root too
    import sys, os
    sys.path.insert(0, os.path.dirname(__file__))
    from web_fetch_utils import fetch_with_fallback, log

# 从本文件位置推断项目根目录
SCRIPT_DIR = Path(__file__).parent
OUTPUT_BASE = SCRIPT_DIR.parent / "output"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def school_to_id(school_name: str) -> str:
    """将学校名转换为 snake_case ID，如 'Monash University' -> 'monash_university'"""
    s = school_name.lower().strip()
    s = re.sub(r"[^a-z0-9\s]", "", s)
    s = re.sub(r"\s+", "_", s)
    return s


def save_content(content: str, output_path: Path, url: str, method: str):
    """保存内容到文件，并创建 sources 记录"""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    # 同时写一个 meta 文件记录来源
    meta_path = output_path.with_suffix(".meta.json")
    meta = {
        "source_url": url,
        "fetch_method": method,
        "fetch_date": datetime.now().strftime("%Y-%m-%d"),
        "char_count": len(content),
    }
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    log(f"  → Saved to: {output_path}")
    log(f"  → Meta: {meta_path}")


# ---------------------------------------------------------------------------
# Main scraping logic
# ---------------------------------------------------------------------------

def scrape_page(url: str, output_path: Path) -> bool:
    """
    爬取单个页面，五层 fallback。成功返回 True，失败返回 False。
    """
    content, method = fetch_with_fallback(url)
    if content is None:
        log(f"  ✗ All layers failed for: {url}")
        return False
    save_content(content, output_path, url, method)
    return True


def scrape_faculty_page(school_name: str, url: str, output_dir: Path) -> dict:
    """
    爬取院系 faculty 主页面（以及可能的子页面）。
    返回爬取结果摘要。
    """
    school_id = school_to_id(school_name)
    raw_dir = output_dir / school_id / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    log(f"=== Step 1: Research -- {school_name} ===")
    log(f"School ID: {school_id}")
    log(f"Target URL: {url}")
    log(f"Output dir: {raw_dir}")

    results = {
        "school": school_name,
        "school_id": school_id,
        "urls_scraped": [],
        "urls_failed": [],
        "output_dir": str(raw_dir),
        "scrape_date": datetime.now().strftime("%Y-%m-%d"),
    }

    # 主页面
    main_filename = "faculty_page.md"
    main_path = raw_dir / main_filename
    success = scrape_page(url, main_path)

    if success:
        results["urls_scraped"].append(url)
    else:
        results["urls_failed"].append(url)

    # 写摘要
    summary_path = output_dir / school_id / "scrape_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    return results


def scrape_raw(url: str, output_dir: Path) -> bool:
    """
    爬取任意 URL（用于 JD 等），保存为原始内容。
    """
    log(f"=== Fetching raw content ===")
    log(f"URL: {url}")

    # 从 URL 生成文件名
    parsed = urlparse(url)
    filename = re.sub(r"[^a-z0-9]", "_", parsed.path.lower()).strip("_")[:50]
    if not filename:
        filename = "page"
    output_path = output_dir / f"{filename}.md"

    return scrape_page(url, output_path)


# ---------------------------------------------------------------------------
# Additional scraping for individual faculty homepages
# ---------------------------------------------------------------------------

def scrape_faculty_profiles(school_id: str, faculty_urls: list[str], output_dir: Path):
    """
    爬取单个 faculty 的主页（用于获取更详细的研究信息）。
    在 Claude Code 分析主页面后，如果需要更多信息时调用。
    """
    profiles_dir = output_dir / school_id / "raw" / "profiles"
    profiles_dir.mkdir(parents=True, exist_ok=True)

    for url in faculty_urls:
        parsed = urlparse(url)
        name_slug = re.sub(r"[^a-z0-9]", "_", parsed.path.lower()).strip("_")[-30:]
        output_path = profiles_dir / f"{name_slug}.md"

        if output_path.exists():
            log(f"  → Already scraped: {output_path.name}")
            continue

        success = scrape_page(url, output_path)
        if not success:
            log(f"  ✗ Failed to scrape: {url}")

        time.sleep(1)  # polite delay


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="page_scraper.py -- Overseas Pipeline Step 1: Research\n"
                    "使用 Jina Reader API 将院系页面和 JD 页面转为 markdown，供 Claude Code 分析。",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("--url", required=True, help="要爬取的页面 URL（院系 faculty 页面或职位 JD URL）")
    parser.add_argument("--school", help="学校名（如 'Monash University'）；--output-type=raw 时可省略")
    parser.add_argument(
        "--output-type",
        choices=["faculty", "raw"],
        default="faculty",
        help="输出类型：faculty（完整 Step 1 流程）或 raw（仅爬取内容，不创建学校目录）"
    )
    parser.add_argument(
        "--output-dir",
        default=str(OUTPUT_BASE),
        help=f"输出根目录（默认: {OUTPUT_BASE}）"
    )
    parser.add_argument(
        "--faculty-profiles",
        nargs="*",
        help="额外爬取的 faculty 主页 URL 列表（用空格分隔）"
    )

    args = parser.parse_args()
    output_dir = Path(args.output_dir)

    if args.output_type == "faculty":
        if not args.school:
            parser.error("--school 参数在 --output-type=faculty 时必须提供")

        results = scrape_faculty_page(args.school, args.url, output_dir)

        print("\n" + "=" * 60)
        print("爬取完成！")
        print(f"  学校: {results['school']} ({results['school_id']})")
        print(f"  成功: {len(results['urls_scraped'])} 页")
        print(f"  失败: {len(results['urls_failed'])} 页")
        print(f"  输出: {results['output_dir']}")
        print()
        print("下一步：在 Claude Code 中运行命令：")
        print(f"  '分析 {results['school']}'")
        print("  Claude Code 会读取爬取的 markdown，提取 faculty 信息，判断 overlap，")
        print("  生成 faculty_data.json 和 fit_report.md")

        if results["urls_failed"]:
            print("\n⚠ 以下 URL 爬取失败，请手动 copy-paste 内容：")
            for url in results["urls_failed"]:
                print(f"  - {url}")

        # 如果提供了 faculty profile URL，也一并爬取
        if args.faculty_profiles and results.get("school_id"):
            log("\n开始爬取 faculty 主页...")
            scrape_faculty_profiles(results["school_id"], args.faculty_profiles, output_dir)

    elif args.output_type == "raw":
        raw_dir = output_dir / "raw_pages"
        success = scrape_raw(args.url, raw_dir)
        if success:
            print(f"\n✓ 内容已保存到: {raw_dir}")
        else:
            print(f"\n✗ 爬取失败: {args.url}")
            print("请手动访问此 URL 并将内容粘贴给 Claude Code。")
            sys.exit(1)


if __name__ == "__main__":
    main()
