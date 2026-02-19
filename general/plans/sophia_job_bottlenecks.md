# Sophia 找教职：关键瓶颈与 Agent 优化机会分析

> 基于 SophiaJobHelper 项目、Research-Notes、Job Talk 笔记、Research Statement、以及近期对话
文档来源 https://github.com/JamesCao2048/personal-branding/blob/master/docs/sophia-job-search-bottlenecks.md

---

## 一、当前状态

- **美国市场**：投了很多，今年行情差，几乎没拿到 interview
- **下一步**：主投澳洲、欧洲，基本在 online 面试及之前阶段
- **已有工具**：SophiaJobHelper（job_hunting 搜集 + job_filling 表单自动填写），主要覆盖国内高校
- **研究方向**：Human-AI Collaboration for Unstructured Data Analysis（HCI + AI + 软工）
- **代表作**：CollabCoder (CHI)、CoAIcoder (TOCHI)、MindCoder、Taxonomy (human-LLM interaction)

---

## 二、关键瓶颈识别

### 瓶颈 1：🎯 命中率极低——"广投但不精投"

**问题**：美国市场行情差不是她能控制的，但投了很多没有 interview 说明可能存在 **材料-学校匹配度** 问题。每个学校的 hiring committee 关注点不同，通用材料很难打动人。

**具体痛点**：
- Cover Letter 需要针对每个学校的研究方向、院系特色做定制，手动改非常耗时
- Research Statement 的 framing 是否对齐目标学校的 cluster 方向（比如有的学校偏 AI systems，有的偏 social computing）
- 不清楚哪些学校的 committee member 和自己的 research 有交集（可以在信里 name-drop）

**Agent 优化点**：
- **School-Fit Analyzer Agent**：爬取目标院系的 faculty list → 分析每位教授的 research keyword → 计算与 Sophia 研究方向的 overlap → 生成 fit score + 推荐 mention 的教授名字
- **Cover Letter Personalizer Agent**：输入学校信息，自动生成针对性 cover letter 段落（"Your department's strength in X aligns with my work on Y..."）
- **Application Tracker Dashboard**：跟踪每个申请的状态，自动提醒 deadline，标记 high-fit 学校优先投

### 瓶颈 2：🌏 澳洲/欧洲市场不熟——信息不对称

**问题**：之前主投美国+中国，对澳洲/欧洲的学术招聘生态不够熟悉。不同地区的申请规则、材料要求、评审文化差异很大。

**具体痛点**：
- 澳洲/欧洲的招聘网站分散（不像美国有 HigherEdJobs/academicjobsonline 集中）
- 不同国家对 Teaching Statement、Research Statement 的期望格式不同
- 不清楚哪些学校有 HCI 方向（尤其是非 top 但 quality 不错的学校）
- 签证/tenure-track 政策各国不同

**Agent 优化点**：
- **Global Job Scout Agent**：扩展 SophiaJobHelper 的 job_hunting 到澳洲/欧洲，监控 jobs.ac.uk、euraxess.ec.europa.eu、seek.com.au/academic 等平台
- **Region Adaptation Agent**：输入目标国家，输出该地区学术招聘的格式要求、文化注意点、常见面试问题
- **HCI Faculty Map**：构建全球 HCI 方向院系地图（基于 CHI/CSCW/UIST 发表数据），识别 Sophia 没注意到的潜在目标

### 瓶颈 3：📹 Job Talk / Interview 准备不足

**问题**：从 job talk 笔记看，Sophia 有很好的 narrative vision（"Efficiency is not the right goal" → "Human-AI collaboration for better outcomes" → "Collaboration enables learning"），但还在打磨中，很多 TODO 未完成。

**具体痛点**：
- Job talk slides 内容结构已有雏形，但例子还不够 concrete（多处 "TODO: 想更深入的例子"）
- 还没有录制练习视频来审视自己的表现
- 澳洲/欧洲的 online interview 和美国 on-site 不同，需要适应远程呈现
- 没有模拟 Q&A 练习（面试官常问的 challenging questions）

**Agent 优化点**：
- **Talk Rehearsal Agent**：
  - 录制练习视频 → 自动转录 → 分析语速、filler words、关键信息覆盖度
  - 对比 slides 内容和口述内容的 alignment
  - 标记"你说了但 slides 没展示的"和"slides 有但你忘了说的"
- **Mock Q&A Agent**：基于 Sophia 的 research statement + 目标学校方向，生成高概率面试问题：
  - "How does your work differ from just adding human-in-the-loop?"
  - "What's your 5-year research plan?"
  - "How would you secure funding for this line of research?"
  - "Can you teach a course on X?"（根据学校的 course catalog 定制）
- **Presentation Coach**：分析 online interview 的特殊要求（摄像头角度、背景、网络、屏幕共享技巧）

### 瓶颈 4：📝 论文发表节奏——需要更多弹药

**问题**：教职申请的核心竞争力是 publication record。MindCoder 是当前的主要 pipeline，需要尽快产出 paper（UIST 或 CHI）。

**具体痛点**：
- MindCoder framing 还在纠结 CHI vs UIST（从对话看，UIST timeline 更合适但 framing 需要调整）
- 前端开发（React）占用大量时间，不是 Sophia 的核心竞争力
- 论文写作本身耗时

**Agent 优化点**：
- **Paper Writing Assistant**：
  - 不是让 AI 写论文，而是帮管理写作流程：outline tracking、word count 目标、deadline countdown
  - Related work 自动搜索和整理（输入关键词 → 输出格式化的 related work 段落草稿，人来审核）
  - 自动检查 formatting（是否符合 ACM template、reference 格式）
- **Framing Advisor Agent**：输入论文的 contribution 和目标 venue → 分析过去 3 年该 venue 的 accepted papers 的 framing pattern → 建议最佳 story angle
- **前端开发加速**：James 直接用 Agent 帮 Sophia 做 MindCoder 的前端开发（你已经在 #mindcoder 频道做了），释放她的时间做 study design 和 writing

### 瓶颈 5：🤝 Network / Visibility 不够

**问题**：在竞争激烈的市场，很多 offer 给了有 connection 的候选人。Sophia 的研究在 HCI 圈子有一定知名度（TOCHI、CHI 发表），但还需要更多 visibility。

**具体痛点**：
- 没有系统性地 reach out 给目标学校的 faculty
- 学术社交媒体（Twitter/X、Google Scholar）profile 可能不够突出
- 没有利用 conference networking 的机会

**Agent 优化点**：
- **Networking Agent**：
  - 识别目标学校 hiring committee 中可能认识 Sophia 的人（共同 co-author、同 workshop、同 reviewer pool）
  - 生成 warm intro email 草稿
  - 追踪谁回复了、谁没回复
- **Academic Presence Agent**：
  - 自动更新 Google Scholar profile
  - 定期发 research summary 到 Twitter/X（基于最新论文）
  - 监控 citation 和 mention

---

## 三、优先级排序（投入产出比）

| 优先级 | 优化点 | 投入 | 预期产出 | 理由 |
|--------|--------|------|----------|------|
| 🔴 P0 | Cover Letter 个性化 Agent | 低（已有材料模版） | 高（直接提升命中率） | 澳洲/欧洲马上要投，最急 |
| 🔴 P0 | 全球职位监控扩展 | 中（需要新数据源） | 高（发现更多机会） | 主投方向转移，急需 |
| 🟡 P1 | Mock Q&A + Talk 练习 | 低（可以立即开始） | 高（面试是 converting 关键） | 有 interview 才需要，但要提前准备 |
| 🟡 P1 | School-Fit 匹配分析 | 低 | 中（帮助精准投递） | 避免浪费时间投不匹配的学校 |
| 🟢 P2 | MindCoder 前端加速 | James 做 | 高（释放 Sophia 做研究） | 已经在做了 |
| 🟢 P2 | Paper framing advisor | 中 | 中（长期价值） | UIST/CHI deadline 驱动 |
| ⚪ P3 | Networking Agent | 低 | 中（长尾效应） | 重要但不紧急 |
| ⚪ P3 | Talk 录制分析 | 中 | 中 | 等有 interview 再做也行 |

---

## 四、立即可做的事（本周）

1. **扩展 SophiaJobHelper 到澳洲/欧洲数据源** — 加 jobs.ac.uk、euraxess、seek academic
2. **写一个 Cover Letter 个性化脚本** — 输入学校名+院系 → 爬取 faculty list → 匹配 research keyword → 生成定制段落
3. **准备 Mock Q&A 题库** — 基于她的 research statement 和常见教职面试问题
4. **建一个全球 HCI faculty map** — 从 DBLP/Google Scholar 数据找出哪些学校有 HCI group

---

## 五、双赢：这些工具本身就是你的产品原型

每一个为 Sophia 做的工具，都是你 Phase 2 的开源产品候选：

| 给 Sophia 的工具 | 通用化后的产品 |
|------------------|----------------|
| School-Fit Analyzer | → Academic Job Matching Service |
| Cover Letter Personalizer | → AI-Powered Academic Application Suite |
| Mock Q&A Agent | → Interview Prep for Academics |
| Global Job Scout | → Academic Job Aggregator |
| Talk Rehearsal Agent | → Presentation Coach for Researchers |

**而且这些工具的使用数据 = Sophia 发 paper 的素材**（"We dogfooded our own agentic tools during a real job search..."）。一鱼三吃仍然成立。🐲

---

*文档生成日期：2026-02-18*