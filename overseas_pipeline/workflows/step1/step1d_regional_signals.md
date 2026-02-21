# Phase D: 地区信号检测（条件触发）

> **子步骤文件** — 由 `workflows/step1_research.md` 分派，不可独立执行。
> **触发条件**：`region=new_zealand`（D1）或 `region=australia`（D2）

JSON 格式定义见 `../references/regional_signal_schemas.md`。

---

## D1. NZ Te Tiriti 信号检测（仅 region=new_zealand）

读取策略文件：`overseas_pipeline/strategies/nz_te_tiriti_strategy.md`

### A. JD 信号检测

1. 读取 `raw/jd_main.md`（Phase A 已完成；若文件缺失，说明 A4 未执行，立即补爬后继续）
2. 扫描策略文件 §一 中的关键词清单（核心词 + 辅助词）
3. 按位置权重规则判定 `jd_signal` level：
   - Essential Criteria / Key Responsibilities → `explicit`
   - Desirable / Nice-to-have → `boilerplate`
   - 仅 EEO 样板 / 页脚 → `no_mention`
4. 对每个命中词记录：原文文本 + 所在板块/bullet 位置
5. 写入 `faculty_data.json → te_tiriti.jd_signal`

### B. 学校信号检测

1. 检查学校卡 `region_knowledge/schools/{school_id}/{dept_id}.md` 是否已有 `Te Tiriti 学校信号` 字段，且 `assessed_date` 在 6 个月内
   - 如有 → 读取复用，写入 `faculty_data.json → te_tiriti.school_signal`，跳到 C
   - 如无或已过期 → 继续
2. 查策略文件 §六 学校种子表，按 school_id 匹配已知条约页面 URL
3. 爬取种子 URL：`python src/web_fetch_utils.py "种子URL" --search-hint "学校名 Te Tiriti"`
4. 如种子不足或失败，搜索补充：
   - `"{school_name} Te Tiriti strategy"`
   - `"{school_name} Māori strategic framework"`
   - `"{school_name} Treaty of Waitangi policy"`
5. 基于爬取内容评定 `school_signal` level（见策略文件 §一 1.2 评级标准）
6. 摘录原文证据（至少 2 条），记录来源 URL + 文档名
7. 识别该校专有框架名称和核心价值观术语
8. **双写入：**
   - 写入 `region_knowledge/schools/{school_id}/{dept_id}.md → ## Te Tiriti 学校信号`
   - 写入 `output/{school_id}/{dept_id}/knowledge/{dept_id}.md`（同步）
9. 写入 `faculty_data.json → te_tiriti.school_signal`

### C. 预判策略标签

1. 查策略文件 §二 矩阵，根据 jd_signal × school_signal 得出初步 strategy label
2. 如为 `strong` 或 `full_treaty` → **在 `step1_summary.md` 中写入完整的 Te Tiriti 中断报告**（须包含以下所有要素）：
   - **Te Tiriti 背景说明**（2-3 句话解释什么是 Te Tiriti、为什么对学术招聘重要）
   - **JD 原文摘录**：引用 JD 中 Māori/Pasifika/Treaty 相关原文（标注所在章节）
   - **学校战略文件原文摘录**：引用抓取到的 Te Tiriti / Waipapa / Te Ao Māori 相关段落
   - **参考 URL**：列出战略文件、招聘政策等来源链接
   - **对材料的具体影响**：Cover Letter / Research Statement / Teaching Statement 各需要什么
   - **面试注意事项**
   ```
   ⚠ NZ Te Tiriti 高级别信号（[strategy]），需用户审查后手动触发 Step 2
   ```
   > ⚠ 不得假设用户了解 NZ 文化背景。中断报告的目标是让从未接触过 Te Tiriti 的申请者也能理解其重要性和对材料准备的影响。
3. 写入 `faculty_data.json → te_tiriti.strategy`
4. 留空 `te_tiriti.strategy_rationale`（Step 2 填充）
5. 在 `step1_summary.md` 中追加一行：`Te Tiriti: JD=[level], School=[level] → [strategy]（初步）`
6. **全量模式中断判定**：如 strategy ∈ {strong, full_treaty} → 全量模式下 pipeline 在 Step 1 完成后**自动中断**，不进入 Step 2，等待用户审查 step1_summary 后手动触发继续

---

## D2. AU 原住民信号检测（仅 region=australia）

读取策略文件：`overseas_pipeline/strategies/au_indigenous_strategy.md`

### A. JD 信号检测

1. 读取 `raw/jd_main.md`（Phase A 已完成；若文件缺失，说明 A4 未执行，立即补爬后继续）
2. 扫描策略文件 §一 中的关键词清单（核心词 + 辅助词）
3. 按位置权重规则判定 `jd_signal` level：
   - Essential Criteria / Key Responsibilities / Selection Criteria → `explicit`
   - Desirable / Nice-to-have / About the University → `boilerplate`
   - 仅 EEO 样板 / 页脚 → `no_mention`
4. 对每个命中词记录：原文文本 + 所在板块/bullet 位置
5. 写入 `faculty_data.json → au_indigenous.jd_signal`

### B. 学校信号检测

1. 检查学校卡 `region_knowledge/schools/{school_id}/{dept_id}.md` 是否已有 `AU Indigenous 学校信号` 字段，且 `assessed_date` 在 6 个月内
   - 如有 → 读取复用，写入 `faculty_data.json → au_indigenous.school_signal`，跳到 C
   - 如无或已过期 → 继续
2. 查策略文件 §八 学校种子表，按 school_id 匹配已知 RAP/Indigenous Strategy URL
3. 爬取种子 URL：`python src/web_fetch_utils.py "种子URL" --search-hint "学校名 Indigenous strategy"`
4. 如种子不足或种子全部失败，搜索补充：
   - `"{school_name} Reconciliation Action Plan"`
   - `"{school_name} Indigenous strategy"`
   - `"{school_name} Aboriginal Torres Strait Islander employment"`
5. Agent 基于爬取内容评定 `school_signal` level（见策略文件 §一 1.2 评级标准）
6. 摘录原文证据（至少 2 条），记录来源 URL 和文档名
7. 识别 RAP tier、原住民战略名称、学术支持中心名称
8. **双写入：**
   - 写入 `region_knowledge/schools/{school_id}/{dept_id}.md → ## AU Indigenous 学校信号`（格式见策略文件 §七 7.2）
   - 写入 `output/{school_id}/{dept_id}/knowledge/{dept_id}.md`（同步）
9. 写入 `faculty_data.json → au_indigenous.school_signal`

### C. 预判策略标签

1. 查策略文件 §二 矩阵，根据 jd_signal × school_signal 得出初步 strategy label
2. 如为 `strong` 或 `full_rap` → **在 `step1_summary.md` 顶部标注中断警告**
3. 写入 `faculty_data.json → au_indigenous.strategy`
4. 留空 `au_indigenous.strategy_rationale`（Step 2 填充）

### D. Step 1 Summary 新增行

在 `step1_summary.md` 中追加：
- `"AU Indigenous: JD=[level], School=[level] → [strategy_label]（初步）"`
- 如 strong/full_rap: `"⚠ AU Indigenous 高级别信号，需用户审查 step1_summary 后手动触发 Step 2"`

### E. 全量模式中断判定

如 strategy_label ∈ {strong, full_rap} → **全量模式下 pipeline 在 Step 1 完成后自动中断**，不进入 Step 2，等待用户审查 step1_summary 后手动触发继续。
