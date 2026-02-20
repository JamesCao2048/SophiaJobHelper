# Step 3: Materials Generation（生成材料）

## 前提

Step 2 已完成（`output/{school_id}/{dept_id}/fit_report.md` 存在）

---

## 可用材料库（overseas_pipeline/overleaf-projects/Faculty Position/）

| 目录 | 用途 | 备注 |
|------|------|------|
| `Cover Letter/Cover Letter- {学校名}/` | 该校 Cover Letter（如已有） | 若不存在，用模板 |
| `Research Statement/Research Statement/` | Research Statement 完整版 | 含图片 |
| `Teaching Statement/Teaching Statement/` | Teaching Statement | 含 Zhiyao/Erika/Ruyuan 故事 |
| `DEI-structured-1p/` | Diversity Statement 1 页版 | **管道默认 DEI** |
| `DEI-structured-2p/` | Diversity Statement 2 页版 | JD 要求 2p 时使用 |
| `DEI-prose-2p/` | DEI 散文叙事版（旧版，备用） | 内容角度不同，酌情参考 |
| `CV_latest/CV_latest/` | CV 模块化 LaTeX 源 | Step 3 按需定制 |
| `templates/cover_letter/` | Cover Letter 模板 | 该校无专属版时使用 |

---

## 执行步骤

1. 读取 `output/{school_id}/{dept_id}/fit_report.md` 中的"各材料调整建议"
2. 读取 Sophia 现有材料（`overseas_pipeline/materials/*.md`）
3. 读取区域规则卡（`region_knowledge/regions/{region}.md`）
4. 读取 `overseas_pipeline/strategies/hci_density_strategy.md`
   - 从 `faculty_data.json` 获取 `hci_density.strategy` 和 `department_courses`
5. 读取 overleaf 原始 LaTeX 源文件（见可用材料库）
6. 为每份材料生成初稿 + notes（**Step 3a**）
7. Humanizer 处理（**Step 3a 收尾**，强制）
8. 复制 overleaf 项目 + 替换内容 + 编译 PDF（**Step 3b**）
9. 同校多系一致性检查（如 `related_applications` 字段存在）

---

## Step 3a: 生成内容

### Cover Letter

- 来源：该校专属版（如存在）或 `templates/cover_letter/main_template.tex`
- 基于 fit_report 建议定制，按 HCI 密度策略调整修辞
- 长度：1-2 页
- **OUCletter.cls 注意：** cls 已自动渲染信息栏，**不要**添加 tikz overlay，否则重叠。只需定义 `\signature{\name}` 供 closing 使用。
- 同时生成 `cover_letter.notes.md`

### Research Statement / Research Interests

- 来源：`Research Statement/Research Statement/main.tex`（完整版含图）
- TT 岗：完整版，加 ARC/NSF/EPSRC 等对应地区的 grant 计划
- NTT 岗：压缩为 Research Interests（2-3 页），删 grant 蓝图，加 Research-Teaching Connection 章节
- 同时生成 `research_statement.notes.md`

### Teaching Statement

- 来源：`Teaching Statement/Teaching Statement/Teaching_Statement.tex`
- 修改点：补充该校课程编号（来自 `department_courses`）、加量化数据、按密度策略调整课程顺序
- 澳洲：加 40/40/20 声明
- NTT：Teaching Statement 是核心材料，扩充 advising 描述
- 同时生成 `teaching_statement.notes.md`

### Diversity Statement（按需）

**触发条件：** JD 明确要求提交

若 JD 要求：
1. 检查 fit_report.md 中的页数要求（1p / 2p / 未指定）
2. 选择基础版本：
   - 1 页 → `DEI-structured-1p/`
   - 2 页或未指定 → `DEI-structured-2p/`
3. 定制内容（通常只需微调）：
   - 在 Plans 部分提及该校具体 diversity 项目/学生构成（如知道）
   - 替换学校名称引用（如有）
4. 输出到 `materials/Diversity Statement/`（从对应 DEI 目录复制后替换 content.tex）
5. 编译：`pdflatex main.tex && pdflatex main.tex`
6. 同时生成 `diversity_statement.notes.md`

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

- 从 JD 中提取所有 Essential 和 Desirable criteria
- 全新生成 LaTeX 文件（使用与 Teaching Statement 一致的样式）
- 格式：逐条用 STAR 法则回应（Situation → Task → Action → Result）
- 长度：6-10 页
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

---

## Step 3b: 复制模板 + 编译 PDF

**执行流程：**

1. 从 `overseas_pipeline/overleaf-projects/Faculty Position/` 复制完整 LaTeX 项目到 `output/{school_id}/{dept_id}/materials/`
2. 用 Step 3a 生成的 .tex 内容**替换**复制后目录中对应的 .tex 文件
3. 检查样式一致性（preamble 包/颜色/页边距/字体）
4. 编译 PDF：

   | 材料 | 编译器 | 命令 |
   |------|--------|------|
   | Cover Letter | xelatex | `xelatex main.tex && xelatex main.tex` |
   | Research Statement | pdflatex | `pdflatex main.tex && pdflatex main.tex` |
   | Teaching Statement | pdflatex | `pdflatex Teaching_Statement.tex && pdflatex Teaching_Statement.tex` |
   | Diversity Statement | pdflatex | `pdflatex main.tex && pdflatex main.tex` |
   | CV | xelatex | `xelatex main.tex && xelatex main.tex` |
   | Selection Criteria | pdflatex | `pdflatex selection_criteria_response.tex && ...` |

5. 验证 PDF 生成成功，检查页数是否合理

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
