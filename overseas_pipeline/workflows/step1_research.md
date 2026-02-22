# Step 1: Research（研究学校）

> ⚠️ **爬取强制规则**：Step 1 中所有 Claude Code 直接发出的 HTTP 请求，**必须通过 `python src/web_fetch_utils.py "URL"` 调用**，禁止直接使用 WebFetch 工具或手动 curl。脚本失败后的补救、cluster 爬取、Te Tiriti/AU Indigenous 种子 URL 等均适用此规则。

## 前提

需要学校名 + 院系 URL（或职位 URL）

---

## Phase 概览

| Phase | 文件 | 内容 | 触发条件 | 主要输出物 |
|-------|------|------|---------|-----------|
| A | `step1/step1a_setup.md` | 初始化与数据准备 | 始终执行 | output 目录、JD 原文 |
| B | `step1/step1b_scrape_analyze.md` | 爬取与分析 | 始终执行 | dept_data.json、faculty/、sources.md、papers/ |
| C | `step1/step1c_profiling.md` | 分类与画像 | 始终执行 | 规则卡、HCI 密度、dept_profile、课程、data_quality.json |
| D | `step1/step1d_regional_signals.md` | 地区信号检测 | region=new_zealand 或 australia | te_tiriti / au_indigenous 信号 |

**执行顺序**：A → B → C → D（条件触发）→ 数据质量评估

---

## 数据质量评估（Step 1 完成后必须执行）

完整规范（分级标准 + 消息模板）见 `references/data_quality_spec.md`。

---

## 数据文件格式

- `dept_data.json`：院系级数据（metadata、job_posting、dept_profile、hci_density、strategic_intelligence、te_tiriti、teaching_context、decision_makers、data_quality、faculty_summary[]）
- `faculty/{slug}.json`：个人 faculty 文件（name、title、homepage、clusters、research_interests、overlap_with_sophia、overlap_reason、research_background、overlapping_papers 等）

`faculty_summary[]` 中每条记录包含 `file` 字段指向对应的 `faculty/{slug}.json`。

完整 JSON schema 见 `references/faculty_data_schema.md`。
