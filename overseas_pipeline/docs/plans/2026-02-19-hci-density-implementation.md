# HCI Density Strategy Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 将 HCI 研究者密度维度融入 overseas_pipeline 的 Step 1/2/3，实现自动分类、课程抓取、策略驱动材料生成。

**Architecture:** 新增独立策略文件（被 agent 读取）+ 两个 Python 脚本（code 做确定性工作）+ 更新 CLAUDE.md 流程指令。agent 和 code 分工：code 负责关键词匹配/计数/结构化，agent 负责边界判断/策略叙事/材料生成。

**Tech Stack:** Python 3.10+（标准库 + requests）、JSON、Markdown、Bash（curl + Tavily API）

**Design Doc:** `docs/plans/2026-02-19-hci-density-strategy-design.md`

---

## Task 1: 创建 HCI 密度策略文件

**Files:**
- Create: `overseas_pipeline/strategies/hci_density_strategy.md`

**Step 1: 创建目录**
```bash
mkdir -p overseas_pipeline/strategies
```

**Step 2: 写入策略文件**

内容如下（完整写入）：

```markdown
# HCI 密度策略指南

本文件被 Step 2（分析）和 Step 3（材料生成）读取，根据目标院系 HCI 研究者密度指导申请材料的修辞策略。

## 一、密度等级定义

| level | 人数 | 含义 |
|:------|:-----|:-----|
| `none` | 0 | 无 HCI 研究者 |
| `few` | 1–3 | 小规模 HCI 集群 |
| `many` | >3 | 成熟 HCI 团队 |

## 二、组合策略矩阵

双层分类（目标系 × 学院）决定策略标签：

| 目标系 \ 学院 | **none** | **few** | **many** |
|:-------------|:---------|:--------|:---------|
| **none** | `pure_pioneer` | `pioneer_with_few_allies` | `pioneer_with_allies` |
| **few** | 罕见 | `builder` | `builder_in_rich_ecosystem` |
| **many** | — | — | `specialist` |

## 三、各策略详细指南

### pure_pioneer（target=none, faculty=none）

**人设：** 开拓者。院系所有评委都是非 HCI 人士。

#### Cover Letter
- 全面技术伪装：避免 "HCI"、"用户体验" 等感性词汇
  - ✅ "human-in-the-loop computing" / "interactive systems architecture"
  - ❌ "UX research" / "design thinking"
- 论证 HCI 对院系的**增量价值**：可申请社科/医学基金（传统 CS 难触及）
- 点名目标系内有研究交集的教授（即使非 HCI 方向）

#### Research Statement
- "硬化"处理：系统架构图 > 用户引语；强调算法/模型/系统贡献
- 加入"方法论严谨性"段落，解释用户研究的科学性
- 强调量化指标（准确率、效率提升等）

#### Teaching Statement
- **必须**列 CS 核心课（数据结构、软工、算法、离散数学等）
- 从目标系 course catalog 中选出 Sophia 能教的具体课程（列课程编号和名称）
- HCI 课程作为"可开设的新课"而非主打

#### 经费叙事
- "我的加入将为院系打开新的经费渠道（NSF SBE / ARC 社会科学板块 / 医学基金）"

---

### pioneer_with_few_allies（target=none, faculty=few）

**人设：** 开拓者 + 少量盟友。学院有 1–3 位 HCI 教授，可作为合作叙事的锚点。

#### Cover Letter
- 技术硬核基调打底（同 pure_pioneer）
- 用一段补充跨系合作：点名已有 HCI 教授，说明互补性
- 注意：盟友少，不能过度依赖跨系叙事

#### Research Statement / Teaching Statement
- 同 pure_pioneer，但可在未来计划中提及与已有 HCI 教授的合作

---

### pioneer_with_allies（target=none, faculty=many）

**人设：** 开拓者 + 强盟友。最复杂场景——目标系无 HCI，但学院有成熟 HCI 团队。

**核心矛盾：** 必须同时说服两群人：
- 目标系 CS 评委：不懂 HCI，需要技术伪装
- 学院 HCI 教授（可能作为外部评审）：懂 HCI，评判合作潜力

**关键陷阱：** 不能让人觉得"你应该去 HCI 系而不是目标系"。

#### Cover Letter
- 技术硬核基调打底
- 用一段专讲跨系合作：**优先点名目标系内有交集的教授**，不够时补充其他系 HCI 教授
- 必须论证：为什么你的工作属于目标系（例："agentic AI 的 human evaluation 方法论是 AI 系的核心需求，而非 HCI 系的边界课题"）

#### Research Statement
- "硬化"语言为主（为 CS 评委）
- 加 "Cross-departmental synergies" 段落（点名 HCI 教授及具体合作方向）
- 点名策略同 Cover Letter

#### Teaching Statement
- CS 核心课能力 + 目标系 catalog 中的具体课程
- 提出与 HCI 系**联合开课**的可能性（作为加分项，不是主打）

---

### builder（target=few, faculty=few）

**人设：** 建设者。院系已有小规模 HCI 集群，急需扩充。

#### Cover Letter
- 明确点名现有 HCI 教授，阐述研究互补性
  - ✅ "我的 X 方向与 Prof.A 的 Y 方向形成天然互补，共同覆盖从 Z1 到 Z2 的完整研究范围"
  - ❌ 申请与现有教授**完全重叠**的方向
- 展示"桥梁"价值：连接 HCI 小组与主流 CS 教授

#### Research Statement
- 展示与现有研究的协同效应（而非竞争）
- 强调研究的社会/应用价值（比 pure_pioneer 更可以用"人"的语言）

#### Teaching Statement
- 展示课程如何与现有课程拼成完整 HCI Track（"目前已有 X 和 Y，我可以补 Z"）
- 从目标系 catalog 找**缺口课程**，提出补全方案
- 列出能帮助建立硕博项目的课程

---

### builder_in_rich_ecosystem（target=few, faculty=many）

**人设：** 建设者 + 丰富生态。类似 builder，但可提出更大规模的倡议。

#### 特殊策略
- 可提出建立**跨系研究中心**或**硕士项目**
- 利用学院现有 HCI 资源作为依托，降低风险感
- 比 builder 更可以展示"领导力"愿景

---

### specialist（target=many, faculty=many）

**人设：** 专家。HCI 本身没有稀缺性，必须有"绝活"。

#### Cover Letter
- 愿景驱动：提出**新子领域**或新研究议程（不仅是你做过什么）
- 展示跨学院合作能力和学术领导力
- 引用目标院系教授的工作：定位而非奉承（"Prof.X 解决了 A，我将 A 和 B 结合开启 C"）

#### Research Statement
- 理论贡献 > 系统贡献
- 展示"第二阶影响"：工具使用量、数据集下载量、政策采纳
- 强调 Community Service（Workshop Organizer, AC 等角色）

#### Teaching Statement
- 工作室教学法（Studio Model）、项目制学习（PBL）
- 博士指导理念（这里招的不只是研究员，而是未来的学术领袖）
- 从 catalog 中选**高阶/研究生** HCI 课程

---

## 四、点名策略（通用规则）

1. **优先**点名目标系内有研究交集的教授（即使非 HCI 方向）
2. 目标系匹配不足时，**补充**同校其他系 HCI 教授
3. 同校多系投递时：每份材料只点名该系 + 跨系合作对象，**不提另一份申请**

## 五、课程匹配规则

1. Step 2 须爬取目标系 course catalog（五层 fallback）
2. 从 catalog 识别 Sophia 能教的课程（核心课 + 选修课）
3. 根据密度策略调整呈现顺序：
   - **pioneer 系列**: CS 核心课在前，HCI 课在后（作为新课）
   - **builder 系列**: 互补课程在前（填补 HCI Track 缺口），列课程编号
   - **specialist**: 高阶/研究生 HCI 课在前

## 六、参考资料

- 原始策略报告：`general/research_job_rules/大学教职申请：HCI研究者数量策略.md`
- 设计文档：`overseas_pipeline/docs/plans/2026-02-19-hci-density-strategy-design.md`
```

**Step 3: 验证文件存在**
```bash
ls -la overseas_pipeline/strategies/hci_density_strategy.md
```

**Step 4: Commit**
```bash
git add overseas_pipeline/strategies/hci_density_strategy.md
git commit -m "feat: add HCI density strategy guide for Step 2/3"
```

---

## Task 2: 实现 hci_density_classifier.py

**Files:**
- Create: `overseas_pipeline/src/hci_density_classifier.py`

**Step 1: 写入脚本**

```python
#!/usr/bin/env python3
"""
hci_density_classifier.py -- Step 1 辅助：HCI 密度自动分类

从 faculty_data.json 中读取 faculty 列表，
按 research_interests 匹配 HCI 关键词，
推断双层密度分类（target_dept + faculty_wide），
写回 faculty_data.json 的 hci_density 字段。

用法:
  python hci_density_classifier.py --input output/monash_university/faculty_data.json
  python hci_density_classifier.py --input output/monash_university/faculty_data.json --target-dept "DSAI"
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
    "explainability", "interpretability",  # 与 HCI 交叉的 AI 方向
]

STRATEGY_MATRIX = {
    ("none", "none"):   "pure_pioneer",
    ("none", "few"):    "pioneer_with_few_allies",
    ("none", "many"):   "pioneer_with_allies",
    ("few",  "none"):   "builder",          # 罕见
    ("few",  "few"):    "builder",
    ("few",  "many"):   "builder_in_rich_ecosystem",
    ("many", "many"):   "specialist",
}


def count_to_level(count: int) -> str:
    if count == 0:
        return "none"
    elif count <= 3:
        return "few"
    else:
        return "many"


def is_hci_researcher(faculty: dict, keywords: list[str]) -> bool:
    interests = " ".join(faculty.get("research_interests", [])).lower()
    return any(kw.lower() in interests for kw in keywords)


def classify(faculty_data: dict, target_dept_name: str | None, keywords: list[str]) -> dict:
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
    print(f"Target dept: {result['target_dept']['level']} ({result['target_dept']['count']} people)")
    if result['target_dept']['hci_members']:
        print(f"  Members: {', '.join(result['target_dept']['hci_members'])}")
    print(f"Faculty wide: {result['faculty_wide']['level']} ({result['faculty_wide']['count']} people)")
    if result['faculty_wide']['hci_members']:
        print(f"  Members: {', '.join(result['faculty_wide']['hci_members'])}")
    print(f"Strategy: {result['strategy']}")

    if args.dry_run:
        print("\n[dry-run] Not writing to file.")
        return

    faculty_data["hci_density"] = result

    with open(input_path, "w", encoding="utf-8") as f:
        json.dump(faculty_data, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Written to {input_path}")


if __name__ == "__main__":
    main()
```

**Step 2: 用现有测试数据验证**
```bash
python overseas_pipeline/src/hci_density_classifier.py \
  --input overseas_pipeline/output/monash_university_0218/faculty_data.json \
  --target-dept "DSAI" \
  --dry-run
```

期望输出（大致）：
```
=== HCI Density Classification ===
Target dept: none (0 people)
Faculty wide: many (3+ people)
Strategy: pioneer_with_allies
[dry-run] Not writing to file.
```

**Step 3: 真实写入验证**
```bash
# 先备份
cp overseas_pipeline/output/monash_university_0218/faculty_data.json \
   overseas_pipeline/output/monash_university_0218/faculty_data.json.bak

python overseas_pipeline/src/hci_density_classifier.py \
  --input overseas_pipeline/output/monash_university_0218/faculty_data.json \
  --target-dept "DSAI"

# 检查 hci_density 字段是否写入
python3 -c "
import json
d = json.load(open('overseas_pipeline/output/monash_university_0218/faculty_data.json'))
print(json.dumps(d.get('hci_density', {}), indent=2, ensure_ascii=False))
"
```

**Step 4: Commit**
```bash
git add overseas_pipeline/src/hci_density_classifier.py
git commit -m "feat: add HCI density classifier (Step 1 code layer)"
```

---

## Task 3: 实现 course_catalog_scraper.py

**Files:**
- Create: `overseas_pipeline/src/course_catalog_scraper.py`

**Step 1: 写入脚本**

```python
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
  Layer 3:   Tavily Search API（搜索课程页面）

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
import os
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: pip install requests", file=sys.stderr)
    sys.exit(1)

TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "")
TIMEOUT = 20

HCI_COURSE_KEYWORDS = [
    "hci", "human-computer", "interaction design", "user experience",
    "ux", "usability", "accessibility", "human factors",
    "interface", "user interface", "human-ai", "conversational",
    "visualization", "information design",
]

BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def log(msg):
    print(f"[course_scraper] {msg}", flush=True)


def is_blocked(text: str) -> bool:
    signals = ["just a moment", "cf_chl_opt", "challenge-platform",
               "enable javascript", "403 forbidden", "access denied"]
    low = text.lower()
    return any(s in low for s in signals) or len(text) < 300


# --- Fetch layers ---

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
        resp = requests.get(f"https://r.jina.ai/{url}",
                            headers={"User-Agent": BROWSER_HEADERS["User-Agent"]},
                            timeout=TIMEOUT)
        if len(resp.text) < 500 or "error" in resp.text[:200].lower():
            log("  ✗ Jina returned short/error response")
            return None
        log(f"  ✓ {len(resp.text)} chars")
        return resp.text
    except Exception as e:
        log(f"  ✗ {e}")
        return None


def layer2_tavily_extract(url: str) -> str | None:
    if not TAVILY_API_KEY:
        log("  ⚠ TAVILY_API_KEY not set, skipping Layer 2")
        return None
    log(f"Layer 2: Tavily Extract")
    try:
        resp = requests.post(
            "https://api.tavily.com/extract",
            headers={"Authorization": f"Bearer {TAVILY_API_KEY}",
                     "Content-Type": "application/json"},
            json={"urls": [url]},
            timeout=TIMEOUT,
        )
        data = resp.json()
        results = data.get("results", [])
        if not results:
            log("  ✗ No results")
            return None
        content = results[0].get("raw_content", "")
        log(f"  ✓ {len(content)} chars")
        return content
    except Exception as e:
        log(f"  ✗ {e}")
        return None


def layer2_5_wayback(url: str) -> str | None:
    log(f"Layer 2.5: Wayback Machine")
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


def layer3_tavily_search(url: str, school: str = "") -> str | None:
    if not TAVILY_API_KEY:
        log("  ⚠ TAVILY_API_KEY not set, skipping Layer 3")
        return None
    domain = url.split("/")[2] if "//" in url else url
    query = f"site:{domain} course catalog {school} courses list"
    log(f"Layer 3: Tavily Search '{query}'")
    try:
        resp = requests.post(
            "https://api.tavily.com/search",
            headers={"Authorization": f"Bearer {TAVILY_API_KEY}",
                     "Content-Type": "application/json"},
            json={"query": query, "max_results": 5, "include_raw_content": True},
            timeout=TIMEOUT,
        )
        data = resp.json()
        results = data.get("results", [])
        if not results:
            log("  ✗ No results")
            return None
        combined = "\n\n".join(r.get("content", "") for r in results)
        log(f"  ✓ {len(combined)} chars from {len(results)} results")
        return combined
    except Exception as e:
        log(f"  ✗ {e}")
        return None


def fetch_with_fallback(url: str, school: str = "") -> tuple[str | None, str]:
    """五层 fallback，返回 (content, layer_used)"""
    content = layer1_curl(url)
    if content:
        return content, "layer1_curl"

    content = layer1_5_jina(url)
    if content:
        return content, "layer1.5_jina"

    content = layer2_tavily_extract(url)
    if content:
        return content, "layer2_tavily_extract"

    content = layer2_5_wayback(url)
    if content:
        return content, "layer2.5_wayback"

    content = layer3_tavily_search(url, school)
    if content:
        return content, "layer3_tavily_search"

    return None, "all_failed"


# --- Course extraction (heuristic, agent will refine) ---

def is_hci_course(name: str) -> bool:
    low = name.lower()
    return any(kw in low for kw in HCI_COURSE_KEYWORDS)


def extract_courses_heuristic(text: str) -> list[dict]:
    """
    简单启发式提取：在文本中匹配课程编号 + 名称模式。
    Agent 会在此基础上审查和补充。
    """
    courses = []
    # 常见课程编号格式：FIT5145, CS101, COMP3702, INFO4112 等
    pattern = re.compile(
        r'\b([A-Z]{2,6}\s*\d{3,5}[A-Z]?)\s*[:\-–]?\s*([^\n\r,;]{10,80})',
        re.MULTILINE
    )
    for match in pattern.finditer(text):
        code = match.group(1).strip().replace(" ", "")
        name = match.group(2).strip().rstrip(".,;")
        if len(name) < 5:
            continue
        # 粗略判断是否是本科/研究生（编号数字部分）
        digits = re.search(r'\d+', code)
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
    seen = set()
    unique = []
    for c in courses:
        if c["code"] not in seen:
            seen.add(c["code"])
            unique.append(c)

    return unique


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="Course catalog URL")
    parser.add_argument("--output", help="Path to faculty_data.json to update")
    parser.add_argument("--school", default="", help="School name (for search fallback)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    content, layer = fetch_with_fallback(args.url, args.school)

    if not content:
        print("ERROR: All five layers failed. Manual paste required.", file=sys.stderr)
        sys.exit(1)

    courses = extract_courses_heuristic(content)
    log(f"Extracted {len(courses)} courses ({sum(1 for c in courses if c['hci_relevant'])} HCI-relevant)")

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

    if args.dry_run:
        print("\n[dry-run] Not writing.")
        return

    if not args.output:
        print("WARNING: --output not specified. Printing JSON only.")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    output_path = Path(args.output)
    if output_path.exists():
        with open(output_path, encoding="utf-8") as f:
            faculty_data = json.load(f)
    else:
        faculty_data = {}

    faculty_data.update(result)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(faculty_data, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Written to {output_path}")


if __name__ == "__main__":
    main()
```

**Step 2: dry-run 测试（用已有学校数据）**
```bash
python overseas_pipeline/src/course_catalog_scraper.py \
  --url "https://www.monash.edu/it/dsai/courses" \
  --school "Monash University DSAI" \
  --dry-run
```

观察：五层中哪层成功、提取到多少课程。

**Step 3: Commit**
```bash
git add overseas_pipeline/src/course_catalog_scraper.py
git commit -m "feat: add course catalog scraper with five-layer fallback (Step 1 code layer)"
```

---

## Task 4: 更新 CLAUDE.md

**Files:**
- Modify: `overseas_pipeline/CLAUDE.md`

需要更新三个地方：

**Step 1: 网页抓取规则（顶部）— 三层改五层**

将：
```
1. **Layer 1**: WebFetch / Jina Reader / curl + browser UA
2. **Layer 2**: Tavily Extract API（`$TAVILY_API_KEY`）
3. **Layer 3**: Tavily Search API
```

改为：
```
1. **Layer 1**: curl + browser UA
2. **Layer 1.5**: Jina Reader（`https://r.jina.ai/`，免费无 key，适合 Medium/Cloudflare 场景）
3. **Layer 2**: Tavily Extract API（`$TAVILY_API_KEY`）
4. **Layer 2.5**: Wayback Machine（`web.archive.org/web/{year}/原URL`，免费，适合博客/个人网站）
5. **Layer 3**: Tavily Search API
```

**Step 2: Step 1 流程 — 新增步骤 6/7/8**

在"研究 {学校名}"的执行步骤中，现有步骤 5/6 之后追加：

```markdown
6. **HCI 密度分类（Code）**：
   ```
   python overseas_pipeline/src/hci_density_classifier.py \
     --input output/{school_id}/faculty_data.json \
     [--target-dept "{目标系名称}"]
   ```
   → 自动推断双层密度（target_dept + faculty_wide）和策略标签，写入 `faculty_data.json` 的 `hci_density` 字段
   → **agent 随后补充 `strategy_rationale`**（自然语言解释，检查边界情况）

7. **课程体系抓取（Code）**：
   ```
   python overseas_pipeline/src/course_catalog_scraper.py \
     --url "{目标系课程页面URL}" \
     --output output/{school_id}/faculty_data.json \
     --school "{学校名}"
   ```
   → 五层 fallback 抓取课程列表，写入 `faculty_data.json` 的 `department_courses` 字段
   → 如课程页面 URL 未知，用 Tavily 搜索 `site:{domain} course catalog`
   → **agent 随后审查**：识别 Sophia 能教的课，按密度策略排序（pioneer→CS 核心课在前；builder→互补课程在前；specialist→高阶课在前）

8. **agent 审查补充**：
   - 检查密度分类是否有边界遗漏（如某教授写 "computational social science" 但实际做 HCI）
   - 补充 `hci_density.strategy_rationale` 自然语言解释
   - 将密度判断 + 课程匹配概览写入 `step1_summary.md`，供 Sophia 异步审查
   - Sophia 有异议时给 comment 覆盖，无 comment 则流程继续
```

**Step 3: Step 2 流程 — 新增 HCI 密度策略维度**

在"分析 {学校名}"的执行步骤 6（规则冲突检查）之前插入：

```markdown
5b. 读取 HCI 密度策略：
   - 读取 `overseas_pipeline/strategies/hci_density_strategy.md`
   - 从 `faculty_data.json` 获取 `hci_density.strategy`
   - 确定点名优先级（目标系教授优先 → 其他系补充）
   - 确定课程匹配顺序（按策略类型）
```

在 `fit_report.md` 格式中新增维度：

```markdown
### HCI 密度策略分析 (X/10)
- 目标系 HCI 密度：{level}（{count} 人：{names}）
- 学院 HCI 密度：{level}（{count} 人：{names}）
- 推荐策略：`{strategy}`
- 策略要点：
  - {评委构成对应的修辞建议}
  - 点名优先级：{目标系交集教授} → {其他系补充教授}
  - {如 pioneer_with_allies：论证为什么属于目标系的关键点}

### 各材料调整建议

#### Cover Letter
- **密度策略** [`{strategy}`]：{具体修辞建议，引用策略文件对应章节}
- **点名建议**：
  - 目标系（优先）：{教授列表 + 合作点}
  - 跨系补充（如有需要）：{教授列表 + 合作点}

#### Teaching Statement
- **密度策略** [`{strategy}`]：{课程呈现顺序建议}
- **目标系课程匹配**：
  - 可教的现有课：{课程编号 + 名称}
  - 可开设新课：{课程编号 + 名称}
  - 联合开课建议：{与哪个系合作，开什么课}
```

**Step 4: Step 3 流程 — 新增密度策略读取和一致性检查**

在"生成材料 {学校名}"的执行步骤 1 前追加：

```markdown
0. 读取密度策略文件：
   - `overseas_pipeline/strategies/hci_density_strategy.md`
   - `faculty_data.json` 中的 `hci_density` 和 `department_courses` 字段
   - 确定本次生成的策略类型（`pure_pioneer` / `pioneer_with_allies` / 等）

（完成后）如存在 `related_applications` 字段：
   - 读取同校其他投递的 fit_report.md
   - 在每份 notes.md 的"给 Sophia 的审核重点"中追加同校一致性检查段落：
     ```markdown
     ## 同校多系一致性检查
     - 本校另一份申请：{department}（{strategy} 策略，状态：{status}）
     - 核心叙事一致性：✅/⚠ {描述两份材料核心定位是否统一}
     - 侧重点差异：本系版（{简述}）vs 另一系版（{简述}）
     - ⚠ 注意：{具体提醒，如"两份 Cover Letter 均未提及另一份申请"，或"Research Statement 点名教授无重叠"等}
     ```
```

**Step 5: 验证 CLAUDE.md 没有格式损坏**
```bash
wc -l overseas_pipeline/CLAUDE.md
head -30 overseas_pipeline/CLAUDE.md
```

**Step 6: Commit**
```bash
git add overseas_pipeline/CLAUDE.md
git commit -m "feat: update pipeline CLAUDE.md — five-layer fallback + HCI density integration"
```

---

## Task 5: 验证端到端（Smoke Test）

**用现有 Monash 数据跑一遍 Task 2/3 的真实写入，检查 faculty_data.json 结构完整性**

**Step 1: 跑密度分类**
```bash
python overseas_pipeline/src/hci_density_classifier.py \
  --input overseas_pipeline/output/monash_university_0218/faculty_data.json \
  --target-dept "DSAI"
```

**Step 2: 跑课程抓取（dry-run，因为需要网络）**
```bash
python overseas_pipeline/src/course_catalog_scraper.py \
  --url "https://www.monash.edu/it/dsai/courses" \
  --school "Monash University" \
  --dry-run
```

**Step 3: 检查 JSON 结构完整性**
```bash
python3 -c "
import json
d = json.load(open('overseas_pipeline/output/monash_university_0218/faculty_data.json'))
fields = ['school', 'faculty', 'hci_density', 'scrape_date']
for f in fields:
    status = '✅' if f in d else '❌'
    print(f'{status} {f}')
hd = d.get('hci_density', {})
print(f'  strategy: {hd.get(\"strategy\")}')
print(f'  target_dept level: {hd.get(\"target_dept\", {}).get(\"level\")}')
print(f'  faculty_wide level: {hd.get(\"faculty_wide\", {}).get(\"level\")}')
"
```

**Step 4: 最终 commit（如有残留修改）**
```bash
git status
git add -p  # 按需选择
```

---

## 实现顺序

```
Task 1 (策略文件) → Task 2 (密度分类脚本) → Task 3 (课程抓取脚本)
                                                        ↓
Task 4 (CLAUDE.md 更新) ← 需要了解 Task 2/3 的调用接口
                                                        ↓
                                               Task 5 (Smoke Test)
```

Task 1、2、3 可以并行，Task 4 在 2/3 完成后进行。
