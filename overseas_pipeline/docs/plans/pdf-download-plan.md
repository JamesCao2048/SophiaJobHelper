# PDF 下载方案（存档，待后续实现）

> 当前流程已简化为仅使用摘要（abstract）。本文档记录完整 PDF 下载方案以备后续实现。

## 背景

Step 1 Phase B 原设计中，对 high/medium faculty 的 top 3 相关论文进行 PDF 下载，
供 Step 2 fit_report 精读分析。实际执行中遇到以下问题：
- VR/AR / HCI 类论文多在 ACM/IEEE 付费墙后，无 OA 版本
- PDF 下载 fallback 链路长、等待慢，阻断整体流程
- 暂时用摘要替代已足够支撑 Step 2/3 分析

## 完整方案设计（待实现）

### 触发时机

在 A-1 选出 top 5 + abstract 之后，启动 A-2 PDF 下载（可选/后台）。

### PDF 查找优先级（每篇最多 3 步，失败即跳）

```
1. OpenAlex 返回的 oa_url（若存在）
2. WebSearch "{论文标题} site:arxiv.org"
3. WebSearch "{论文标题} filetype:pdf"（作者 preprint/个人主页）
❌ 不走 web_fetch_utils.py 五层 fallback（太慢）
❌ 不尝试 Sci-Hub、Unpaywall、ResearchGate
```

### 下载命令

```bash
python src/faculty_scraper.py download-paper \
  --url "{PDF_URL}" \
  --output "output/{school_id}/{dept_id}/papers/{姓}_{年}_{短标题}.pdf"
```

### 写入格式

成功后写入 `faculty_data.json → faculty[i].overlapping_papers[j].local_pdf`

### Step 2/3 读取优先级

`local_pdf` > `abstract`（两者均存于 `overlapping_papers[]`）

### 命名规则

`{作者姓}_{年份}_{简短标题}.pdf`（简短标题取前 3 个有意义词，snake_case）

## 现有已下载 PDF

UoA CS（2026-02-20）：
- `papers/pai_2025_introspectus_ai.pdf`
- `papers/pai_2025_haptic_empathy.pdf`
- `papers/pai_2024_radarhand.pdf`
- `papers/warren_2025_chatbot_therapeutic_alliance.pdf`
- `papers/warren_2025_personalised_affective_modelling.pdf`
- `papers/warren_2025_xai_explainability.pdf`
- `papers/wuensche_2024_gpt4_cg_assessment.pdf`

这些已有 PDF 在 Step 2/3 中仍正常使用（`local_pdf` 字段已填充）。
