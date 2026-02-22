# dept_data.json + faculty/{slug}.json 完整格式

> **参考文件** — 由 workflow 步骤引用，不可独立执行。
> **引用方**：`workflows/step1/step1b_scrape_analyze.md` B3、`workflows/step1_research.md`

## 概述

院系研究数据拆分为两级文件：

| 文件 | 内容 | 路径 |
|------|------|------|
| `dept_data.json` | 院系级元数据、JD、画像、HCI 密度、战略情报、教学上下文、数据质量、faculty 摘要索引 | `output/{school_id}/{dept_id}/dept_data.json` |
| `faculty/{slug}.json` | 单个教授的详细信息（背景、重叠论文、研究兴趣等） | `output/{school_id}/{dept_id}/faculty/{slug}.json` |

`dept_data.json` 中的 `faculty_summary[]` 数组为每位教授保留一行摘要 + `file` 指针，供快速索引。详细数据按需从 `faculty/{slug}.json` 读取。

---

## dept_data.json 格式

```json
{
  "metadata": {
    "school": "University of Auckland",
    "school_id": "university_of_auckland",
    "department": "School of Computer Science",
    "dept_id": "cs",
    "region": "new_zealand",
    "generated_date": "YYYY-MM-DD",
    "workflow_status": {
      "step1": "complete | in_progress | not_started",
      "step2": "complete | in_progress | not_started",
      "step3": "complete | in_progress | not_started"
    }
  },

  "job_posting": {
    "job_url": "https://...",
    "api_url": "https://... (如有结构化 API)",
    "ref_number": "REF38990C",
    "position_number": "55562462",
    "title": "Lecturer - Data Science/AI",
    "grade": "Senior Lecturer",
    "contract_type": "Permanent",
    "hours": "Full-time (40 hours/week)",
    "salary_nzd": "$99,788 – $112,730",
    "location": "Auckland City Campus",
    "posted_date": "YYYY-MM-DD",
    "closing_date": "YYYY-MM-DD",
    "head_of_school": "Professor Giovanni Russello",
    "contact_email": "g.russello@auckland.ac.nz",
    "materials_required": [
      "Cover Letter",
      "CV",
      "Teaching Philosophy Statement",
      "Research Statement"
    ],
    "jd_raw_path": "raw/jd_main.md"
  },

  "dept_profile": {
    "official_category": "cs | ischool | ds | aix | other",
    "official_name": "School of Computer Science",
    "qs_ranking_cs_2024": 99,
    "qs_ranking_overall_2025": 65,
    "faculty_size": "75+ academic staff",
    "dimensions": {
      "quantitative_rigor": {
        "level": "high | medium | low",
        "confidence": "high | medium | low",
        "evidence": ["证据1（JD原文/faculty背景/课程信号）", "证据2"]
      },
      "interdisciplinary_openness": {
        "level": "high | medium | low",
        "confidence": "high | medium | low",
        "evidence": ["证据1", "证据2"]
      },
      "system_building_preference": {
        "level": "high | medium | low",
        "confidence": "high | medium | low",
        "evidence": ["证据1", "证据2"]
      },
      "social_impact_focus": {
        "level": "high | medium | low",
        "confidence": "high | medium | low",
        "evidence": ["证据1", "证据2"]
      }
    },
    "needs_user_review": false,
    "founding": {
      "year": 1981,
      "method": "organic_growth | spinoff | merger | new_establishment",
      "motivation": "简短描述建院动机或背景"
    },
    "faculty_background_distribution": {
      "hci_qual": 6,
      "hci_systems": 2,
      "ml_theory": 2,
      "ml_applied": 10,
      "nlp": 1,
      "other_unknown": 4,
      "note": "说明估算方式或待校准标注"
    },
    "notes": "维度判断的补充说明（如有矛盾信号或边界情况）"
  },

  "hci_density": {
    "target_dept": {
      "level": "many | few | none",
      "count": 8,
      "hci_members": ["Prof. A", "Prof. B"],
      "note": "补充说明（如数据源局限）",
      "members_note": "成员变动说明（如有人员调动）"
    },
    "faculty_wide": {
      "level": "many | few | none",
      "count": 0,
      "hci_members": [],
      "note": "跨院系 HCI 协作者说明"
    },
    "strategy": "specialist | builder | pioneer_with_allies | pioneer_with_few_allies | pure_pioneer",
    "strategy_rationale": "...",
    "classified_at": "YYYY-MM-DD",
    "keywords_used": 52
  },

  "strategic_intelligence": {
    "school_level": {
      "vision": "学校愿景/使命摘要",
      "strategic_priorities": ["优先级1", "优先级2"],
      "source_date": "YYYY-MM-DD"
    },
    "clusters": [
      {
        "name": "Human-Computer Interaction",
        "url": "https://...",
        "description": "从官网提取的简介",
        "sophia_alignment": "high | medium | low",
        "alignment_notes": "Sophia 与此 cluster 最新方向的具体结合点",
        "source": "raw/cluster_hci.md"
      }
    ],
    "cross_faculty_scan": null
  },

  "te_tiriti": {
    "jd_signal": "explicit | boilerplate | no_mention",
    "jd_signal_evidence": [
      {
        "text": "原文摘录",
        "location": "所在板块/bullet",
        "weight": "high | medium | low — 说明"
      }
    ],
    "school_signal": "strong | moderate | light",
    "school_signal_evidence": [
      {
        "text": "原文摘录",
        "source": "文档名称",
        "url": "来源 URL"
      }
    ],
    "school_framework_name": "框架名称（如 Waipapa framework）",
    "school_key_values": ["Manaakitanga", "Whanaungatanga"],
    "school_programme": "Tuākana Māori and Pacific support programme",
    "assessed_date": "YYYY-MM-DD",
    "strategy": "skip | subtle | moderate | strong | full_treaty",
    "strategy_rationale": "...",
    "note": "补充说明",
    "interrupt_triggered": true
  },

  "teaching_context": {
    "programs": ["Bachelor of Science in Computer Science", "..."],
    "course_catalog_url": "https://...",
    "course_catalog_scraped": true,
    "course_catalog_scrape_method": "说明爬取方式",
    "department_courses": [
      {
        "code": "COMPSCI 345",
        "name": "Human-computer Interaction",
        "level": "300",
        "sophia_can_teach": true,
        "priority_for_sophia": 1,
        "note": "课程与 Sophia 的匹配说明",
        "verified": true,
        "source_url": "https://..."
      }
    ],
    "courses_note": "课程数据补充说明",
    "teaching_load_note": "教学负荷说明"
  },

  "decision_makers": {
    "head_of_school": "Professor Giovanni Russello",
    "contact": "g.russello@auckland.ac.nz",
    "committee_structure": "委员会结构说明"
  },

  "data_quality": {
    "overall": "high | medium | low",
    "issues": ["问题1", "问题2"],
    "hci_count_adjustment": "调整说明（如有人员变动）",
    "last_updated": "YYYY-MM-DD"
  },

  "related_applications": [],

  "faculty_summary": [
    {
      "name": "Prof. Jane Smith",
      "title": "Professor",
      "overlap_with_sophia": "high | medium | low | none",
      "clusters": ["HCI", "AI/ML"],
      "homepage": "https://...",
      "file": "faculty/jane_smith.json"
    }
  ]
}
```

### 字段说明

| 字段 | 说明 |
|------|------|
| `metadata.workflow_status` | 各步骤完成状态，Step 1 写入时初始化 |
| `dept_profile.dimensions.*` | 每个维度为嵌套对象：`{level, confidence, evidence}` |
| `dept_profile.founding` | 嵌套对象：`{year, method, motivation}` |
| `dept_profile.faculty_background_distribution` | 院系教师背景分布统计（在 dept_profile 内部） |
| `strategic_intelligence.clusters[].sophia_alignment` | 旧字段名 `alignment_with_sophia` 已重命名 |
| `strategic_intelligence.clusters[].alignment_notes` | 旧字段名 `alignment_reason` 已重命名 |
| `faculty_summary[].file` | 指向 `faculty/{slug}.json` 的相对路径 |
| `faculty_summary[].homepage` | 旧字段名 `profile_url` 已重命名 |
| `te_tiriti` | 仅 NZ 学校需要；详见 `regional_signal_schemas.md` |

### 条件字段

以下字段仅在特定地区出现：

| 字段 | 条件 |
|------|------|
| `te_tiriti` | `region == "new_zealand"` |
| `au_indigenous`（格式同 `regional_signal_schemas.md`） | `region == "australia"` |

---

## faculty/{slug}.json 格式

文件名规则：教授姓名转 slug（小写，空格/特殊字符替换为下划线），如 `jane_smith.json`、`padriac_amato_tahua_oleary.json`。

```json
{
  "name": "Prof. Jane Smith",
  "title": "Professor",
  "homepage": "https://...",
  "clusters": ["HCI", "AI/ML"],
  "overlap_with_sophia": "high | medium | low | none",
  "overlap_reason": "详细说明重叠原因",
  "overlap_confidence": "high | medium | low",
  "overlap_notes": "补充分析说明（如研究方向漂移、降权建议等）",
  "research_background": {
    "major": "hci_qual | hci_systems | ml_theory | ml_applied | nlp | se | systems | stats_ds | responsible_ai | interdisciplinary | cs_education | other",
    "minor": "nlp | hci_systems | null",
    "confidence": "high | medium | low",
    "note": "分类依据说明",
    "evidence_venues": ["CHI 2024 (qual study)", "CSCW 2023", "ACL 2022"]
  },
  "research_interests": ["human-AI interaction", "CSCW", "affective computing"],
  "research_interests_raw_scrape": "从官网原始抓取的兴趣描述（保留原文）",
  "google_scholar": "https://scholar.google.com/citations?user=xxxxx",
  "overlapping_papers": [
    {
      "title": "...",
      "venue": "CHI 2024",
      "year": 2024,
      "url": "https://doi.org/...",
      "oa_url": "https://...",
      "local_pdf": "papers/Smith_2024_title.pdf",
      "abstract": "Full abstract text from OpenAlex (always populated when available, regardless of PDF status)",
      "relevance": "Direct overlap with CollabCoder line"
    }
  ],
  "profile_scraped": true,
  "current_institution": "说明（如已离校则标注）"
}
```

### 字段说明

| 字段 | 说明 |
|------|------|
| `homepage` | 旧字段名 `profile_url` 已重命名为 `homepage` |
| `research_interests` | 旧字段名 `research_interests_actual` 已重命名为 `research_interests` |
| `research_interests_raw_scrape` | 官网原始抓取文本，保留用于数据溯源 |
| `overlapping_papers[].local_pdf` | PDF 下载成功时填入，Step 2/3 优先使用 |
| `overlapping_papers[].abstract` | OpenAlex 拉取的摘要，PDF 不可用时作为 Step 2/3 的分析依据 |
| `overlapping_papers[].oa_url` | OpenAlex 返回的开放获取链接（若有），用于 PDF 下载尝试 |
| `profile_scraped` | 是否已完成个人主页详细爬取 |
| `current_institution` | 人员变动标注（如已离校） |

**Step 2/3 读取优先级**：`local_pdf` > `abstract`（两者都没有时在 `data_quality` 标注 warning）

---

## 迁移对照表

旧 `faculty_data.json` 单文件格式与新双文件格式的字段映射：

| 旧路径 | 新位置 | 变更 |
|--------|--------|------|
| `faculty_data.json`（顶层） | `dept_data.json` + `faculty/*.json` | 拆分为两级 |
| `.school`, `.school_id`, `.department`, `.dept_id`, `.region` | `dept_data.json` → `metadata.*` | 移入 metadata 对象 |
| `.job_url`, `.job_url` | `dept_data.json` → `job_posting.*` | 移入 job_posting 对象 |
| `.research_focus` | `dept_data.json` → `dept_profile` 或 `job_posting` | 按语义归类 |
| `.dept_profile.dimensions.quantitative_rigor` (flat) | `.dept_profile.dimensions.quantitative_rigor.{level, confidence, evidence}` | 平铺 → 嵌套 |
| `.dept_profile.founding` (flat) | `.dept_profile.founding.{year, method, motivation}` | 平铺 → 嵌套 |
| `.faculty_background_distribution`（顶层） | `dept_data.json` → `dept_profile.faculty_background_distribution` | 移入 dept_profile |
| `.strategic_intelligence.clusters[].alignment_with_sophia` | `.strategic_intelligence.clusters[].sophia_alignment` | 字段重命名 |
| `.strategic_intelligence.clusters[].alignment_reason` | `.strategic_intelligence.clusters[].alignment_notes` | 字段重命名 |
| `.faculty[]` | `faculty/{slug}.json`（独立文件） | 拆分为独立文件 |
| `.faculty[].profile_url` | `faculty/{slug}.json` → `homepage` | 字段重命名 |
| `.faculty[].research_interests_actual` | `faculty/{slug}.json` → `research_interests` | 字段重命名 |
| `faculty_data.sources.md` | `dept_data.sources.md` | 文件名同步更新 |
