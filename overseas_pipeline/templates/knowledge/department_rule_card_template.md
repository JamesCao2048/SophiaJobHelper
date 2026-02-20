# {学校} — {院系} 规则卡

## 元信息
- school_id: {school_id}
- dept_id: {dept_id}
- region: {region}
- version: v1
- last_updated: YYYY-MM-DD
- status: draft

---

## 1. 基本信息

| 项目 | 内容 |
|---|---|
| 学校 | {学校全称} |
| 院系 | {院系全称} |
| 别名 | {可选别名} |
| 地点 | {城市, 州/省, 国家} |
| 类型 | {公立/私立/其他} |
| 招聘主页 | {url} |
| 院系主页 | {url} |

---

## 2. 与地区卡差异（覆盖规则）

| 规则 | 地区卡默认 | 本系覆盖 | 证据 |
|---|---|---|---|
| {rule_name} | {region_default} | {dept_override} | {source_url} |

---

## 3. 关键决策人

| 阶段 | 姓名 | 职务 | 范围 | 证据 |
|---|---|---|---|---|
| {stage} | {name} | {title} | {scope} | {source} |

---

## 4. HCI 生态与合作

- 目标系 HCI 密度：many|few|none
- 学院范围 HCI 密度：many|few|none
- 关键合作人：
  - {name}（{dept}, {overlap}）

---

## 5. 教学与课程

- 课程目录：{url}
- 可教授的现有课：
  - {course_code} {course_name}
- 可提出的新课：
  - {new_course_name}

---

## 6. 风险与待确认

- 已确认：
  - {verified_fact}
- 待确认：
  - {open_question}

---

## 7. 同校复用记录

- from_dept_id: {dept_id}
- reused_fields: [{field_1}, {field_2}]
- rationale: {reason}

---

## Te Tiriti 学校信号（仅 region=new_zealand）

- **signal_level**: strong | moderate | light
- **assessed_date**: YYYY-MM-DD
- **key_framework**: 框架名称（如 Waipapa Taumata Rau，无则填 N/A）
- **key_values**: 术语1, 术语2, ...（无则填 N/A）
- **evidence**:
  1. "原文摘录（英文原文）"
     - source: [文档名](URL)
  2. "原文摘录（英文原文）"
     - source: [文档名](URL)
- **notes**: 其他备注（如 PVC(Māori) 审查权限、面试必考条约题等）

---

## AU Indigenous 学校信号（仅 region=australia）

- **signal_level**: strong | moderate | light
- **assessed_date**: YYYY-MM-DD
- **rap_tier**: Stretch | Innovate | Reflect | Elevate | none
- **rap_document**: RAP 文档名称（如 "Innovate RAP 2024-2026"，无则填 N/A）
- **indigenous_strategy**: 原住民战略名称（如 "Murmuk Djerring"，无则填 N/A）
- **indigenous_centre**: 原住民学术支持中心（如 "Murrup Barak"，无则填 N/A）
- **evidence**:
  1. "原文摘录（英文原文）"
     - source: [文档名](URL)
  2. "原文摘录（英文原文）"
     - source: [文档名](URL)
- **notes**: 其他备注（如 DVC(Indigenous) 审查权限、特定 KPI、学院级原住民战略等）

---

## 变更记录
- YYYY-MM-DD：初始化
