# faculty_data.json 完整格式

> **参考文件** — 由 workflow 步骤引用，不可独立执行。
> **引用方**：`workflows/step1/step1b_scrape_analyze.md` B4、`workflows/step1_research.md`

```json
{
  "school": "Monash University",
  "school_id": "monash_university",
  "department": "Department of Data Science and AI",
  "dept_id": "dsai",
  "department_url": "https://...",
  "job_url": "https://...",
  "region": "australia",
  "research_focus": ["AI", "HCI", "data science"],
  "hci_density": {
    "target_dept": "many | few | none",
    "faculty_wide": "many | few | none",
    "strategy": "specialist | builder | pioneer_with_allies | pioneer_with_few_allies | pure_pioneer",
    "strategy_rationale": "...",
    "target_dept_hci_faculty": ["Prof. X (HCI)", "Prof. Y (CSCW)"],
    "cross_department_collaborators": [
      {
        "name": "Prof. Z",
        "department": "School of Design",
        "research_interests": ["interaction design"],
        "overlap_reason": "User study methods overlap"
      }
    ]
  },
  "department_courses": [
    {
      "code": "FIT3170",
      "name": "Software Engineering Practice",
      "level": "undergraduate",
      "sophia_can_teach": true,
      "density_strategy_priority": "core"
    }
  ],
  "sophia_teachable_courses": {
    "can_teach_existing": [],
    "can_propose_new": []
  },
  "dept_profile": {
    "official_category": "cs | ischool | ds | aix | other",
    "official_name": "Department of Computer Science",
    "founding": {
      "year": 1965,
      "method": "organic_growth | spinoff | merger | new_establishment",
      "motivation": "简短描述建院动机或背景",
      "notes": "辅助判断各维度的关键历史信息"
    },
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
    "dimension_notes": "维度判断的补充说明（如有矛盾信号或边界情况）",
    "confirmed_by_user": false
  },
  "strategic_intelligence": {
    "school_level": {
      "strategic_plan_url": "https://...",
      "key_priorities": ["战略优先级1（如 AI for Health）", "战略优先级2"],
      "sophia_alignment": "high | medium | low",
      "alignment_notes": "Sophia 的研究与学校战略的具体对齐点",
      "source": "raw/school_strategic_plan.md"
    },
    "clusters": [
      {
        "name": "Human-Centred Computing Group",
        "url": "https://...",
        "description": "从官网提取的简介",
        "key_faculty": ["Prof. A", "Prof. B"],
        "latest_projects": ["项目1", "项目2"],
        "sophia_alignment": "high | medium | low",
        "alignment_notes": "Sophia 与此 cluster 最新方向的具体结合点",
        "source": "raw/cluster_hcc.md"
      }
    ],
    "cross_school_opportunities": [
      {
        "school_name": "School of Medicine",
        "dept_name": "Health Informatics",
        "relevant_faculty": ["Dr. X"],
        "collaboration_angle": "AI-assisted clinical decision support",
        "trigger_reason": "IO=high + JD 明确提及跨学科合作"
      }
    ]
  },
  "faculty": [
    {
      "name": "Prof. Jane Smith",
      "title": "Professor",
      "research_interests": ["human-AI interaction", "CSCW"],
      "homepage": "https://...",
      "google_scholar": "https://scholar.google.com/citations?user=xxxxx",
      "overlap_with_sophia": "high",
      "overlap_reason": "Both work on human-AI collaboration for data analysis",
      "research_background": {
        "major": "hci_qual | hci_systems | ml_theory | nlp | se | systems | stats_ds | responsible_ai | interdisciplinary | cs_education | other",
        "minor": "nlp | hci_systems | null",
        "evidence_venues": ["CHI 2024 (qual study)", "CSCW 2023", "ACL 2022"]
      },
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
      ]
      // 字段说明：
      // local_pdf: PDF 下载成功时填入，Step 2/3 优先使用
      // abstract:  OpenAlex 拉取的摘要，PDF 不可用时作为 Step 2/3 的分析依据
      // oa_url:    OpenAlex 返回的开放获取链接（若有），用于 PDF 下载尝试
      // Step 2/3 读取优先级：local_pdf > abstract（两者都没有时在 data_quality 标注 warning）
    }
  ],
  "scrape_date": "YYYY-MM-DD",
  "scrape_method": "jina_reader"
}
```
