# Job Application Form Filler

## 语言要求

**所有与用户的交互必须使用中文。** 包括提示、确认、错误信息、状态报告等。代码注释和变量名保持英文。

## 会话启动行为

**当检测到新会话开始时（system-reminder 中包含 SessionStart hook 输出），必须在第一次回复中主动执行以下操作：**

1. **向用户显示欢迎信息**，包括：
   - 系统名称和功能概述（智能表单自动填写、积累学习、安全保障）
   - 当前状态（Chrome 调试端口状态、当前打开的页面）
   - 主要使用方式（"帮我填写表单"、"启动持续填写"）

2. **检查系统状态**：
   - Chrome 调试端口是否已启动（`curl -s http://localhost:9222/json/version`）
   - 当前打开的标签页（`curl -s http://localhost:9222/json`）

3. **提示下一步操作（根据 Chrome 状态）**：

   **如果 Chrome 未启动：**
   ```
   📋 Chrome 调试端口未启动，需要先启动。

   我来帮你启动 Chrome 调试端口（命令会在后台运行）。
   启动后你可以在 Chrome 中：
   1. 打开要填写的申请页面
   2. 登录并导航到表单页面
   3. 回来告诉我"帮我填写表单"
   ```
   然后执行启动命令：`/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 &`

   **如果 Chrome 已启动但没有打开的标签页：**
   ```
   ✅ Chrome 调试端口已启动（端口 9222）
   📋 当前没有打开的标签页

   请在 Chrome 中：
   1. 打开要填写的申请页面
   2. 登录并导航到表单页面
   3. 回来告诉我"帮我填写表单"
   ```

   **如果 Chrome 已启动且有打开的标签页：**
   ```
   ✅ Chrome 已就绪（端口 9222）
   📄 当前页面：[页面标题] ([URL])

   准备好后告诉我：
   - "帮我填写表单" — 自动填写当前页面
   - "启动持续填写" — 填完后自动监控翻页并继续填写
   ```

**触发条件**：当 system-reminder 中包含 `SessionStart:startup hook success` 字样时。

**不要等用户主动询问，主动展示这些信息。**

## 核心架构

**Claude Code 本身就是匹配引擎。** 不依赖外部 Claude API 调用。

工作流程：
1. `python form_filler.py extract` → 提取页面字段 JSON
2. **Claude Code 读取 profile.yaml + materials/*.md，推理每个字段的匹配值**
3. Claude Code 生成填写指令 JSON，写入临时文件
4. `python form_filler.py apply /tmp/instructions.json` → 执行填写
5. 用户在 Chrome 中检查、手动修改
6. 用户点击下一页 → `python form_filler.py wait-and-learn` 自动学习 → 回到步骤 1

## 系统功能说明

本系统帮助你自动填写学术教职申请表单。**你只需通过 Claude Code 告诉我要做什么。** 主要功能：

### 功能 1：智能表单自动填写
- 连接你的 Chrome 浏览器（通过 CDP 调试端口），读取当前页面的所有表单字段
- **Claude Code 直接推理匹配**：读取 `profile.yaml`（含 learned_fields 和个人信息）和 `materials/*.md`（CV、研究/教学陈述等），为每个字段决定最佳值
- 支持标准输入框、原生下拉菜单、单选/复选框，以及 **自定义 JS 下拉组件**（如 PageUp 的 `pu-select`）

### 功能 2：积累学习，越用越准
- 填写后你可以在 Chrome 中手动修改任何字段
- **翻页时自动学习** — 你点击下一页后，系统自动读回所有字段值（包括你的修改）保存到 `learned_fields`
- 每次申请填得越多，后续申请需要手动操作的就越少

### 功能 3：安全保障
- **Label 不一致警告**：如果同一个字段名在不同网站对应不同含义，会提醒确认
- **隐藏字段过滤**：页面上不可见的条件字段不会被提取或填写
- **填不了就不填**：无法确定的字段不会乱填，留给用户在浏览器手动补充

---

## 使用指南

> **每次用户执行完一步操作后，必须告知下一步要做什么以及为什么。**
>
> **用户通过 Claude Code 与系统交互，不需要手动运行 Python 命令。**
>
> **不在聊天中问用户输入字段值 — 填不了的让用户在浏览器手动填。**

### 第 0 步：启动 Chrome 调试端口

**做什么：** 我会检查 Chrome 调试端口是否已启动。如未启动，我会帮你启动。

**为什么：** 系统需要通过 CDP（Chrome DevTools Protocol）连接你的浏览器，才能读取和操作页面表单。

**下一步：** 在 Chrome 中打开要填写的申请页面，登录后导航到表单页面，然后告诉我"**帮我填写表单**"。

---

### 第 1 步：自动填写当前页面

**用户说：** "帮我填写表单" / "填写当前页面" / "开始填写"

**我会做什么：**
1. 执行 `python form_filler.py extract` 提取页面所有字段
2. 读取 `profile.yaml` 和 `materials/*.md`
3. 用我的推理能力为每个字段匹配最佳值（参考下方"字段匹配指引"）
4. 生成填写指令写入 `/tmp/instructions.json`
5. 执行 `python form_filler.py apply /tmp/instructions.json` 填写
6. **重新提取并检查是否有新展开的字段**（见下方"条件展开字段处理"）

**填写原则：尽量填写所有字段。** 除非 profile.yaml 和 materials 中确实没有任何相关信息，否则应该通过推理给出合理值。宁可填了让用户在浏览器修改，也不要留空让用户手动输入。

**每轮填写后必须输出汇总报告：**

```
📋 本轮填写汇总（共 X 个字段）

已填写（Y 个）：
  ✓ 字段名 → 值
  ✓ 字段名 → 值
  ⚠ 字段名 → 值    ← 建议检查：[原因，如"最接近的选项，不完全匹配"]

未填写（Z 个）：
  ✗ 字段名 — 原因（如"无相关信息"/"readonly 搜索字段需手动"）

🔍 建议重点检查：
  - 字段名：[为什么信心较低]
```

**信心标记规则：**
- `✓` — 高信心：来自 learned_fields 精确匹配或 profile 中有明确对应值
- `⚠` — 低信心：通过推理得出但不确定、选项中没有精确匹配只有近似值、或从 materials 中拼凑
- `✗` — 未填：确实无信息

**下一步：** 去 Chrome 中重点检查 ⚠ 标记的字段，手动补充 ✗ 字段。改完后直接点击"下一页"。

---

### 第 2 步：翻页（自动学习 + 继续填写）

**用户说：** "下一页了" / "继续" / "我点了下一页"

**我会做什么：**
1. 执行 `python form_filler.py learn` 读回当前页面值（捕获你的手动修改）
2. 回到第 1 步，对新页面执行同样的流程

**为什么自动学习很重要：**
- 你修正的值 → 下次会用修正后的值
- 你新填的字段 → 下次自动填写
- 你主动留空的字段 → 下次不再填

---

### 持续填写模式

**用户说：** "启动持续填写" / "持续填写" / "开始watch" / "启动watch"

**工作流程：**

**第一次启动时，我会：**
1. extract → 推理匹配 → apply 填写当前页面
2. **重新 extract 检查条件展开的新字段** → 如有新字段则继续匹配 → apply（循环直到无新字段）
3. 输出填写汇总报告
4. 告诉用户："请检查并点击下一页"
5. 通过 **Task agent** 启动 `python form_filler.py wait-and-learn`，等待翻页

**翻页后自动执行：**
6. wait-and-learn 检测到翻页 → 自动学习当前页面值（保存 learned_fields）→ 输出新页面 URL
7. 我提取新页面字段 → 推理匹配 → apply 填写
8. 回到步骤 3，循环执行
9. 用户说"停"时，停止 agent

**重要：使用 Task agent 执行 wait-and-learn**
- **必须通过 Task tool 启动 Bash agent**，不能直接用 Bash tool
  ```python
  Task(
    subagent_type="Bash",
    description="等待翻页并学习",
    prompt="执行 python form_filler.py wait-and-learn，等待用户点击下一页，然后学习当前页面的字段值"
  )
  ```
- 这样用户可以进入子任务查看实时输出（等待翻页提示、学习过程、新页面 URL）
- agent 完成后（翻页+学习完成），我会自动填写新页面，然后启动新的 wait-and-learn agent

---

## 启动检查清单

每次启动会话时执行：

1. **检查 Chrome 调试端口**：`curl -s http://localhost:9222/json/version`
2. **如未启动**，启动 Chrome：
   ```
   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 &
   ```
3. **检查当前标签页**：`curl -s http://localhost:9222/json`，告诉用户当前打开的页面
4. **提醒用户**："Chrome 已就绪。请打开要填写的申请页面并登录，准备好后告诉我。"

---

## 条件展开字段处理（重要！）

某些表单字段（特别是自定义下拉 `custom-select`）在选择值后会**动态展开新的子字段**。例如：
- 选择 "Type of education: Tertiary" → 展开 Degree type、Discipline、Institution、Country、Education status 等字段
- 选择某个分类选项 → 展开该分类下的详细字段

**必须执行的流程：**

1. 第一轮 extract → 匹配 → apply（填写当前可见的所有字段）
2. **立即重新 extract**，对比第一轮的字段列表
3. 如果出现新字段（selector 不在第一轮中）→ 为新字段匹配值 → 再次 apply
4. 重复步骤 2-3，直到没有新字段出现

**注意事项：**
- 每轮 apply 后都可能触发新的条件字段，必须循环检查
- 不要假设一轮 extract-apply 就能填完所有字段
- 对于教育经历等重复区块（education 1/2/3），先选类型展开子字段，再填具体值
- `extract` 输出的 JSON 可能很大（如 discipline 有 305 个选项），用脚本过滤而非直接读取全部

---

## 字段匹配指引（Claude Code 推理用）

当拿到 `extract` 输出的字段列表后，按以下规则为每个字段决定值：

### 匹配优先级

1. **`learned_fields`（最高优先级）** — `profile.yaml` 中 `learned_fields` 部分
   - 用字段 label 的 sanitized key（小写、去标点、snake_case、截断 40 字符）查找
   - value 为空字符串 `""` → **跳过该字段**（用户刻意留空，不填也不放入指令）
   - value 非空 → 使用该值
   - 如果 learned_fields 中的 label 与当前字段 label 差异大，在输出中提醒用户确认

2. **profile.yaml 结构化数据** — 个人信息、地址、教育、工作经历等
   - 根据字段 label 语义匹配到 profile 中对应的值

3. **materials/*.md** — CV、研究陈述、教学陈述等
   - 对于要求长文本描述的字段（如 research interests、teaching philosophy），从 materials 中提取或组合

4. **尽力推理填写** — 即使没有精确匹配，也应通过推理给出最合理的值（标记为 ⚠ 低信心）
5. **确实填不了 → 不填** — 只有 profile/materials 中完全没有相关信息时才不填，并说明原因

### 生成指令格式

将匹配结果写入 `/tmp/instructions.json`：

```json
{
  "auto_fill": [
    {"selector": "#first-name", "value": "John", "action": "fill", "label": "First Name"},
    {"selector": "#country", "value": "AU", "action": "select", "label": "Country"},
    {"selector": "input[name='gender']", "value": "male", "action": "check", "label": "Gender"},
    {"selector": "#title-edit", "value": "Dr", "action": "custom-select", "label": "Title", "listbox_id": "title-list"},
    {"selector": "#major_1Text", "value": "Information Systems", "action": "search-select", "label": "Major:", "hidden_id": "major_1"}
  ]
}
```

### action 规则

| 字段类型 | tag/type | action | value 要求 |
|---------|----------|--------|-----------|
| 文本输入框 | input[type=text], textarea | `"fill"` | 直接填入的文本 |
| 原生下拉 | select | `"select"` | **必须是 options 中的 value 属性**（不是 text） |
| 单选/复选框 | input[type=radio/checkbox] | `"check"` | **必须是 options 中的 value 属性** |
| 自定义下拉 | custom-select | `"custom-select"` | options 中的 value 属性，**必须带 listbox_id** |
| 搜索弹窗字段 | search-select | `"search-select"` | 搜索关键词文本，**必须带 hidden_id**（从 extract 输出获取） |

**search-select 注意事项：**
- 搜索词应简短（如机构英文短名），过长可能无结果
- 搜索无结果时会自动 fallback 到手动输入模式（勾选"Didn't find"复选框 + 填入文本）
- 支持两种弹窗：`SearchDialog.aspx`（Major、Company 等）和 `SelectUniDialog.aspx`（Institution）

### 关键注意事项

- **select/radio/checkbox 的 value 必须来自 options 列表中的 value 属性**，不能随意填写
- 已有 `current_value` 且正确 → 跳过，不放入指令
- 字段有 `required: true` 但填不了 → 仍然不填，告诉用户
- 对于 email 类型字段，确保格式正确
- 对于 tel 类型字段，使用国际格式

---

## learned_fields 格式

```yaml
learned_fields:
  title:
    value: Dr           # 字段值（空字符串表示刻意留空）
    label: "Title:*"    # 原始字段标签（用于不一致检测）
  second_nationality:
    value: ""           # 用户主动留空，下次跳过
    label: "Second nationality:"
```

## 自定义下拉组件 (pu-select)

PageUp 等网站使用自定义 JS 下拉组件（`div.pu-select`），非原生 `<select>`。提取器通过检测 `.pu-select` 容器和 listbox 获取选项。填写器点击打开下拉再选择选项。

## 文件说明

| 文件 | 用途 |
|------|------|
| `profile.yaml` | 结构化个人信息 + `learned_fields`（每个字段的值和标签） |
| `materials/*.md` | CV、研究陈述、教学陈述等（Claude Code 推理上下文） |
| `form_filler.py` | CLI 主入口：`extract`、`apply`、`wait-and-learn`、`fill`、`learn`、`watch` 命令 |
| `browser.py` | Playwright CDP 连接 Chrome |
| `field_extractor.py` | 从页面 DOM 提取表单字段（标准 + 自定义下拉） |
| `llm_matcher.py` | 保留供参考，不再使用 |
| `llm_matcher_local.py` | 本地规则匹配（`fill` 命令的 fallback） |
| `profile_store.py` | profile.yaml 读写 |

## 命令执行说明

| 用户说... | 我执行的命令 | 说明 |
|----------|------------|------|
| "帮我填写表单" | ① `python form_filler.py extract` → ② 我推理匹配 → ③ `python form_filler.py apply /tmp/instructions.json` | 提取 → 推理 → 填写 |
| "下一页了" / "继续" | ① `python form_filler.py learn` → ② 重复填写流程 | 学习修改 → 填新页面 |
| "启动持续填写" / "填写当前页面并watch" | 循环：extract → 推理 → apply → `python form_filler.py watch`（**前台运行，实时输出**） | 持续监控模式 |
| "学习我的修改" | `python form_filler.py learn` | 手动触发学习 |

**Watch 模式执行要求：**
- **禁止**使用 `run_in_background=true` 参数
- **必须**让用户看到 watch 命令的实时输出
- **必须**在输出中明确告知用户当前状态（等待翻页、学习中、提取中、填写中）
- 如果用户需要查看进度，应该能从输出中直接看到，而不是读取后台日志文件

## 修改代码时注意

- 新增规则匹配字段：编辑 `llm_matcher_local.py` 的 `_RULES` 列表
- 新增自定义下拉类型：扩展 `field_extractor.py` 中 JS 的 "Custom pu-select dropdowns" 部分
- `profile.yaml` 含个人信息，不要提交到 git
