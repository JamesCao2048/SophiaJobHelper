# Phase B: 爬取与分析

> **子步骤文件** — 由 `workflows/step1_research.md` 分派，不可独立执行。

---

## 流程总览

```
B1  爬取院系主页
 ↓
B2  识别 faculty 列表（基础信息，不判 overlap）
 ↓
B3  全院论文拉取 + 分类（分批并行：拉标题 → 立即判 overlap + background）
 ↓  汇总：统计 background 分布，报告 ? 数量
B4  高相关教授摘要精选（high/medium，分批并行）
 ↓
B5  输出结构化数据
B6  输出数据溯源文件
```

**设计原则**：DBLP 标题是基础数据层。B3 中每位 faculty 拉取标题后立即完成 overlap + background 分类，不等其他人——消除同步等待。摘要预筛（B4）复用 B3 产出的 `_titles.json`，不重复拉取。

---

### B1. 爬取院系主页

```bash
python overseas_pipeline/src/page_scraper.py --school "{学校名}" --url "{院系URL}"
```

脚本内部已封装 curl + Jina Reader。若脚本失败，用 CLI 补救：
```bash
python src/web_fetch_utils.py "院系URL" --search-hint "学校名 department faculty"
```
若全部失败则提示用户手动 copy-paste。

输出原始 markdown 到 `output/{school_id}/{dept_id}/raw/`

---

### B2. 识别 faculty 列表（顺序执行）

- 读取 B1 爬取的院系主页 markdown
- 识别 faculty 列表，提取每人的基础信息并写入 `faculty/{slug}.json`：
  - 姓名、职称、个人主页 URL、所属 cluster/group
  - `research_interests_raw_scrape`：院系主页对该教授的研究方向描述（原文摘录，不解读）
- 同时在 `dept_data.json → faculty_summary[]` 写入摘要条目（name、title、clusters、homepage、file）

**⚠ 此阶段不做 overlap 判断** — 仅提取原始信息。overlap 在 B3 结合 DBLP 数据后判断。

---

### B3. 全院论文拉取 + 分类（分批并行）

**目标**：为每位 faculty 拉取 DBLP 论文标题，**拉完立即分类**（overlap + background），不等其他人。

**分批并行**执行（每批 ≤5 人，每批一个 subagent，批内顺序处理）：

```
分批规则：
  - 将全院 faculty 按顺序分为若干批，每批 ≤5 人
  - 同时启动所有批次的 subagent（如 25 人 → 5 个 subagent 并行）
  - 每个 subagent 内部顺序处理本批 faculty

subagent 输入（每个 subagent 都需读取）：
  - overseas_pipeline/materials/Research_Statement.md（了解 Sophia 研究方向）
  - dept_type_strategy.md §1.3.5（background 分类规则）
```

**每位 faculty 的处理流程**（在 subagent 内顺序执行）：

#### 3a. DBLP 论文标题拉取

```
  步骤 1 — DBLP Author Search（获取 PID）：
    python src/web_fetch_utils.py \
      "https://dblp.org/search/author/api?q={姓名}+{学校关键词}&format=json"
    → 检查返回结果的 affiliation 字段，确认是目标学校的人，获取 PID
    → 若有多个同名结果，选 affiliation 匹配的那条
    → 若无 affiliation 信息，结合 research_interests_raw_scrape 辅助判断

  步骤 2 — 拉取近 3 年论文标题 + venue：
    python src/paper_metadata.py fetch-dblp \
      --pid {dblp_pid} --years 3 \
      --output raw/faculty_profiles/{lastname}_titles.json

  ⚠ DBLP 无记录时：
    WebSearch "{姓名} {学校名} publications 2023 2024 2025"
    → 手动整理标题 + venue 列表，保存到 _titles.json
    → 在 data_quality.json 记录 severity: warning, evidence_source: "web_search"

  ⚠ 信息完全不足时（无 DBLP + WebSearch 无结果）：
    保存空 _titles.json，标记 evidence_source: "insufficient"
```

⚠ **DBLP 同名风险**：同名不同机构的研究者可能出现在搜索结果里，**必须核查 affiliation**。
DBLP 无记录不等于无论文——部分研究者发表在非 CS 体系期刊（如教育、社会学），需 fallback 到 WebSearch。

#### 3b. 立即分类：overlap + background（拉完标题后紧接执行）

**overlap_with_sophia 判断**：

综合 `research_interests_raw_scrape` + DBLP 论文标题/venue，赋值 **high / medium / ? / low / none**：

| 等级 | 判定标准 |
|------|---------|
| **high** | 论文列表中有多篇 HCI / Human-AI / CSCW 相关（venue 或标题匹配），或主页明确描述相关方向 |
| **medium** | 有部分相关论文或方向间接相关（如 AI+education、affective computing） |
| **low** | 论文方向明确不相关（如纯 ML 理论、纯系统） |
| **none** | 完全不同领域（如纯数学、纯生物、行政人员） |
| **?** | 主页描述不足 **且** DBLP 无记录或记录极少 — 仅在双重信息缺失时使用 |

- 识别标准：Human-AI collaboration / HCI / CSCW / AI / NLP / qualitative methods 相关
- 对 overlap=high 和 medium 的 faculty 记录 `overlap_reason`

**research_background 分类**：

按 `dept_type_strategy.md §1.3.5` 分类，确定 `major` / `minor`：

```
信息来源优先级（从高到低）：
  1. venue（确定大类，如 NeurIPS → ml_theory，UIST → hci_systems）
  2. 标题关键词（区分同 venue 内的子类型，如 CHI qual vs systems）
  3. research_interests_raw_scrape（辅助验证，尤其在论文数量少时）

major：近 5 年发表中某类 venue 占比 ≥60%
minor：占比 15–40%（可为 null）
evidence_venues：列出支撑分类的代表 venue（3-5 条）

DBLP 无记录且 WebSearch 也无结果：major = null
```

**写入**：更新 `faculty/{slug}.json` — overlap_with_sophia、overlap_reason、research_background

#### 3c. 全部 subagent 完成后汇总（主 agent 执行）

- 同步更新 `dept_data.json → faculty_summary[]` 中每位 faculty 的 overlap_with_sophia
- 统计全院 background 分布 → `dept_data.json → dept_profile.faculty_background_distribution`（Phase C 使用）
- 若存在 `overlap=?` 的 faculty，在 `step1_summary.md` 报告数量及姓名，标注原因（主页无描述 + DBLP 无记录），在 `data_quality.json` 记录 `severity: warning`

**写入隔离**：每位 faculty 写入自己的 `raw/faculty_profiles/{lastname}_titles.json` 和 `faculty/{slug}.json`，各 subagent 间文件名不重叠。

---

### B4. 高相关教授摘要精选（high/medium 分批并行）

**进入摘要抓取的 faculty**：所有 high/medium，分批并行（每批 ≤5 人，每批一个 subagent）。

> PDF 下载已暂停，仅使用摘要。PDF 方案见 `docs/plans/pdf-download-plan.md`。

```
每位 high/medium faculty 的处理流程：

  步骤 1 — 按标题预筛（论文数 > 15 时必须执行）：
    读取 B3 已获取的 _titles.json（无需重新拉取），按以下规则保留 ≤ 15 篇候选：
      - 排除：纯系统工程、纯 ML 理论（如神经进化、图算法）、
              无用户研究的基础算法论文、非 CS 方向专著章节
      - 保留：HCI / CHI / CSCW / IMWUT 体系、AI+human、affective、VR/AR 用户研究
    ⚠ 论文数 ≤ 15 时跳过此步，直接进入步骤 2。

  步骤 2 — 拉取摘要：
    python src/paper_metadata.py fetch-abstracts \
      --titles "Title 1|Title 2|..." \
      --output raw/faculty_profiles/{lastname}_abstracts.json

    ⚠ `all` 命令会一次性拉取所有摘要，跳过预筛；论文 > 15 篇时禁止直接用 `all`。

  步骤 3 — LLM 选 top 5 并写入 faculty/{slug}.json：
    【精选】读 abstract，按以下标准选 top 5：
      - 优先：Human-AI collaboration / AI-driven interaction / affective computing
      - 次优：user study / CHI / CSCW / IMWUT 体系
      - 再次：AI in education（与 Human-AI 有接触）/ qualitative HCI methods
      - 排除：纯系统工程、纯 ML 理论、无用户研究的基础算法论文

    【写入】top 5 写入 faculty/{slug}.json → overlapping_papers[]：
      每条：title / year / venue / abstract / relevance（1 句说明交集）

    【判断】基于 top 5 更新 overlap_with_sophia：
      - 有直接 Human-AI 交集 → 维持/升级 high/medium
      - 全部无交集 → 降级为 low

    【置信度】写入 faculty/{slug}.json → overlap_confidence + overlap_notes：
      - high：论文数量多、多篇发表于顶级 HCI 场馆
      - medium：有交集但方向偏移、论文稀少、或交集是间接的
      - low：仅标题匹配，无摘要证实
      overlap_notes 记录任何值得 Step 2 注意的观察（如"近期研究方向漂移"）

    【背景修正】若 abstract 揭示 B3 的 background 分类有误，更新 research_background
```

**写入隔离**：每个 subagent 写入自己专属的 `raw/faculty_profiles/{lastname}_abstracts.json`，各教授间文件名不重叠。

> Step 2 fit_report 使用 `overlapping_papers[].abstract` 作为论文分析依据。

---

### B5. 输出结构化数据（dept_data.json + faculty/）

生成以下文件：
- `output/{school_id}/{dept_id}/dept_data.json` — 院系级数据（metadata、job_posting、dept_profile、hci_density、strategic_intelligence、te_tiriti、teaching_context、decision_makers、data_quality、faculty_summary[]）
- `output/{school_id}/{dept_id}/faculty/{slug}.json` — 每位 faculty 一个文件（name、title、homepage、clusters、research_interests、overlap_with_sophia、overlap_reason、research_background、overlapping_papers 等）

`dept_data.json` 中的 `faculty_summary[]` 每条包含 `file` 字段指向对应的 `faculty/{slug}.json`。

完整 JSON schema 见 `../references/faculty_data_schema.md`。

### B6. 输出数据溯源文件

生成 `output/{school_id}/{dept_id}/dept_data.sources.md`（标注院系数据及每位 faculty 信息的来源 URL）。
