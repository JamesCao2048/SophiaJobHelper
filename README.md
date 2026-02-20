# Sophia — 教职申请自动化工具集

AI 辅助的学术教职求职全流程工具，覆盖国内 + 海外双线申请，从职位搜集、材料准备到表单自动填写的完整闭环。

## 如何启动 Claude Code

本项目各子模块均通过 Claude Code CLI 驱动。**从对应子项目目录内启动**，确保相对路径正确解析：

```bash
# 海外教职申请流水线（主要工作区）
cd overseas_pipeline
claude --dangerously-skip-permissions

# 追踪系统（查看申请状态）
cd ..   # 回到项目根目录
python -m tracking.cli dashboard
```

> `--dangerously-skip-permissions` 跳过每次操作的权限确认弹窗，是在本地受信任环境下高效使用 AI 流水线的标准启动方式。**请勿在不信任的机器或共享环境中使用此参数。**

---

## 子项目

### [`china_job_hunting/`](./china_job_hunting/) — 国内教职搜集与材料生成

针对国内高校教职（AI / HCI / HAI 方向）的批量数据管理与材料生成：

- **数据管道**：爬取职位页面，自动补全截止日期、薪酬待遇、博导资格等关键信息
- **院校扫描**：搜索 985 及 HCI 方向强校，发现新招聘机会
- **分析摘要**：为每所院校生成包含岗位分析、研究方向匹配度、申请策略的 `summary.md`
- **材料生成**：批量输出给 HR / 导师的邮件模板及个性化 Cover Letter

---

### [`overseas_pipeline/`](./overseas_pipeline/) — 海外教职申请材料准备流水线

Claude Code 驱动的海外教职申请材料准备流水线，目标将每所学校的材料准备从 1-2 小时降至 15-20 分钟：

- **Step 1 爬取**：抓取目标学校职位页面信息（`src/faculty_scraper.py`）
- **Step 2 匹配分析**：结合 `region_knowledge/` 分析地区规则与申请者匹配度
- **Step 3 材料定制**：基于 LaTeX 模板生成学校专属 Cover Letter 初稿
- **多层 Fallback**：大学网站普遍有 Cloudflare 保护，内置 web-fetch-fallback 策略

---

### [`region_knowledge/`](./region_knowledge/) — 全球教职申请区域知识库

独立知识子模块，管理全球各地区和学校的教职申请规则：

- **双层知识架构**：`regions/{region}.md`（地区通用规则）+ `schools/{school}.md`（学校特有信息）
- **覆盖地区**：英/澳/美/加/法/德/荷/爱/比/葡/西/港/新/日/韩/澳门/新西兰/中东等 21 个区域
- **被 overseas_pipeline 调用**：Step 2 匹配分析 + Step 3 材料定制时读取

---

### [`job_filling/`](./job_filling/) — 申请表单自动填写

通过 Chrome CDP 连接浏览器，由 Claude Code 直接推理填写网页申请表单：

- **智能匹配**：读取个人 profile + 材料文档，推理每个字段的最佳值
- **积累学习**：记录每次填写后的用户修正，下次申请自动复用
- **持续填写模式**：自动监控翻页，循环填写多步表单，无需手动干预

---

### [`faculty-application_script/`](./faculty-application_script/) — 每日职位监控

每日自动抓取多个学术招聘平台（RSS / 网页）的 HCI / AI / CS 方向教职信息，筛选后推荐最匹配职位并写入追踪表。

---

### [`google-sheets-sync/`](./google-sheets-sync/) — Google Sheets 数据同步

与 Google Sheets 双向同步职位数据，支持格式保留（颜色、筛选器）导出为 Excel。

---

### [`general/`](./general/) — 通用规划与知识文档

- `plans/`：申请策略规划文档
- `research_job_rules/`：各地区教职申请机制深度调研（DeepResearch 产出）

---

### [`overseas_pipeline/overleaf-projects/`](./overseas_pipeline/overleaf-projects/) — LaTeX 申请材料

本地 Overleaf 项目同步目录，已整合进 `overseas_pipeline/` 以便流水线直接访问。**完整内容通过 Google Drive 管理**，git 仅保留 3 个参考模板的 `.tex` 源码：

| 保留项目 | 用途 |
|----------|------|
| `Faculty Position/CV_latest/` | CV 模板 |
| `Faculty Position/Research Statement/` | Research Statement 模板 |
| `Cover Letter/Cover Letter - King's College London/` | Cover Letter 模板 |

---

## 整体工作流

```
[china_job_hunting] 搜集国内职位 → 分析筛选 → 生成邮件草稿
                                                      ↓
                                          联系对方 / 获取网申链接
                                                      ↓
[job_filling] Chrome 打开申请页 → 自动填写表单 → 提交

[overseas_pipeline] 职位页面爬取 → 地区规则匹配（region_knowledge）→ 生成材料初稿
```

## 项目结构

```
SophiaJobHelper/
├── china_job_hunting/        # 国内教职搜集与材料生成
├── overseas_pipeline/        # 海外教职材料准备流水线
├── region_knowledge/         # 全球地区申请规则知识库
├── job_filling/              # 申请表单自动填写
├── faculty-application_script/ # 每日职位监控脚本
├── google-sheets-sync/       # Google Sheets 数据同步
├── general/                  # 通用规划与知识文档
├── overseas_pipeline/overleaf-projects/  # LaTeX 材料（已移入 overseas_pipeline）
└── .gitignore
```

## .gitignore 策略

以下内容仅保留在本地，**不纳入版本控制**：

| 类别 | 示例 |
|------|------|
| 申请材料 PDF | `materials/`（除参考 .tex 外） |
| 生成草稿 | `china_job_hunting/drafts/`、`overseas_pipeline/output/` |
| 数据文件 | `*.xlsx`、`*.csv`（职位数据库） |
| Overleaf 完整项目 | `overseas_pipeline/overleaf-projects/`（除 3 个参考模板） |
| 敏感信息 | `profile.yaml`、`.env`、`credentials/`（API 密钥） |
| 运行日志 | `faculty-application_script/monitor_log.txt` |
| 系统文件 | `.DS_Store`、`__pycache__/` 等 |

版本控制追踪的是**代码逻辑与知识结构**（Python 脚本、LaTeX 模板、规则卡文档），而非数据产出物。
