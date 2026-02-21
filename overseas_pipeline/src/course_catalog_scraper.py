#!/usr/bin/env python3
"""
course_catalog_scraper.py -- Step 1 辅助：课程体系抓取

抓取目标院系课程页面，提取课程列表，
写入 faculty_data.json 的 department_courses 字段。

五层 fallback 策略：
  Layer 1:   curl + browser UA
  Layer 1.5: Jina Reader (https://r.jina.ai/)
  Layer 2:   Tavily Extract API
  Layer 2.5: Wayback Machine
  Layer 3:   Tavily Search API

用法:
  python course_catalog_scraper.py \
    --url "https://www.monash.edu/it/dsai/courses" \
    --output overseas_pipeline/output/monash_university/faculty_data.json

  python course_catalog_scraper.py \
    --url "https://www.monash.edu/it/dsai/courses" \
    --dry-run
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    from web_fetch_utils import fetch_with_fallback, log
except ImportError:
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    from web_fetch_utils import fetch_with_fallback, log

HCI_COURSE_KEYWORDS = [
    "hci", "human-computer", "interaction design", "user experience",
    "ux", "usability", "accessibility", "human factors",
    "interface", "user interface", "human-ai", "conversational",
    "visualization", "information design", "human centered",
]


def is_hci_course(name: str) -> bool:
    low = name.lower()
    return any(kw in low for kw in HCI_COURSE_KEYWORDS)


def extract_courses_heuristic(text: str) -> list[dict]:
    """
    启发式提取课程编号 + 名称。
    Agent 会在此基础上审查和补充。
    """
    courses = []
    # 常见课程编号格式：FIT5145, CS101, COMP3702, INFO4112 等
    pattern = re.compile(
        r"\b([A-Z]{2,6}\s*\d{3,5}[A-Z]?)\s*[:\-\u2013]?\s*([^\n\r,;]{10,80})",
        re.MULTILINE,
    )
    for match in pattern.finditer(text):
        code = match.group(1).strip().replace(" ", "")
        name = match.group(2).strip().rstrip(".,;")
        if len(name) < 5:
            continue
        digits = re.search(r"\d+", code)
        level = "unknown"
        if digits:
            n = int(digits.group())
            if n >= 5000:
                level = "postgrad"
            elif n >= 3000:
                level = "undergrad_advanced"
            else:
                level = "undergrad"

        courses.append({
            "code": code,
            "name": name,
            "level": level,
            "hci_relevant": is_hci_course(name),
        })

    # 去重（按 code）
    seen: set[str] = set()
    unique = []
    for c in courses:
        if c["code"] not in seen:
            seen.add(c["code"])
            unique.append(c)

    return unique


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Course catalog scraper with five-layer fallback"
    )
    parser.add_argument("--url", required=True, help="Course catalog URL")
    parser.add_argument("--output", help="Path to faculty_data.json to update")
    parser.add_argument("--school", default="", help="School name (for search fallback)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    content, layer = fetch_with_fallback(args.url, args.school)

    if not content:
        print(
            "ERROR: All five layers failed. Manual paste required.", file=sys.stderr
        )
        sys.exit(1)

    courses = extract_courses_heuristic(content)
    hci_count = sum(1 for c in courses if c["hci_relevant"])
    log(f"Extracted {len(courses)} courses ({hci_count} HCI-relevant), via {layer}")

    result = {
        "department_courses": courses,
        "course_catalog_url": args.url,
        "course_catalog_scrape_date": datetime.now().strftime("%Y-%m-%d"),
        "course_fetch_layer": layer,
        "course_count": len(courses),
    }

    print("\n=== Course Catalog ===")
    for c in courses[:10]:
        tag = "🔵" if c["hci_relevant"] else "  "
        print(f"  {tag} [{c['level']}] {c['code']}: {c['name']}")
    if len(courses) > 10:
        print(f"  ... and {len(courses) - 10} more")
    print(f"\nLayer used: {layer}")

    if args.dry_run:
        print("\n[dry-run] Not writing.")
        return

    if not args.output:
        print("WARNING: --output not specified. Printing JSON only.")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    output_path = Path(args.output)

    # 保存原始内容到 raw/ 目录，供 agent 在正则提取为空时直接分析
    raw_dir = output_path.parent / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    raw_path = raw_dir / "course_catalog_raw.md"
    with open(raw_path, "w", encoding="utf-8") as f:
        f.write(f"<!-- source: {args.url} | layer: {layer} | date: {datetime.now().strftime('%Y-%m-%d')} -->\n\n")
        f.write(content)
    log(f"Raw content saved to {raw_path} ({len(content)} chars)")

    if output_path.exists():
        with open(output_path, encoding="utf-8") as f:
            faculty_data = json.load(f)
    else:
        faculty_data = {}

    faculty_data.update(result)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(faculty_data, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Written to {output_path}")
    if len(courses) == 0:
        print(f"⚠ 课程提取为空（{layer} 内容已保存到 {raw_path}）")
        print("  Agent 应在 Step 1 step 10 审查中直接读取 raw 文件识别课程")


if __name__ == "__main__":
    main()
