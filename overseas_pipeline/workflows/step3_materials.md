# Step 3: Materials Generation（生成材料）

## 前提

Step 2 已完成（`output/{school_id}/{dept_id}/fit_report.md` 存在）

---

## 资源分工

### 格式模板（`templates/`）

独立可编译的 LaTeX 项目，Caramel 配色（匹配 CV_latest），Step 3 以此为起点复制到 `output/`：

| 路径 | 对应材料 | 目标页数 |
|------|---------|---------|
| `templates/cover_letter/` | Cover Letter | **2 页** |
| `templates/research_statement/` | Research Statement | **5 页 TT / 2-3 页 NTT** |
| `templates/teaching_statement/` | Teaching Statement | **2 页** |
| `templates/diversity_statement/` | Diversity Statement | **1 页（可扩展至 2 页）** |
| `templates/selection_criteria_response/` | Selection Criteria | 按 criteria 数量（6-10 页） |

**页数默认值**：以上为 JD 未指定时的强制默认值。如 fit_report.md 中有 `⚠ JD 明确要求` 标注，以 JD 要求为准。

### 内容来源（`overleaf-projects/Faculty Position/`）

Sophia 现有的真实申请材料文本，Step 3 从这里提取内容填入模板：

| 目录 | 用途 |
|------|------|
| `Cover Letter/Cover Letter- {学校名}/` | 该校已有 Cover Letter（优先使用，作为内容基础） |
| `Research Statement/Research Statement/main.tex` | Research Statement 完整版文本（含图） |
| `Teaching Statement/Teaching Statement/Teaching_Statement.tex` | Teaching Statement 文本 |
| `DEI-structured-1p/content.tex` | DEI 1 页版内容文本 |
| `DEI-structured-2p/content.tex` | DEI 2 页版内容文本 |
| `CV_latest/CV_latest/` | CV 模块化 LaTeX 源 |

---

## 执行步骤

### 1. 加载匹配报告与页数要求

读取 `output/{school_id}/{dept_id}/fit_report.md` 中的"各材料调整建议"和页数要求（含 JD 覆盖值）
- **NZ 职位**：明确记录 fit_report 中 Te Tiriti 专节对每个文档的建议（Cover Letter / Research Statement / Teaching Statement）
- **AU 职位**：明确记录 fit_report 中 AU Indigenous 专节对每个文档的建议（Cover Letter / Research Statement / Teaching Statement / KSC Response）

### 2. 加载 Sophia 现有材料

读取 `overseas_pipeline/materials/*.md`

### 3. 加载区域规则卡

读取 `../region_knowledge/regions/{region}.md`

### 4. 加载策略文件

两者都必须读取：
- `strategies/dept_type_strategy.md`（**优先**）
  - 从 `dept_data.json` 获取 `dept_profile.dimensions`（QR / IO / SB / SI）
  - 从 `fit_report.md` 的"院系类型策略分析"节确认：技术伪装程度、主推论文、经费叙事、术语体系
- `strategies/hci_density_strategy.md`
  - 从 `dept_data.json` 获取 `hci_density.strategy` 和 `teaching_context`
  - 确认点名优先级和课程匹配顺序

### 5. 加载 LaTeX 内容来源

读取内容来源 LaTeX 源文件（见"内容来源"表格）

### 6. 各材料初稿生成

**NZ/AU 职位**：生成每个文档时，必须**显式检查** fit_report 中对应文档的 Te Tiriti / AU Indigenous 建议是否已执行。

#### Cover Letter

- **格式模板**：`templates/cover_letter/`（Caramel 配色 OUCletter.cls）
- **内容来源**：该校专属版（`overleaf-projects/Cover Letter/Cover Letter- {学校名}/`，如存在）优先；否则以模板结构为基础全新撰写
- **修辞基调（由 dept_type_strategy 驱动）**：
  - QR=high → 技术语言为主，系统/算法贡献放首位，用户研究作为"科学验证"而非核心贡献
  - QR=medium → 技术为主，定性洞察作为设计决策依据（三段式：定性洞察→系统设计→量化评估）
  - QR=low → 可直接呈现定性方法，强调社会影响和应用价值
- **跨学院合作段落（IO 驱动）**：
  - IO=high → 必须包含跨学院合作段落，点名潜在合作院系和教授，说明具体协作角度
  - IO=medium → 若 JD 有跨学科信号则加入，否则可省略
  - IO=low → 不需要跨学院叙述
- **院系战略对齐**（参照 fit_report 院系战略对齐节）：加入 1-2 句与目标院系/学校最新战略方向的对齐叙述
- **点名结构**（由 hci_density 驱动）：按 fit_report 点名建议排序
- **经费叙事**（参照 dept_type_strategy.md §五）：在 research vision 段落末尾自然融入
- **目标页数**：**2 页**（如 fit_report 中有 JD 覆盖值，以 JD 为准）
- **OUCletter.cls 注意：** cls 已自动渲染信息栏，**不要**添加 tikz overlay，否则重叠。只需定义 `\signature{\name}` 供 closing 使用。
- 同时生成 `cover_letter.notes.md`（格式见 `references/notes_and_output_spec.md`）

#### Research Statement / Research Interests

- **格式模板**：`templates/research_statement/main.tex`（Caramel 配色，pdflatex 编译）
- **内容来源**：`overleaf-projects/Faculty Position/Research Statement/Research Statement/main.tex`（读取各 section 真实内容）
- TT 岗：完整版（**目标 5 页**），加 ARC/NSF/EPSRC 等对应地区的 grant 计划
- NTT 岗：压缩为 Research Interests（**目标 2-3 页**），删 grant 蓝图，加 Research-Teaching Connection 章节
- **如 fit_report 有 JD 覆盖值，以 JD 页数为准**
- **技术伪装处理（由 dept_type_strategy 驱动）**：
  - QR=high → 系统架构 > 用户引语；"硬化"处理：加算法/模型/系统贡献段落，量化指标（准确率/效率提升）优先
  - QR=medium → 三段式叙述：定性洞察（formative study）→ 系统设计决策 → 量化评估结果
  - QR=low → 直接呈现定性方法，清晰解释 formative study 的科学性，与系统贡献并举（V5 原则：不伪装，但框定）
- **主推论文顺序**（参照 fit_report 主推论文节 + dept_type_strategy.md §四）：
  - TOCHI 论文在所有类型院系均为首推（体现 HCI 的系统性贡献）
  - 根据 QR/SB 等级调整 P2、P3 顺序
- **院系战略对齐段落（Future Work 节）**：
  - 参照 `dept_data.json → strategic_intelligence.clusters`，在 Future Work/Research Vision 节加入与目标院系最相关 cluster 的战略方向对齐（1-2 句）
  - SB=high → 强调系统基础设施和工具贡献方向
  - SI=high → 强调社会影响、政策影响、应用落地方向
- 同时生成 `research_statement.notes.md`

#### Teaching Statement

- **格式模板**：`templates/teaching_statement/main.tex`（Caramel 配色，pdflatex 编译）
- **内容来源**：`overleaf-projects/Faculty Position/Teaching Statement/Teaching Statement/Teaching_Statement.tex`
- **目标页数**：**2 页**（NTT 可扩展至 2.5 页；如 fit_report 有 JD 覆盖值，以 JD 为准）
- **课程顺序（由 hci_density_strategy 驱动）**：
  - pioneer 系列（QR=high）→ CS 核心课（数据结构/软工/算法）在前，HCI 课作为"可开设新课"在后
  - builder 系列 → 互补课程在前（填补 HCI Track 缺口），列课程编号（来自 `department_courses`）
  - specialist → 高阶/研究生 HCI 课在前，工作室教学法/PBL 理念突出
- **院系特色课程**（来自 `dept_data.json → teaching_context.department_courses`）：将 `sophia_can_teach: true` 的课程按以上优先级顺序提及（列课程编号）
- **博士指导理念**（specialist 时必须包含 / builder 时建议包含）：说明如何培育未来研究者
- 澳洲：加 40/40/20 声明
- NTT：Teaching Statement 是核心材料，扩充 advising 描述
- 同时生成 `teaching_statement.notes.md`

#### Diversity Statement（按需）

**触发条件：** JD 明确要求提交

若 JD 要求：
1. 检查 fit_report.md 中的页数要求
2. **格式模板**：`templates/diversity_statement/main.tex`（Caramel 配色，pdflatex 编译）
3. **内容来源**：
   - 默认（1 页）：`overleaf-projects/Faculty Position/DEI-structured-1p/content.tex`
   - 2 页时：`overleaf-projects/Faculty Position/DEI-structured-2p/content.tex`
4. **目标页数**：**1 页**（默认）；JD 明确要求 2 页 → 使用 2 页内容，取消 `\section{Plans}` 注释
   - 如 fit_report 有 JD 覆盖值，以 JD 页数为准
5. 定制内容（通常只需微调）：
   - 在 Plans 部分提及该校具体 diversity 项目/学生构成（如知道）
   - 替换学校名称引用（如有）
6. 输出到 `materials/Diversity Statement/`
7. 同时生成 `diversity_statement.notes.md`

若 JD 不要求：在 step3_summary.md 中标注"不提交（JD 未要求）"，**不生成文件**。

**地区默认期望：**

| 地区 | 期望 |
|------|------|
| USA TT | 约 60% 的职位要求，如 JD 无要求也可主动提交（见地区卡） |
| Canada | 几乎所有 TT 职位必须，且有 EDI Statement 专项要求 |
| Australia | JD 要求时提交，否则不主动 |
| UK / Europe | 较少要求，有时合并在 Cover Letter 中 |

#### CV（按需定制）

**判断流程：**
1. 读取 fit_report.md 中的"CV 变体选择"建议
2. 查阅 `strategies/cv_strategy.md` 确认变体操作步骤
3. 执行定制：

| 变体 | 操作 |
|------|------|
| `base` | 从 `CV_latest/CV_latest/` 复制到 `materials/CV/`，**不修改**，直接编译 |
| `ntt` | 复制后修改 `main.tex` 中的 `\input` 顺序（Teaching + Mentoring 提前），在 interests 段末加教学转化句 |
| `metrics-first` | 复制后在 Education 前插入 Bibliometrics 摘要表（LaTeX tabular） |
| `cv-analytique` | ⚠ 不自动生成，在 step3_summary.md 中提示 Sophia 手动准备 |
| `dach` | ⚠ 不自动生成，提示 Sophia 补充个人信息和 Habilitation 叙事 |

4. 编译：`xelatex main.tex && xelatex main.tex`
5. 同时生成 `cv.notes.md`（记录变体类型、修改的节顺序、Bibliometrics 数据来源）

**注意：** 几乎所有申请都需要 CV，`base` 变体无需每次修改，直接在材料目录中放一份编译好的 PDF 即可（可从 `CV_latest/CV_latest/main.pdf` 直接复制）。只有当变体≠base 时才需要重新定制编译。

#### Selection Criteria Response（仅澳洲职位）

- **格式模板**：`templates/selection_criteria_response/main.tex`（Caramel 配色，与所有 Statement 一致）
- 从 JD 中提取所有 Essential 和 Desirable criteria，逐条回应
- 格式：逐条用 STAR 法则回应（Situation → Task → Action → Result）
- 长度：6-10 页（按 criteria 数量决定，无固定上限）
- **这是澳洲申请的核心文件，不提交直接出局**
- 同时生成 `selection_criteria_response.notes.md`

### 7. Humanizer 去 AI 化处理（强制）

**REQUIRED SKILL: 在写入 .tex 文件之前，对所有新增/修改的英文正文使用 `humanizer` skill。**

完整检查清单见 `references/humanizer_checklist.md`。

**⚠ 顺序强制：Humanizer 必须在编译和页数压缩之前完成。** 不可先编译再做 humanizer——humanizer 修改可能改变文本量，导致页数验证结论失效。

**并行化：** 多份材料（CL / RS / TS）可同时启动 subagent 并行检查，每个 subagent 负责一份材料的 humanizer 审核。所有材料通过后再统一进入编译阶段。

### 8. 编译 PDF 与页数验证

**执行顺序（严格按此顺序）：**

1. Humanizer 检查全部通过（step 7）
2. 从 `templates/{doc_type}/` 复制完整 LaTeX 项目到 `output/{school_id}/{dept_id}/materials/{材料名}/`
3. 用 step 6 生成的 .tex 内容**替换**复制后目录中对应的 .tex 文件
4. 将 `templates/sophia-statement.sty` 复制到各材料目录（或用相对路径 `../../sophia-statement.sty` 引用）
5. 编译 PDF（各材料可并行执行）：

   | 材料 | 编译器 | 命令 |
   |------|--------|------|
   | Cover Letter | xelatex | `xelatex main_template.tex && xelatex main_template.tex` |
   | Research Statement | pdflatex | `pdflatex main.tex && pdflatex main.tex` |
   | Teaching Statement | pdflatex | `pdflatex main.tex && pdflatex main.tex` |
   | Diversity Statement | pdflatex | `pdflatex main.tex && pdflatex main.tex` |
   | CV | xelatex | `xelatex main.tex && xelatex main.tex` |
   | Selection Criteria | pdflatex | `pdflatex main.tex && pdflatex main.tex` |

6. **⚠ 页数验证（编译成功后必须执行）**：完整 PDF 微调策略见 `references/pdf_tuning_guide.md`

### 9. 同校多系一致性检查

如 `related_applications` 字段存在，执行一致性检查。完整格式见 `references/notes_and_output_spec.md`。

---

## 产出物清单

完整产出物清单格式见 `references/notes_and_output_spec.md`。

## notes.md 格式

完整 notes.md 格式规范见 `references/notes_and_output_spec.md`。
