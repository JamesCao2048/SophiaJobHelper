# Monash University 知识卡

## 元信息
- school_id: monash_university
- region: australia  ← 继承自 `regions/australia.md`
- created: 2026-02-19
- last_updated: 2026-02-19
- status: draft（来自 overseas_pipeline Step 1 首次生成）

---

## 1. 基本信息

| 项目 | 内容 |
|------|------|
| 全称 | Monash University |
| 目标院系 | Department of Data Science and AI (DSAI) |
| 次级相关院系 | Department of Human Centred Computing (HCC) |
| 院系主页（DSAI）| https://www.monash.edu/it/dsai |
| 院系主页（HCC）| https://www.monash.edu/it/hcc |
| 招聘页 | https://www.monash.edu/jobs |
| 地点 | Clayton Campus, Melbourne, Victoria, Australia |
| QS CS 排名 | ~60-80 全球（估计，未直接验证）|
| Monash AI Institute | https://www.monash.edu/ai-institute |
| HCC 全球排名 | #10（CHI 论文数，WebSearch 2026-02-19）|

---

## 2. 关键决策人

### 2026 年 Agentic AI 职位（Job Ref: 688354）

| 角色 | 姓名 | 研究方向 | 联系邮件 | 主页 |
|------|------|---------|---------|------|
| 联系人 / 招聘委员会成员 | Associate Professor Markus Wagner | 优化算法、算法设计、软件工程应用 | markus.wagner@monash.edu | https://research.monash.edu/en/persons/markus-wagner/ |

### HCC 院系（潜在合作人）

| 姓名 | 职称 | 研究方向 | 主页 |
|------|------|---------|------|
| Sharon Oviatt | Professor | Multimodal interfaces, human-centered AI, educational interfaces | https://research.monash.edu/en/persons/sharon-oviatt/ |
| Joe Liu (Jiazhou Liu) | Lecturer | Human-AI interaction, immersive analytics, spatial cognition | https://research.monash.edu/en/persons/joe-liu/ |
| Matthew Butler | Associate Professor | Accessibility, conversational agents, data visualization | https://research.monash.edu/en/persons/matthew-butler/ |

### DSAI 院系

| 姓名 | 职称 | 研究方向 | 主页 |
|------|------|---------|------|
| Gholamreza (Reza) Haffari | Professor | NLP, Machine Translation, Vision and Language | https://research.monash.edu/en/persons/reza-haffari/ |
| Hamid Rezatofighi | Associate Professor | Computer vision, human activity recognition, robotics | https://research.monash.edu/en/persons/hamid-rezatofighi/ |

---

## 3. 与地区卡的差异（覆盖规则）

覆盖 `australia.md` 的以下规则：

| 规则 | 地区卡默认 | Monash 特有 |
|------|-----------|-----------|
| 合同类型 | 通常 Continuing（永久制）| Agentic AI 职位（688354）为 **3 年 Fixed-term** |
| 院系结构 | 通用描述 | Monash IT 下设 DSAI + HCC 两个独立院系；Sophia 投 DSAI 但 HCC 是更自然的 fit |
| HCI 认可度 | CHI/CSCW 在澳洲 HCI 社区认可 | Monash HCC 全球 #10，CHI 认可度极高 |

---

## 4. HCI Group 信息（来自 overseas_pipeline Step 1）

**DSAI 院系的 HCI 情况：**
- DSAI 主要聚焦 AI/ML/数据科学，没有独立的 HCI group
- Markus Wagner（联系人）研究方向为优化算法，非 HCI

**HCC 院系的 HCI 情况（更自然的归属）：**
- 全球排名 #10（CHI 论文数）
- 主要研究组：Computer Human Interaction & Creativity (CHIC)
- 现有 127+ 研究人员
- 与 Sophia 研究最接近的 faculty：
  - Joe Liu（human-AI interaction，直接 overlap）
  - Sharon Oviatt（human-centered AI，深度 HCI）
  - Matthew Butler（conversational agents，中等 overlap）

---

## 5. 课程信息（Teaching Statement 定制用）

来自 Monash handbook（需验证具体年份）：

| 课程代码 | 课程名 | 与 Sophia 教学能力匹配 |
|---------|--------|---------------------|
| FIT3063 | Human-Computer Interaction | 直接匹配，可作为 TA 或共同授课 |
| FIT3080 | Artificial Intelligence | 可作为 Human-AI Collaboration 课程的上游 |
| FIT1059 | AI for Everyone | 可作为 Sophia 新课程的入门补充 |
| FIT3094 | AI Planning (待验证) | 如果存在，与 Agentic AI 相关 |

**Sophia 可开设的新课（未被现有课程覆盖）：**
- Human-AI Collaboration and Interaction（研究生+高年级本科生）
- Computational Qualitative Analysis（研究生）

---

## 6. 申请历史

**2026 年 02 月 19 日：**
- overseas_pipeline Step 1-3 完成
- 投递职位：Lecturer in Agentic AI (Level B), Ref 688354
- Deadline: 2026-03-02 11:55pm AEDT
- 生成材料：
  - Cover Letter (cover_letter.tex)
  - Research Statement (research_statement.md)
  - Teaching Statement (teaching_statement.md)
  - Selection Criteria Response (selection_criteria_response.md, ~8 页)
- Fit Score: 6.5/10（值得一试）
- 材料位置：`overseas_pipeline/output/monash_university/materials/`

---

## 7. 已知注意事项

1. **DECRA 时间窗口紧迫**：ARC DECRA 2027 截止 2026-03-11，需立即确认是否能以 Monash 名义申请（可能需要已获 offer 才能通过 Monash 提交）
2. **Monash 主站 Cloudflare 保护**：后续需要更多 faculty 信息时，手动访问比自动爬取更可靠
3. **HCC vs DSAI 定位**：如果 HCC 后续有职位开放，对 Sophia 的匹配度会更高（8-9/10）
