# Step 2: Fit Analysis（分析匹配度）

## 前提

Step 1 已完成（`output/{school_id}/{dept_id}/dept_data.json` 存在）

---

## 执行步骤

### 1. 加载院系数据

读取 `output/{school_id}/{dept_id}/dept_data.json`（含 `hci_density`、`teaching_context`、`dept_profile`、`strategic_intelligence`、`faculty_summary[]` 字段）

### 2. 加载地区与院系规则卡

- 确定 region → 读取 `region_knowledge/regions/{region}.md`
- 读取院系规则卡（用于覆盖地区卡差异）：
  - 主路径：`region_knowledge/schools/{school_id}/{dept_id}.md`
  - 副本路径：`output/{school_id}/{dept_id}/knowledge/{dept_id}.md`
  - 若主路径不存在但副本存在，读取副本并在 `step2_summary.md` 标注 "using_output_copy"
  - 若两者都不存在，按 "无院系覆盖规则" 继续并在 `step2_summary.md` 标注缺失

### 3. 加载策略文件

- `overseas_pipeline/strategies/dept_type_strategy.md`（所有地区，**优先读取**）
  - 根据 `dept_profile.dimensions` 确定技术伪装程度、术语体系、主推论文、经费叙事
  - 根据 `strategic_intelligence` 确定院系战略对齐方向
- `overseas_pipeline/strategies/hci_density_strategy.md`（所有地区）
  - 根据 `hci_density.strategy` 确定点名优先级和课程匹配顺序
  - **注意**：dept_type_strategy 决定"说什么"，hci_density 决定"说给谁/点谁名"
- `overseas_pipeline/strategies/nz_te_tiriti_strategy.md`（仅 region=new_zealand）
- `overseas_pipeline/strategies/au_indigenous_strategy.md`（仅 region=australia）

### 4. 加载 JD 原文

- 检查 `output/{school_id}/{dept_id}/raw/jd_main.md` 是否存在
- ✅ 存在：直接读取，继续
- ❌ 缺失（Step 1 未执行或爬取失败）：立即补救
  ```bash
  python overseas_pipeline/src/page_scraper.py \
    --url "{dept_data.json → job_posting.url}" --output-type raw \
    --output-dir output/{school_id}/{dept_id}/raw/
  ```
  脚本失败则用 `web-fetch-fallback` skill，最终失败则请用户粘贴 JD 文本

### 5. 提取页数要求

在 JD 原文中搜索页数相关关键词（大小写不敏感）：
- `"not exceeding"`, `"no more than"`, `"maximum"`, `"up to"`, `"limited to"`
- `"X pages"`, `"X-page"`, `"within X pages"`
- 常见组合：`"research statement of no more than 3 pages"`, `"2-page teaching statement"`

**默认页数（JD 未指定时使用）：**

| 材料 | 默认页数 |
|------|---------|
| Cover Letter | 2 页 |
| Research Statement | 5 页（TT），2-3 页（NTT） |
| Teaching Statement | 2 页 |
| Diversity Statement | 1 页（JD 要求 2 页时扩展） |
| Selection Criteria Response | 按 criteria 数量，通常 6-10 页 |

**如 JD 指定了与默认不同的页数要求：**
- 在 `fit_report.md` 各材料调整建议中标注：`⚠ JD 明确要求：X 页（覆盖默认 Y 页）`
- 在 `step2_summary.md` 顶部生成**页数偏差警示区块**（格式见 `references/step2_message_templates.md`）
- Step 3 优先使用 JD 要求的页数，不使用默认值

### 6. 加载论文数据与 Sophia 现有材料

**Faculty 数据加载**：从 `dept_data.json → faculty_summary[]` 获取 high/medium overlap 教授列表，然后读取对应的 `faculty/{slug}.json` 获取完整详情（`overlapping_papers`、`overlap_confidence`、`overlap_notes`、`research_background` 等）。

**论文读取优先级**（对每位 high/medium faculty 的 `faculty/{slug}.json → overlapping_papers[]`）：
- 有 `local_pdf` → 读取 PDF 全文进行精读分析
- 无 `local_pdf` 但有 `abstract` → 使用摘要进行分析（在 fit_report 注明"摘要分析，未读全文"）
- 两者都无 → 仅凭标题和 `relevance` 做推断，在 fit_report 标注置信度为 low

**overlap_confidence 降权规则**（读取 `faculty/{slug}.json → overlap_confidence` 字段）：
- `high`：正常权重；可在 Cover Letter 和 Research Statement 中明确点名
- `medium`：正常权重，但 fit_report 中注明"间接交集"；Cover Letter 点名时措辞保守
- `low`：该教授在 fit_report 中标注 ⚠（证据偏弱）；在合作段落中降权或不列入；
  同时检查 `overlap_notes` 是否有补救建议（如"DBLP 索引不全，建议参考 step1_summary"）
- 字段缺失（旧数据）：按 `overlap_with_sophia` 的值正常处理

**Sophia 现有材料：**
- `overseas_pipeline/materials/Research_Statement.md`
- `overseas_pipeline/materials/Teaching_Statement.md`
- `overseas_pipeline/materials/cv_latest.md`
- `overseas_pipeline/materials/Impact_Statement.md`（如存在）

### 7. 规则冲突检查（⚠ 关键）

- 比较 JD 要求与地区规则卡的规则
- 如发现冲突，**立即暂停**，显示冲突详情和处理选项（格式见 `references/step2_message_templates.md`）

### 8. NZ Te Tiriti 矩阵分析（条件：region=new_zealand）

a. 读取 `dept_data.json → te_tiriti` 块（Step 1 已填充的 jd_signal、school_signal、strategy）
b. 读取 Sophia 材料识别可 Claim 的经历锚点（`materials/Research_Statement.md`, `materials/Teaching_Statement.md`）
c. 确认/调整策略标签：
   - 如需调整，在 `strategy_rationale` 中记录理由
   - 典型上调：JD 是 `boilerplate` 但已知该校（Auckland/VUW）面试必考条约题 → 上调一级
   - 典型维持：school_signal=`strong` 但 JD 无任何条约词 → 维持矩阵结果（不下调）
d. 填充 `dept_data.json → te_tiriti.strategy_rationale`
e. 在 fit_report 中生成 **Te Tiriti 评估** 专节（格式见 `references/fit_report_template.md`）
f. **Per-document 建议必须为每个文档提供具体修辞指令**（不能只写 Cover Letter 建议而留空 Research Statement / Teaching Statement）

### 9. AU 原住民矩阵分析（条件：region=australia）

a. 读取 `dept_data.json → au_indigenous` 块（Step 1 已填充的 jd_signal、school_signal、strategy）
b. 读取 Sophia 材料识别可 Claim 的经历锚点（`materials/Research_Statement.md`, `materials/Teaching_Statement.md`）
c. 确认/调整策略标签：
   - Agent 可上调**至多一级**，仅限 skip→subtle 或 subtle→moderate
   - **禁止** agent 自行上调到 strong 或 full_rap
   - 典型上调场景：JD 是 `boilerplate` 但该校已知面试考文化胜任力
   - 上调必须在 `strategy_rationale` 中注明理由
d. 如策略为 `strong`：在 fit_report 中显示升级门槛验证提示（见策略文件 §三）
e. 如策略为 `full_rap`：**暂停并询问用户确认**后才写入最终策略标签（见策略文件 §三）
f. 填充 `dept_data.json → au_indigenous.strategy_rationale`
g. 在 fit_report 中生成 **AU Indigenous 评估** 专节（格式见 `references/fit_report_template.md`）
h. **Per-document 建议必须为每个文档提供具体修辞指令，含 KSC Response 建议**

### 10. 生成匹配报告与溯源文件

- 生成 `output/{school_id}/{dept_id}/fit_report.md`（完整模板见 `references/fit_report_template.md`）
- 生成 `output/{school_id}/{dept_id}/fit_report.sources.md`
