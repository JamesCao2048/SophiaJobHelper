# Step 2: Fit Analysis（分析匹配度）

## 前提

Step 1 已完成（`output/{school_id}/{dept_id}/faculty_data.json` 存在）

---

## 执行步骤

1. 读取 `output/{school_id}/{dept_id}/faculty_data.json`（含 `hci_density` 和 `department_courses` 字段）
2. 确定 region → 读取 `region_knowledge/regions/{region}.md`
3. 读取院系规则卡（用于覆盖地区卡差异）：
   - 主路径：`region_knowledge/schools/{school_id}/{dept_id}.md`
   - 副本路径：`output/{school_id}/{dept_id}/knowledge/{dept_id}.md`
   - 若主路径不存在但副本存在，读取副本并在 `step2_summary.md` 标注 "using_output_copy"
   - 若两者都不存在，按 "无院系覆盖规则" 继续并在 `step2_summary.md` 标注缺失
4. 读取 HCI 密度策略文件：`overseas_pipeline/strategies/hci_density_strategy.md`
   - 根据 `hci_density.strategy` 确定点名优先级和课程匹配顺序
5. 爬取职位 JD 原文：
   - `python overseas_pipeline/src/faculty_scraper.py --url "{job_url}" --output-type raw`
   - 或请用户提供 JD 文本
   - 保存到 `output/{school_id}/{dept_id}/raw/jd_*.md`
6. 读取 Sophia 全套材料：
   - `overseas_pipeline/materials/Research_Statement.md`
   - `overseas_pipeline/materials/Teaching_Statement.md`
   - `overseas_pipeline/materials/cv_latest.md`
   - `overseas_pipeline/materials/Impact_Statement.md`（如存在）
7. **⚠ 规则冲突检查（关键）**：
   - 比较 JD 要求与地区规则卡的规则
   - 如发现冲突，**立即暂停**，显示冲突详情和处理选项（见下）
8. 生成 `output/{school_id}/{dept_id}/fit_report.md`（见格式规范）
9. 生成 `output/{school_id}/{dept_id}/fit_report.sources.md`

---

## fit_report.md 格式

```markdown
# {学校} {院系} -- 匹配分析报告

## 基本信息
- 院系：
- 地区 / 规则卡：{region} / `region_knowledge/regions/{region}.md`
- 职级：
- 职位类型：TT / NTT / Teaching-track（影响 CV 变体选择）
- Deadline：
- 薪资：
- 职位链接：

## Fit Score: X/10

## 各维度评分

| 维度 | 评分 | 说明 |
|------|------|------|
| 研究方向匹配 | X/10 | |
| 教学匹配 | X/10 | |
| 区域适配 | X/10 | |
| 职位类型适配 | X/10 | |
| HCI 密度策略 | X/10 | `{strategy}` |

## 匹配维度分析

### 研究方向匹配 (X/10)
...

### 教学匹配 (X/10)
...

### 区域适配 (X/10)
...

### HCI 密度策略分析 (`{strategy}`)

- 目标系 HCI 密度：{level}（{count} 人）
- 学院 HCI 密度：{level}（{count} 人）
- 推荐策略：`{strategy}`
- 策略要点：
  - 对目标系评委：{具体修辞建议}
  - 点名优先级：{目标系教授} → {跨系补充（如有）}

### 关键决策人分析（材料写给谁看）

| 阶段 | 决策人 | 看什么 |
|------|--------|--------|
| 初筛 | 搜寻委员会 | ... |
| 面试 | ... | ... |
| 最终 | 系主任 | ... |

### 各材料调整建议

#### Cover Letter
- **密度策略** [`{strategy}`]：{具体修辞建议}
- **点名建议**：
  - 目标系（优先）：{教授 + 合作点}
  - 跨系补充（如需）：{教授 + 合作点}
- 其他定制点：...

#### Research Statement / Research Interests
- **密度策略** [`{strategy}`]：{硬化/愿景化程度}
- 具体修改点：...

#### Teaching Statement
- **密度策略** [`{strategy}`]：{课程呈现顺序}
- **课程匹配**（来自 department_courses）：
  - 可教现有课：{课程代码 + 名称}
  - 可开新课：{名称}
- 其他修改点：...

#### Diversity Statement
- 是否需要提交：{是 / 否（JD 未要求）}
- 如需提交：页数要求 {1p / 2p / 未指定} → 使用 `{DEI-structured-1p / DEI-structured-2p}`
- 定制方向：{提及该校具体 diversity 项目或学生构成}

#### CV
- 变体选择：`{base / ntt / metrics-first / cv-analytique / dach}`（见 workflows/cv_strategy.md）
- 触发原因：{职位类型 NTT / 地区 Italy 等}
- 如为 `base`：直接提交，无需修改

#### Selection Criteria Response（如为澳洲职位）
...（逐条列出 criterion + 回应框架）

### 规则冲突记录

| 冲突项 | 规则卡规定 | JD 要求 | 处理方式 |
|--------|-----------|---------|---------|
| ... | ... | ... | 以 JD 为准 |

### 风险提示
...

### 投递建议
- 是否建议投递：
- 优先级：my favorite / worth trying / low priority
- 理由：...
```

---

## 规则冲突处理流程

```
⚠ 发现规则冲突，暂停流水线。

【地区卡规则】{具体规则内容}（来源：{source URL}）
【JD 实际要求】{JD 中的具体要求}（来源：{job URL}）

请选择处理方式：
A. 以该校 JD 为准（本次），记录到学校卡
B. 以该校 JD 为准，同时标记地区卡 needs_review
C. 忽略冲突，仍按地区卡执行

请回复 A、B 或 C。
```
