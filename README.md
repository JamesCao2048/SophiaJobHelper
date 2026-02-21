# 海外教职申请流水线

Claude Code 驱动的海外教职申请材料准备工具。提供学校名和职位链接，AI 自动完成院系调研、匹配分析、材料定制，将每所学校的材料准备从 1-2 小时压缩到 15-20 分钟。

---

## 快速开始

```bash
cd overseas_pipeline
claude --dangerously-skip-permissions
```

> **模型选择建议**：Step 1 涉及大量网页爬取，token 消耗大，建议用 **Sonnet** 节省费用；Step 2/3 需要深度推理和写作，建议切换到 **Opus**。在 Claude Code 中输入 `/model` 即可切换。

启动后直接用中文告诉 Claude 你要做什么，例如：

```
研究一下 University of Auckland，链接：https://...
分析 Auckland 的匹配度
给 Auckland 生成材料
```

详细使用说明见 [`overseas_pipeline/README.md`](./overseas_pipeline/README.md)。

---

## 模块说明

### [`overseas_pipeline/`](./overseas_pipeline/) — 申请材料流水线（核心）

三步完成一所学校的完整材料准备：

| 步骤 | 内容 |
|------|------|
| **Step 1** 院系研究 | 爬取教授列表、分析研究重叠、下载相关论文、抓取课程体系 |
| **Step 2** 匹配分析 | 读取 JD + 地区规则卡，生成 Fit Score 和各材料定制建议 |
| **Step 3** 材料生成 | 输出 Cover Letter / Research Statement / Teaching Statement / CV 等完整初稿 |

内含 Sophia 的现有申请材料（`materials/`）和 LaTeX 模板（`overleaf-projects/`），开箱即用。

### [`region_knowledge/`](./region_knowledge/) — 全球申请规则知识库

覆盖 21 个地区的教职申请规则，被流水线 Step 2/3 自动调用：

```
region_knowledge/
├── regions/          # 地区通用规则（new_zealand.md、australia.md 等）
└── schools/          # 学校特有规则（跨院系申请时复用）
```

已覆盖：英 / 澳 / 美 / 加 / 法 / 德 / 荷 / 爱 / 比 / 葡 / 西 / 港 / 新 / 日 / 韩 / 澳门 / 新西兰 / 中东等

### [`job_filling/`](./job_filling/) — 申请表单填写

Chrome 浏览器自动填写网页申请表单，支持多步骤表单的持续填写模式。

### [`general/`](./general/) — 策略规划文档

- `plans/`：申请策略、流程设计文档
- `research_job_rules/`：各地区教职申请机制深度调研

---

## 目录结构

```
SophiaJobHelper/
├── overseas_pipeline/        # 申请材料流水线（主要工作区）
│   ├── materials/            # Sophia 现有材料（CV、Research/Teaching Statement 等）
│   ├── overleaf-projects/    # LaTeX 模板源文件
│   ├── workflows/            # Step 1/2/3 详细执行规范
│   ├── src/                  # 爬取工具脚本
│   └── output/               # 各校分析产出（本地，不提交 git）
├── region_knowledge/         # 全球地区申请规则知识库
├── job_filling/              # 申请表单自动填写
└── general/                  # 通用规划与知识文档
```
