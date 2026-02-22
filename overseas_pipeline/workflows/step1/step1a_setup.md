# Phase A: 初始化与数据准备

> **子步骤文件** — 由 `workflows/step1_research.md` 分派，不可独立执行。

---

### A0. 环境检查（强制）

**在执行任何 Step 1 操作前，必须检查以下环境依赖：**

```bash
python3 -c "from src.web_fetch_utils import TAVILY_API_KEY; print('✅ TAVILY_API_KEY loaded') if TAVILY_API_KEY else print('❌ TAVILY_API_KEY not set')"
```

**TAVILY_API_KEY 缺失时的影响：**
- Layer 2 (Tavily Extract) 和 Layer 3 (Tavily Search) **完全不可用**
- 五层 fallback 退化为三层（curl → Jina → Wayback），搜索准确性严重下降
- 课程目录、JD 页面等 Cloudflare 防护站点大概率无法获取

**修复方式：**
1. 在 `overseas_pipeline/.env` 中添加：`TAVILY_API_KEY=your_key_here`
2. `.env` 已在 `.gitignore` 中排除，不会被提交
3. `web_fetch_utils.py` 会自动从 `.env` 加载

**如未配置，必须提示用户：**
> "⚠ TAVILY_API_KEY 未配置。Layer 2/3 搜索不可用，将严重影响数据抓取质量。请在 `overseas_pipeline/.env` 中配置后重试。"

---

### A1. 确定学校与院系标识

- `school_id`：snake_case，如 `monash_university`
- `dept_id`：目标院系英文缩写，snake_case，如 `dsai`、`hcc`、`cs`
- 输出目录：`output/{school_id}/{dept_id}/`（单系学校也保留 `dept_id` 层）

### A2. 复用同校已有数据（如 `output/{school_id}/` 已存在）

- 列出已有的 `{dept_id}/` 子目录
- 识别与当前院系 faculty 重叠的教授（joint appointment 或同校 HCI 教授）
- 将有价值的论文 PDF **复制**到当前院系的 `papers/` 目录（不是 symlink）
- 将已有院系的 `related_applications` 信息写入当前院系的 `dept_data.json`
- 在 step1_summary.md 中列出：从哪个已有院系复用了哪些论文

**跨系 faculty 数据复用约定：**
- 已有院系的 `cross_department_collaborators` 往往正是当前院系的主体 faculty
- 预填充步骤：从已有院系的 `cross_department_collaborators` 中，找出 `department` 字段匹配当前院系的成员，将其基础信息作为当前院系 `faculty` 数组的**起点**
- 预填充只是起点，仍需：① 重新判断 `overlap_with_sophia`；② 重新搜索 `overlapping_papers`
- 已下载的论文 PDF 可直接复用（复制到当前 `papers/`），无需重新下载

**跨系规则卡复用约定：**

> ⚠ 复用范围必须严格区分"学校级"与"院系级"——不同院系的战略方向、维度评估、课程体系完全独立，不能互相继承。

| 数据类型 | 是否可跨系复用 | 说明 |
|---------|-------------|------|
| `hci_ecosystem`（学校 HCI 生态图谱） | ✅ 可复用 | 同一所学校的 HCI 教授分布是学校级信息 |
| `strategic_intelligence.school_level`（学校战略规划） | ✅ 可复用（6 个月内） | 学校整体战略对所有院系相同 |
| Te Tiriti / AU Indigenous school_signal | ✅ 可复用（6 个月内） | 已由信号检测步骤处理 |
| `dept_profile.dimensions`（四维评分） | ❌ 必须重新分析 | 每个院系维度完全不同 |
| `strategic_intelligence.clusters`（研究 cluster） | ❌ 必须重新分析 | 不同院系 cluster 完全不同 |
| `teaching_context`、`decision_makers` | ❌ 必须重新分析 | 院系特有信息 |

**操作流程：**
- 扫描 `region_knowledge/schools/{school_id}/` 找到已有规则卡
- 仅提取上表中"可复用"字段，写入当前院系规则卡，标注 `source_dept: {来源院系}` 和 `source_date: {原采集日期}`
- 复用内容不替代 Phase C 的重新采集——只作为参考起点

### A3. 检查地区规则卡（强制）

- 从 JD 或学校信息确定 `region`（如 `new_zealand`、`australia`）
- 使用**绝对路径**检查地区规则卡是否存在：
  ```
  ../region_knowledge/regions/{region}.md
  ```
- ⚠️ **不要用相对路径**（工作目录是 `overseas_pipeline/`，`region_knowledge/` 在项目根目录）
- 如果存在：
  - 读取并记录关键信息（薪资基准、特殊材料要求、评审重点）
  - 在 `step1_summary.md` 中标注：地区规则卡已存在 + 路径
  - 将地区卡中的特殊要求（如 NZ 的 Te Tiriti、澳洲的 KSC）传递给后续步骤
- 如果不存在：
  - 在 `step1_summary.md` 中标注：地区规则卡不存在，Step 2 前需创建
  - 提示用户

### A4. 爬取职位描述（强制，尽早执行）

JD 原文是后续多个步骤的共同输入（维度评估 C3、Te Tiriti/AU Indigenous 信号检测、Step 2 匹配分析），必须在 Step 1 早期完成。

```bash
python overseas_pipeline/src/page_scraper.py --url "{job_url}" --output-type raw \
  --output-dir output/{school_id}/{dept_id}/raw/
```

- 输出文件命名：`raw/jd_main.md`；若 JD 有多页（如独立的 Selection Criteria 页），追加命名 `jd_ksc.md`、`jd_about.md` 等
- 若脚本失败，使用 `web-fetch-fallback` skill 补救
- 若 URL 不可访问（需登录/已关闭）：提示用户手动粘贴 JD 文本到 `raw/jd_main.md`
- 写入 `dept_data.json → job_posting.job_url`（如尚未写入）
