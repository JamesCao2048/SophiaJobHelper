# Phase B: 爬取与分析

> **子步骤文件** — 由 `workflows/step1_research.md` 分派，不可独立执行。

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

### B2-B3. 识别教授、抓取档案、下载论文（含并行结构）

#### Stage 1：从主页 HTML 识别 faculty 列表（顺序执行）

- 读取 B1 爬取的院系主页 markdown
- 读取 `overseas_pipeline/materials/Research_Statement.md` 了解 Sophia 研究方向
- 识别 faculty 列表，对每人判断 `overlap_with_sophia`（**high / medium / ? / low / none**）
- 识别标准：Human-AI collaboration / HCI / CSCW / AI / NLP / qualitative methods 相关
- **`?` 的使用规则**：若主页对该 faculty 的研究方向描述不足，赋值 `?`，**禁止默认填 `low`**
- 对 overlap=high 的 faculty（≤5人）记录初步的 `overlap_reason`
- 将 faculty 列表写入 `faculty_data.json`（仅基础字段，供后续脚本读取）

#### Stage 2：两阶段分析（? 快速扫描 → 摘要精选）

**目标**：
1. 对方向未确认（`?`）的 faculty 先做轻量扫描确认方向
2. 对确认的 high/medium faculty 拉近 3 年论文 + 摘要，选 top 5 写入 JSON

> PDF 下载已暂停，仅使用摘要。PDF 方案见 `docs/plans/pdf-download-plan.md`。

**执行顺序**：Stage 2a（? 快速扫描）→ 汇总后 → Stage 2b（摘要抓取 + 批量扫描并行）

---

**Stage 2a：`?` faculty 快速扫描**

对所有 `overlap=?` 的 faculty（一个 subagent 顺序处理）：

```
来源优先级（按顺序执行，尽量两步都做以互相验证）：

  步骤 1 — DBLP 两步法（首选，抗同名混淆）：
    a. Author search（带机构关键词确认身份）：
       python src/web_fetch_utils.py \
         "https://dblp.org/search/author/api?q={姓名}+{学校关键词}&format=json"
       → 检查返回结果的 affiliation 字段，确认是目标学校的人，获取 PID
       → 若有多个同名结果，选 affiliation 匹配的那条；若无 affiliation 信息则跳到步骤 2
    b. 用确认的 PID 拉论文列表：
       python src/web_fetch_utils.py "https://dblp.org/pid/{pid}.xml"

  步骤 2 — 院系 profile 页面（补充研究方向描述）：
    python src/web_fetch_utils.py "https://profiles.{school}.edu/{slug}" \
      --search-hint "{姓名} {学校名} research interests"
    注：profile 页面若为 JS SPA，脚本将自动 fallback 到 Jina/Tavily

  步骤 3 — WebSearch 兜底（DBLP 无记录 或 profile 页失败时）：
    WebSearch "{姓名} {学校名} publications research interests 2023 2024 2025"

判断研究方向：
  - 方向与 Sophia 相关 → 升级为 high 或 medium，记录 overlap_reason
  - 方向明确不相关   → 降级为 low，记录原因
  - DBLP 记录极少但 profile 页说方向相关 → 标 medium（置信度低）
  - 信息仍不足        → 保持 ?，在 data_quality.json 记录 severity: warning

⚠ DBLP 同名风险：同名不同机构的研究者可能出现在搜索结果里，**必须核查 affiliation**。
   DBLP 无记录不等于无论文——部分研究者发表在非 CS 体系期刊（如教育、社会学），需 fallback 到 profile/WebSearch。

保存到 raw/faculty_profiles/{lastname}_profile.md
更新 faculty_data.json 中的 overlap_with_sophia 字段
```

**Stage 2a 完成后**，重新汇总 high/medium 名单（含升级的 `?` faculty），进入 Stage 2b。

---

**Stage 2b：摘要抓取 + 批量扫描（并行）**

**进入摘要抓取的 faculty**：所有 high/medium（含 Stage 2a 升级的），每人一个 subagent，并行。

```
Stage 2a 完成
  ├─► 【组 A】摘要抓取（high/medium，每人一个 subagent，并行）
  │     目标：拿到近 3 年论文 title + abstract，选 top 5 写入 faculty_data.json
  │
  │     步骤 1 — 获取论文列表（仅标题，不拉摘要）：
  │       python src/paper_metadata.py fetch-dblp \
  │         --pid {dblp_pid} --years 3 \
  │         --output raw/faculty_profiles/{lastname}_titles.json
  │
  │       ⚠ `all` 命令会一次性拉取所有摘要，跳过预筛；论文 > 15 篇时禁止直接用 `all`。
  │       ⚠ PID 来自 Stage 2a 的 DBLP 搜索结果（find-pid 步骤）。
  │
  │       DBLP 无记录时（脚本报告 "No papers"）：
  │         WebSearch "{姓名} {学校名} publications 2023 2024 2025" → 收集标题列表
  │
  │     步骤 1.5 — 按标题预筛（论文数 > 15 时必须执行）：
  │       读取标题列表，按以下规则排除明显无关，保留 ≤ 15 篇候选：
  │         - 排除：纯系统工程、纯 ML 理论（如神经进化、图算法）、
  │                 无用户研究的基础算法论文、非 CS 方向专著章节
  │         - 保留：HCI / CHI / CSCW / IMWUT 体系、AI+human、affective、VR/AR 用户研究
  │       ⚠ 论文数 ≤ 15 时跳过此步，直接进入步骤 2。
  │
  │     步骤 2 — 拉取预筛后的摘要：
  │       python src/paper_metadata.py fetch-abstracts \
  │         --titles "Title 1|Title 2|..." \
  │         --output raw/faculty_profiles/{lastname}_abstracts.json
  │
  │     步骤 3 — LLM 选 top 5 并写入 faculty_data.json：
  │       【精选】读 abstract，按以下标准选 top 5：
  │         - 优先：Human-AI collaboration / AI-driven interaction / affective computing
  │         - 次优：user study / CHI / CSCW / IMWUT 体系
  │         - 再次：AI in education（与 Human-AI 有接触）/ qualitative HCI methods
  │         - 排除：纯系统工程、纯 ML 理论、无用户研究的基础算法论文
  │       【写入】top 5 写入 faculty_data.json → overlapping_papers[]：
  │         每条：title / year / venue / abstract / relevance（1 句说明交集）
  │       【判断】基于 top 5 更新 overlap_with_sophia：
  │         - 有直接 Human-AI 交集 → 维持/升级 high/medium
  │         - 全部无交集 → 降级为 low
  │       【置信度】写入 faculty_data.json → overlap_confidence + overlap_notes：
  │         - high：论文数量多、多篇发表于顶级 HCI 场馆
  │         - medium：有交集但方向偏移、论文稀少、或交集是间接的
  │         - low：仅标题匹配，无摘要证实
  │         overlap_notes 记录任何值得 Step 2 注意的观察（如"近期研究方向漂移"）
  │```

**写入隔离**：每个 subagent 写入自己专属的 `raw/faculty_profiles/{lastname}_abstracts.json`，各教授间文件名不重叠。

#### Stage 3：LLM 背景分析（Stage 2 全部完成后）

- 读取所有 `raw/faculty_profiles/{lastname}_*.md` 和 `{lastname}_abstracts.json`
- 按 `dept_type_strategy.md §1.3.5` 的 background 类别分类，确定每人的 `major` 和 `minor`
- 写入 `faculty_data.json → faculty[i].research_background`
- 统计全院 faculty 的 background 分布，记录到 `faculty_data.json → dept_profile_notes`（Phase C 使用）

> Step 2 fit_report 使用 `overlapping_papers[].abstract` 作为论文分析依据。

### B4. 输出结构化数据（faculty_data.json）

生成 `output/{school_id}/{dept_id}/faculty_data.json`。

完整 JSON schema 见 `../references/faculty_data_schema.md`。

### B5. 输出数据溯源文件

生成 `output/{school_id}/{dept_id}/faculty_data.sources.md`（标注每位 faculty 信息的来源 URL）。
