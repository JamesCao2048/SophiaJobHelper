# 地区信号 JSON 格式与学校卡字段规范

> **参考文件** — 由 workflow 步骤引用，不可独立执行。
> **引用方**：`workflows/step1/step1d_regional_signals.md` D1/D2、`workflows/step2_analysis.md` step 8/9

---

## Te Tiriti（NZ）

### dept_data.json te_tiriti 块格式

```json
"te_tiriti": {
  "jd_signal": {
    "level": "explicit | boilerplate | no_mention",
    "evidence": [
      {
        "text": "原文摘录（英文原文）",
        "location": "所在板块/bullet，如 'Key Responsibilities, bullet 7'",
        "source": "raw/jd_main.md"
      }
    ]
  },
  "school_signal": {
    "level": "strong | moderate | light",
    "evidence": [
      {
        "text": "原文摘录（英文原文）",
        "url": "来源 URL",
        "document_name": "文档名称"
      }
    ],
    "key_framework_name": "该校专有框架名称（如有）",
    "key_values": ["该校专有毛利价值观术语列表"]
  },
  "strategy": "skip | subtle | moderate | strong | full_treaty",
  "strategy_rationale": ""
}
```

### 学校卡 Te Tiriti 字段格式

```markdown
## Te Tiriti 学校信号

- **signal_level**: strong | moderate | light
- **assessed_date**: YYYY-MM-DD
- **key_framework**: 框架名称（如 Waipapa Taumata Rau）
- **key_values**: 术语1, 术语2, ...
- **evidence**:
  1. "原文摘录..."
     - source: [文档名](URL)
  2. "原文摘录..."
     - source: [文档名](URL)
- **notes**: 其他备注（如 PVC(Māori) 审查权限等）
```

---

## AU Indigenous

### dept_data.json au_indigenous 块格式

```json
"au_indigenous": {
  "jd_signal": {
    "level": "explicit | boilerplate | no_mention",
    "evidence": [
      {
        "text": "原文摘录（英文原文）",
        "location": "所在板块/bullet，如 'Selection Criteria, item 3'",
        "source": "raw/jd_main.md"
      }
    ]
  },
  "school_signal": {
    "level": "strong | moderate | light",
    "evidence": [
      {
        "text": "原文摘录（英文原文）",
        "url": "来源 URL",
        "document_name": "文档名称"
      }
    ],
    "rap_tier": "Reflect | Innovate | Stretch | Elevate | N/A",
    "indigenous_strategy_name": "名称或 N/A",
    "academic_support_center": "名称或 N/A"
  },
  "strategy": "skip | subtle | moderate | strong | full_rap",
  "strategy_rationale": ""
}
```

### 学校卡 AU Indigenous 字段格式

```markdown
## AU Indigenous 学校信号

- **signal_level**: strong | moderate | light
- **assessed_date**: YYYY-MM-DD
- **rap_tier**: Reflect | Innovate | Stretch | Elevate | N/A
- **indigenous_strategy**: 名称或 N/A
- **academic_support_center**: 名称或 N/A
- **evidence**:
  1. "原文摘录..."
     - source: [文档名](URL)
  2. "原文摘录..."
     - source: [文档名](URL)
- **notes**: 其他备注
```
