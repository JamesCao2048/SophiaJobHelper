# job_filling — AI 驱动的申请表单自动填写系统

通过 Chrome CDP 连接浏览器，由 Claude Code 直接推理匹配，自动填写学术教职申请表单，并随使用积累学习记忆。

## 核心设计

**Claude Code 本身是匹配引擎**——不调用外部 API，直接读取 `profile.yaml` 和 `materials/*.md`，推理每个字段的最佳填写值，生成指令后由 Python 脚本执行填写。

```
extract（提取字段）→ Claude Code 推理匹配 → apply（执行填写）→ 用户校对 → learn（学习修改）
```

## 依赖安装

```bash
pip install -r requirements.txt
# 主要依赖：playwright, pyyaml, pymupdf
playwright install chromium
```

## 快速开始

### Step 0：启动 Chrome 调试端口

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 &
```

然后在 Chrome 中打开目标申请页面并登录，导航到表单页面。

### Step 1：准备个人材料

- `profile.yaml`：个人信息（姓名、地址、教育经历、工作经历等）
- `materials/`：将 PDF 材料转为 Markdown（供 Claude Code 读取）

```bash
python pdf_to_md.py materials/CV.pdf          # 转换 PDF → MD
```

### Step 2：填写表单（通过 Claude Code）

打开 Claude Code，告诉它：**"帮我填写表单"**

Claude Code 会依次执行：
```bash
python form_filler.py extract        # 提取当前页面所有字段
# Claude Code 读取字段 + profile + materials，推理匹配，写入 /tmp/instructions.json
python form_filler.py apply /tmp/instructions.json   # 执行填写
```

填写后 Claude Code 输出汇总报告：
```
✓  高信心（来自记忆或 profile 精确匹配）
⚠  低信心（推理得出，建议检查）
✗  未填写（确实无相关信息）
```

### Step 3：校对与翻页

在 Chrome 中检查并手动修正字段，然后点击"下一页"。

告诉 Claude Code：**"下一页了"**，它会自动学习你的修改并填写新页面。

### Step 4：持续填写模式

```
告诉 Claude Code："启动持续填写"
```

系统自动循环：填写 → 等待翻页 → 学习修改 → 填写下一页，无需手动干预。

## CLI 命令参考

```bash
python form_filler.py extract                    # 提取当前页面字段 → JSON 输出
python form_filler.py apply /tmp/instructions.json  # 按指令填写
python form_filler.py learn                      # 读回当前页面值，保存到 profile.yaml
python form_filler.py wait-and-learn             # 等待翻页后自动学习（持续监控）
python form_filler.py fill                       # 本地规则匹配 + 填写（不依赖 Claude Code）
python form_filler.py watch                      # 持续监控模式（fill 命令版）
```

## profile.yaml 结构

```yaml
personal:           # 姓名、邮箱、电话、网站、ORCID
address:            # 通讯地址
current_position:   # 当前职位与机构
education:          # 教育经历列表
work_experience:    # 工作经历列表
references:         # 推荐人信息
research_interests: # 研究方向（primary/secondary/tertiary）
honors:             # 荣誉奖项

learned_fields:     # 积累学习记录（自动更新）
  field_key:
    value: "填写的值"   # "" 表示刻意留空，下次跳过
    label: "字段标签"   # 原始标签，用于跨网站一致性检测
```

`learned_fields` 优先级最高，随每次申请自动积累。

## 支持的字段类型

| 字段类型 | action 值 | 说明 |
|---------|-----------|------|
| 文本输入框 / 文本域 | `fill` | 直接输入文本 |
| 原生下拉 `<select>` | `select` | 必须使用 options 中的 value 值 |
| 单选 / 复选框 | `check` | 必须使用 options 中的 value 值 |
| 自定义 JS 下拉（PageUp pu-select） | `custom-select` | 需提供 `listbox_id` |
| 搜索弹窗（机构/专业查找） | `search-select` | 需提供 `hidden_id`，搜索词宜简短 |

## 注意事项

**条件展开字段**：选择某些字段（如教育类型）后会动态出现子字段。每次 apply 后需重新 extract，循环直到没有新字段出现。

**个人数据保护**：
- `profile.yaml` 含个人信息，已加入 `.gitignore`，**禁止提交**
- `materials/` 同样已忽略

**Chrome 连接**：
- 端口 9222 必须在运行前空闲
- CDP 断开不会关闭用户的 Chrome，可随时重连

**select/radio/checkbox 填写**：value 必须来自 extract 输出的 options 列表，不能自行填写文字。

**search-select 字段**：搜索词用简短英文缩写（如 "MIT" 而非全称），无结果时自动 fallback 为手动输入模式。

## 文件说明

| 文件 | 用途 |
|------|------|
| `form_filler.py` | CLI 主入口 |
| `field_extractor.py` | 从 DOM 提取表单字段 |
| `profile_store.py` | profile.yaml 读写工具 |
| `browser.py` | Playwright CDP 连接封装 |
| `llm_matcher_local.py` | 本地规则匹配（`fill` 命令 fallback） |
| `pdf_to_md.py` | PDF → Markdown 转换工具 |
| `profile.yaml` | 个人资料 + 学习记忆（本地保留，不提交） |
| `materials/*.md` | 材料文档（Claude Code 推理上下文） |
