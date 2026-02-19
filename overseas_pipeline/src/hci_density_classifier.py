#!/usr/bin/env python3
"""
hci_density_classifier.py -- Step 1 辅助：HCI 密度自动分类

从 faculty_data.json 中读取 faculty 列表，
按 research_interests 匹配 HCI 关键词，
推断双层密度分类（target_dept + faculty_wide），
写回 faculty_data.json 的 hci_density 字段。

用法:
  python hci_density_classifier.py --input output/monash_university/dsai/faculty_data.json
  python hci_density_classifier.py --input output/monash_university/dsai/faculty_data.json --target-dept "DSAI"
  python hci_density_classifier.py --input output/monash_university/dsai/faculty_data.json --dry-run
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# HCI 相关关键词（不区分大小写）
HCI_KEYWORDS = [
    "hci", "human-computer interaction", "human computer interaction",
    "cscw", "computer-supported cooperative work",
    "human-ai interaction", "human ai interaction",
    "ux", "user experience", "user interface", "ui design",
    "accessibility", "inclusive design", "assistive technology",
    "interaction design", "interaction technique",
    "user study", "user research", "usability",
    "participatory design", "co-design",
    "information visualization", "visual analytics",
    "social computing", "computer-mediated communication",
    "augmented reality", "virtual reality", "mixed reality",
    "wearable computing", "ubiquitous computing", "ubicomp",
    "tangible computing", "tangible interface",
    "human factors", "ergonomics",
    "design research", "design thinking",
    "human-centered", "human centered", "people-centered",
    "end-user", "end user computing",
    "conversational agent", "conversational interface",
    "intelligent user interface",
    "explainability", "interpretability",
]

STRATEGY_MATRIX = {
    ("none", "none"):  "pure_pioneer",
    ("none", "few"):   "pioneer_with_few_allies",
    ("none", "many"):  "pioneer_with_allies",
    ("few",  "none"):  "builder",
    ("few",  "few"):   "builder",
    ("few",  "many"):  "builder_in_rich_ecosystem",
    ("many", "none"):  "specialist",
    ("many", "few"):   "specialist",
    ("many", "many"):  "specialist",
}


def count_to_level(count: int) -> str:
    if count == 0:
        return "none"
    elif count <= 3:
        return "few"
    else:
        return "many"


def is_hci_researcher(faculty: dict, keywords: list) -> bool:
    interests = " ".join(faculty.get("research_interests", [])).lower()
    return any(kw.lower() in interests for kw in keywords)


def classify(faculty_data: dict, target_dept_name: str | None, keywords: list) -> dict:
    all_faculty = faculty_data.get("faculty", [])
    default_dept = faculty_data.get("department", "")
    target_dept = target_dept_name or default_dept

    target_hci = []
    wide_hci = []

    for f in all_faculty:
        if not is_hci_researcher(f, keywords):
            continue
        dept = f.get("department", default_dept)
        # 简单字符串包含匹配（宽松）
        if target_dept.lower() in dept.lower() or dept.lower() in target_dept.lower():
            target_hci.append(f["name"])
        else:
            wide_hci.append(f["name"])

    target_level = count_to_level(len(target_hci))
    wide_level = count_to_level(len(wide_hci))

    strategy = STRATEGY_MATRIX.get(
        (target_level, wide_level),
        "builder"  # fallback
    )

    return {
        "target_dept": {
            "level": target_level,
            "count": len(target_hci),
            "hci_members": target_hci,
            "note": f"[auto] {len(target_hci)} HCI researchers in {target_dept}",
        },
        "faculty_wide": {
            "level": wide_level,
            "count": len(wide_hci),
            "hci_members": wide_hci,
            "note": f"[auto] {len(wide_hci)} HCI researchers in other departments",
        },
        "strategy": strategy,
        "strategy_rationale": "",  # agent 后续补充
        "classified_at": datetime.now().strftime("%Y-%m-%d"),
        "keywords_used": len(keywords),
    }


def main():
    parser = argparse.ArgumentParser(description="HCI density classifier for faculty_data.json")
    parser.add_argument("--input", required=True, help="Path to faculty_data.json")
    parser.add_argument("--target-dept", help="Target department name (overrides faculty_data.department)")
    parser.add_argument("--dry-run", action="store_true", help="Print result without writing")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: {input_path} not found", file=sys.stderr)
        sys.exit(1)

    with open(input_path, encoding="utf-8") as f:
        faculty_data = json.load(f)

    result = classify(faculty_data, args.target_dept, HCI_KEYWORDS)

    print("\n=== HCI Density Classification ===")
    print(f"Target dept:  {result['target_dept']['level']} ({result['target_dept']['count']} people)")
    if result['target_dept']['hci_members']:
        print(f"  Members: {', '.join(result['target_dept']['hci_members'])}")
    print(f"Faculty wide: {result['faculty_wide']['level']} ({result['faculty_wide']['count']} people)")
    if result['faculty_wide']['hci_members']:
        print(f"  Members: {', '.join(result['faculty_wide']['hci_members'])}")
    print(f"Strategy:     {result['strategy']}")

    if args.dry_run:
        print("\n[dry-run] Not writing to file.")
        return

    faculty_data["hci_density"] = result

    with open(input_path, "w", encoding="utf-8") as f:
        json.dump(faculty_data, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Written to {input_path}")


if __name__ == "__main__":
    main()
