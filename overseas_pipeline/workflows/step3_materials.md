# Step 3: Materials Generation（生成材料）

## 前提

Step 2 已完成（`output/{school_id}/{dept_id}/fit_report.md` 存在）

---

## 资源分工

Step 3 使用两类资源，分工明确：

### 格式模板（`templates/`）

独立可编译的 LaTeX 项目，Caramel 配色（匹配 CV_latest），Step 3 以此为起点复制到 `output/`：

| 路径 | 对应材料 | 目标页数 |
|------|---------|---------|
| `templates/cover_letter/` | Cover Letter | **2 页** |
| `templates/research_statement/` | Research Statement | **4 页 TT / 2-3 页 NTT** |
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

1. 读取 `output/{school_id}/{dept_id}/fit_report.md` 中的"各材料调整建议"和页数要求（含 JD 覆盖值）
2. 读取 Sophia 现有材料（`overseas_pipeline/materials/*.md`）
3. 读取区域规则卡（`../region_knowledge/regions/{region}.md`）
4. 读取 `strategies/hci_density_strategy.md`
   - 从 `faculty_data.json` 获取 `hci_density.strategy` 和 `department_courses`
5. 读取内容来源 LaTeX 源文件（见"内容来源"表格）
6. 为每份材料生成初稿 + notes（**Step 3a**）
7. Humanizer 处理（**Step 3a 收尾**，强制）
8. 复制格式模板 + 填入内容 + 编译 PDF + 验证页数（**Step 3b**）
9. 同校多系一致性检查（如 `related_applications` 字段存在）

---

## Step 3a: 生成内容

### Cover Letter

- **格式模板**：`templates/cover_letter/`（Caramel 配色 OUCletter.cls）
- **内容来源**：该校专属版（`overleaf-projects/Cover Letter/Cover Letter- {学校名}/`，如存在）优先；否则以模板结构为基础全新撰写
- 基于 fit_report 建议定制，按 HCI 密度策略调整修辞
- **目标页数**：**2 页**（如 fit_report 中有 JD 覆盖值，以 JD 为准）
- **OUCletter.cls 注意：** cls 已自动渲染信息栏，**不要**添加 tikz overlay，否则重叠。只需定义 `\signature{\name}` 供 closing 使用。
- 同时生成 `cover_letter.notes.md`

### Research Statement / Research Interests

- **格式模板**：`templates/research_statement/main.tex`（Caramel 配色，pdflatex 编译）
- **内容来源**：`overleaf-projects/Faculty Position/Research Statement/Research Statement/main.tex`（读取各 section 真实内容）
- TT 岗：完整版（**目标 4 页**），加 ARC/NSF/EPSRC 等对应地区的 grant 计划
- NTT 岗：压缩为 Research Interests（**目标 2-3 页**），删 grant 蓝图，加 Research-Teaching Connection 章节
- **如 fit_report 有 JD 覆盖值，以 JD 页数为准**
- 同时生成 `research_statement.notes.md`

### Teaching Statement

- **格式模板**：`templates/teaching_statement/main.tex`（Caramel 配色，pdflatex 编译）
- **内容来源**：`overleaf-projects/Faculty Position/Teaching Statement/Teaching Statement/Teaching_Statement.tex`
- **目标页数**：**2 页**（NTT 可扩展至 2.5 页；如 fit_report 有 JD 覆盖值，以 JD 为准）
- 修改点：补充该校课程编号（来自 `department_courses`）、加量化数据、按密度策略调整课程顺序
- 澳洲：加 40/40/20 声明
- NTT：Teaching Statement 是核心材料，扩充 advising 描述
- 同时生成 `teaching_statement.notes.md`

### Diversity Statement（按需）

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

### CV（按需定制）

**判断流程：**
1. 读取 fit_report.md 中的"CV 变体选择"建议
2. 查阅 `workflows/cv_strategy.md` 确认变体操作步骤
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

### Selection Criteria Response（仅澳洲职位）

- **格式模板**：`templates/selection_criteria_response/main.tex`（Caramel 配色，与所有 Statement 一致）
- 从 JD 中提取所有 Essential 和 Desirable criteria，逐条回应
- 格式：逐条用 STAR 法则回应（Situation → Task → Action → Result）
- 长度：6-10 页（按 criteria 数量决定，无固定上限）
- **这是澳洲申请的核心文件，不提交直接出局**
- 同时生成 `selection_criteria_response.notes.md`

---

## Step 3a 收尾：Humanizer 处理（强制）

**REQUIRED SKILL: 在写入 .tex 文件之前，对所有新增/修改的英文正文使用 `humanizer` skill。**

处理范围：
- Cover Letter 所有段落
- Research Statement/Interests 新增/修改段落（原文保留的无需重处理）
- Teaching Statement 新增/修改段落
- Diversity Statement content.tex 中的修改部分
- Selection Criteria Response 所有 STAR 段落

不处理范围：LaTeX 命令/环境声明、参考文献、课程代码、人名、数字/统计数据

**Humanizer 检查清单（写入 .tex 前必须全部确认）：**
- [ ] 无 "pivotal / crucial / underscore / showcase / delve / landscape / testament / fostering" 等 AI 高频词
- [ ] 无 "serves as / stands as / marks a / represents a" 等 copula 替代结构（改用 "is/are"）
- [ ] 无 "Not only...but also..." / "It's not just...it's..." 负向并行结构
- [ ] Em dash（—）每份材料不超过 2 处
- [ ] 无模糊引用（"Experts argue / Industry reports" 等）
- [ ] 无假深度 -ing 结尾（"highlights / underscores / reflecting"）
- [ ] 无过度 hedging（"could potentially / might arguably"）
- [ ] 无对话残留（"I hope this helps / let me know"）
- [ ] 结尾段有具体内容，非泛泛 "I look forward to..."
- [ ] 句子长度有变化（非全是同等长度的复合句）
- [ ] **【仅 NZ 职位】Te Tiriti 段落诚实度：**
  - [ ] 无伪装成已有毛利社区合作经验的表述（如 "I have worked with iwi..."）
  - [ ] Aspire 部分有具体学习计划，非空洞的 "I am committed to learning"
  - [ ] 如引用了其他文化的平行经验，后面有"Te Tiriti 独特性"声明
  - [ ] 未把 Sophia 的参与式设计/trustworthy AI 工作夸大为"Data Sovereignty 实践"

---

## Step 3b: 复制模板 + 填入内容 + 编译 PDF + 验证页数

**执行流程：**

1. 从 `templates/{doc_type}/` 复制完整 LaTeX 项目到 `output/{school_id}/{dept_id}/materials/{材料名}/`
2. 用 Step 3a 生成的 .tex 内容**替换**复制后目录中对应的 .tex 文件
3. 将 `templates/sophia-statement.sty` 复制到各材料目录（或用相对路径 `../../sophia-statement.sty` 引用）
4. 编译 PDF：

   | 材料 | 编译器 | 命令 |
   |------|--------|------|
   | Cover Letter | xelatex | `xelatex main_template.tex && xelatex main_template.tex` |
   | Research Statement | pdflatex | `pdflatex main.tex && pdflatex main.tex` |
   | Teaching Statement | pdflatex | `pdflatex main.tex && pdflatex main.tex` |
   | Diversity Statement | pdflatex | `pdflatex main.tex && pdflatex main.tex` |
   | CV | xelatex | `xelatex main.tex && xelatex main.tex` |
   | Selection Criteria | pdflatex | `pdflatex main.tex && pdflatex main.tex` |

5. **⚠ 页数验证（编译成功后必须执行）：**

   用 `pdfinfo` 获取实际页数：
   ```bash
   pdfinfo output.pdf | grep Pages
   # 或
   python3 -c "import subprocess; r=subprocess.run(['pdfinfo','main.pdf'],capture_output=True,text=True); print([l for l in r.stdout.splitlines() if 'Pages' in l])"
   ```

   | 材料 | 目标 | 超出处理 | 明显不足处理 |
   |------|------|---------|------------|
   | Cover Letter | 2 页 | 精简段落，优先删 Service 段细节 | < 1.5 页：提示补充 Fit 段 |
   | Research Statement | 4 页（TT）| 精简 Background 铺垫，删次要 subsection | < 3 页：提示补充 Future Plans |
   | Teaching Statement | 2 页 | 精简 Mentorship 或 Course list | < 1.5 页：提示补充 |
   | Diversity Statement | 1 页（默认）| 精简 Service 段；若 2 页目标则精简 Plans | < 0.8 页：提示补充 |
   | Selection Criteria | 无固定 | 不触发，按 criteria 数量自然延伸 | — |

   **超出处理优先级（精简顺序）：**
   1. 删除或缩短"背景铺垫"段（读者已知的领域常识）
   2. 合并相似 subsection
   3. 缩短 Future Plans（保留 2-3 句而非完整段落）
   4. 压缩 Service/Outreach 段到 1-2 句
   5. 如仍超出：在 step3_summary.md 标注 `⚠ 页数超出，Sophia 需进一步精简`

   **明显不足判断标准**：实际页数 < 目标页数 × 0.75（如目标 4 页但只有 3 页以下）

---

## notes.md 格式（强制，不可简化）

notes.md 是给 Sophia 审核的"修改日志"，必须让她无需打开 .tex 文件就能理解所有修改。

```markdown
# {材料名} 修改说明 -- {学校}

## 生成日期

## 总体策略
<!-- 2-3 句话说明整体定制方向和关键定位决策 -->

## 参考资料清单
| # | 类型 | 资料 | 链接/路径 |
|---|------|------|-----------|
| R1 | 区域规则卡 | {地区}规则卡 Section X（行号）| region_knowledge/regions/{region}.md L58-138 |
| R2 | Fit Report | 匹配分析 | output/{school}/{dept}/fit_report.md |
| R3 | Sophia 材料 | Research Statement | overseas_pipeline/materials/Research_Statement.md |
<!-- 必须标注具体章节/行号 -->

## 逐段修改说明

### 1. {段落标识} [NEW / MODIFIED / UNCHANGED]
**原文：** > 引用原始文本（新增标注"无对应原文"）
**修改为：** > 引用修改后的关键句子
**原因：**
- 引用 [R1: 具体章节/行号] ...

### N. 未修改部分
<!-- 必须列出所有未修改的主要段落，说明保留原因 -->

## 样式说明与 Debug 记录
<!-- 编译器选择、字体、编译问题修复 -->

## 给 Sophia 的审核重点
<!-- 3-5 条具体可操作的审核项，非泛泛"请审核" -->
```

**notes.md 质量自检（Step 3 完成前）：**
- [ ] 每个修改段落都有原文 vs 修改的对比
- [ ] 每个修改原因都引用了具体参考资料编号和章节
- [ ] 未修改的部分也有说明（为什么保留）
- [ ] 有编译/样式说明
- [ ] "给 Sophia 的审核重点"包含具体可操作的审核项

---

## 同校多系一致性检查

如 `related_applications` 字段存在，在每份 notes.md 末尾追加：

```markdown
## 同校多系一致性检查
- 本校另一份申请：{department}（{strategy} 策略）
- 核心叙事一致性：✅/⚠ {说明}
- 侧重点差异：本系版（{简述}）vs 另一系版（{简述}）
- ⚠ 注意：{具体提醒}
```

---

## 产出物清单（step3_summary.md 记录）

```
materials/
├── Cover Letter/
│   ├── main.tex / main.pdf          ✅/❌
│   └── cover_letter.notes.md
├── Research Statement/              ✅/❌（或 Research Interests/）
│   ├── main.tex / main.pdf
│   └── research_statement.notes.md
├── Teaching Statement/              ✅/❌
│   ├── Teaching_Statement.tex / .pdf
│   └── teaching_statement.notes.md
├── Diversity Statement/             ✅/❌/不提交（JD 未要求）
│   ├── main.tex / main.pdf
│   └── diversity_statement.notes.md
├── CV/                              ✅/❌/直接复制（base 变体）
│   ├── main.tex / main.pdf
│   └── cv.notes.md
└── Selection Criteria Response/     ✅/❌/不适用（非澳洲）
    ├── selection_criteria_response.tex / .pdf
    └── selection_criteria_response.notes.md
```
