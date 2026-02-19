# job_hunting — 教职职位搜集与申请材料生成

自动化管理国内高校教职申请流程：从职位搜集、数据填充，到分析摘要与邮件草稿生成。

## 功能概述

| 阶段 | 功能 |
|------|------|
| **Setup** | 验证 Excel 数据结构、格式校验、去重 |
| **Fill** | 爬取职位页面，补全截止日期、薪酬、博导资格等信息 |
| **Scan** | 搜索新目标院校，合并到主数据库 |
| **Draft Summary** | 为每所院校生成岗位分析摘要（优势/劣势/策略） |
| **Draft All** | 批量生成给 HR 和导师的邮件模板及 Cover Letter |

## 目录结构

```
job_hunting/
├── china_job_list.xlsx          # 主数据库（唯一来源）
├── china_job_list_apply_tracking.xlsx  # 申请追踪（仅手动维护）
├── src/                         # Python 脚本
│   ├── setup_check.py           # 数据校验
│   ├── fill_data.py             # 数据填充（网络爬取）
│   ├── generate_drafts.py       # 邮件 / Cover Letter 生成
│   ├── generate_full_scan.py    # 新院校搜索
│   └── add_specific_targets.py  # 手动添加目标院校
├── workflow/                    # 各阶段操作文档
├── scan/                        # 院校搜索结果（xlsx/md，git 忽略）
├── drafts/                      # 各院校申请材料（git 忽略）
├── materials/                   # 个人材料 PDF（git 忽略）
├── backups/                     # 自动备份（git 忽略）
└── sensitive_schools_list.md    # ⚠️ 高风险院校合规清单
```

## 依赖安装

```bash
pip install pandas openpyxl requests beautifulsoup4 tavily-python
```

环境变量（`.env` 文件，**不提交 git**）：
```
firecrawl_token=<your_token>
```

## 典型工作流

> 建议通过 Claude Code 交互执行，而非直接运行脚本。

### 1. 数据校验

```bash
python src/setup_check.py
```

检查列名规范、URL 格式、重复行。首次使用或修改主数据库后必须运行。

### 2. 填充职位信息

```bash
python src/fill_data.py
```

爬取每条职位的截止日期、职位描述、博导资格、联系方式等，输出
`china_job_list_{日期}_filled.xlsx`。

如只做校验不写入：
```bash
python src/fill_data.py --validate-only
```

### 3. 搜索新院校

```bash
python src/generate_full_scan.py
```

搜索 985 + HCI 方向强校，结果写入 `scan/`，合并后生成新版主数据库。

### 4. 生成分析摘要

由 Claude Code 处理：读取主数据库，为每所院校在 `drafts/{院校名}/summary.md`
生成包含以下内容的摘要：
- 岗位信息（方向、截止日期、链接）
- 实验室/导师背景
- 薪酬、博导资格、博生名额、海外人才政策
- 申请优势/风险/策略

### 5. 生成邮件 & Cover Letter

由 Claude Code 批量生成：
- `drafts/{院校}/{学院}/email_HR_inquiry_{学院}.md` — HR 咨询邮件
- `drafts/{院校}/email_Professor_{姓名}.md` — 导师联系邮件
- `drafts/{院校}/Cover_Letter/` — LaTeX 编译的 Cover Letter（需 `xelatex`）

## Excel 主数据库规范

| 列名 | 格式 | 说明 |
|------|------|------|
| `Deadline` | YYYY-MM-DD 或 Rolling | 截止日期 |
| `University&Department` | 清华大学-计算机系 | 院校+部门 |
| `Positions Link` | https://... | 职位详情页 |
| `Position Research Direction` | AI / HCI / HAI | 仅限这三类 |
| `OverseaPolicy` | 海外优青, 百人计划 | 海外人才政策 |
| `联系方式` | 微信:xxx, 邮箱:xxx | **优先微信** |
| `是否计划申请` | 是 / 否 | **仅手动维护，禁止脚本修改** |

## ⚠️ 重要注意事项

### 高风险院校合规
申请前必须对照 `sensitive_schools_list.md` 核查以下院校（涉及美签 PP10043 / 出口管制风险）：
- 国防七子：北航、哈工大、北理工、西工大、哈工程、南航、南理工
- 其他：北邮、国防科大、同济等

### 数据安全
- `china_job_list_apply_tracking.xlsx` 含申请意向，**操作前必须备份**
- `.env` 含 API 密钥，**禁止提交**
- `materials/` 含个人 PDF 材料，已加入 `.gitignore`

### 脚本执行顺序
```
setup → fill → scan → draft-summary → draft-all
```
各阶段有依赖关系，跳过上游步骤可能导致数据不一致。

### 网络请求
`fill_data.py` 内置 1.5 秒请求间隔以避免被封。如遇 403/429 错误，适当增加等待时间。
