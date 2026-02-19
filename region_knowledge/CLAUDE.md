# Region Knowledge -- 全球教职申请区域知识库

## 定位

独立子模块，管理全球各地区和学校的教职申请规则、文化、策略知识。

**被谁使用：**
- `overseas_pipeline/` Step 2 (Fit Analysis): 读取地区卡 + 学校卡，分析匹配度
- `overseas_pipeline/` Step 3 (Materials Customization): 读取规则卡，指导材料定制
- 未来可独立为"全球教职申请知识库"产品

## 双层知识架构

```
regions/{region}.md   → 地区通用规则（14 张）
    ↓ 默认继承
schools/{school}.md   → 学校特有 + 覆盖 + 历史经验（随使用积累）
```

使用时先读地区卡，再用学校卡做覆盖。学校卡只记录与地区卡不同的部分 + 学校特有信息。

## 知识来源

**短期（当前）：**
- 从 `general/research_job_rules/` 下的 DeepResearch 文档蒸馏
  - `海外教职申请机制与策略.md`（英/澳/DACH/荷/加）
  - `亚洲及中东教职招聘分析.md`（中/港/新/日/韩/中东/澳门/新西兰/马来）
- 原始链接轻验证

**长期（多源自动化）：**
- 大学 HR 页面、招聘指南（定期爬取）
- 申请实战反馈（事件驱动）
- 社区信息：Academia SE, Reddit, CS hiring wiki（搜索验证）
- 官方政策变更：ARC/EPSRC/NSERC 等官网（定期检查）

## 地区规则卡列表

| 文件 | 地区 | 状态 |
|------|------|------|
| `regions/australia.md` | 澳大利亚 | verified (2026-02-18) |
| `regions/uk.md` | 英国 | draft (部分验证, 2026-02-18) — 2/7 无法访问 |
| `regions/hong_kong.md` | 香港 | draft (已验证, 2026-02-18) |
| `regions/singapore.md` | 新加坡 | draft (已验证, 2026-02-18) |
| `regions/japan.md` | 日本 | draft (已验证, 2026-02-18) |
| `regions/korea.md` | 韩国 | draft (已验证, 2026-02-18) |
| `regions/macau.md` | 澳门 | draft (已验证, 2026-02-18) |
| `regions/canada.md` | 加拿大 | draft (已验证, 2026-02-18) |
| `regions/dach.md` | 德国/奥地利/瑞士 | draft (已验证, 2026-02-18) |
| `regions/netherlands_nordics.md` | 荷兰/北欧 | draft (已验证, 2026-02-18) |
| `regions/uae.md` | 阿联酋 | draft (已验证, 2026-02-18) |
| `regions/saudi.md` | 沙特 | draft (已验证, 2026-02-18) |
| `regions/new_zealand.md` | 新西兰 | draft (已验证, 2026-02-18) |
| `regions/china_mainland.md` | 中国大陆 | draft (已验证, 2026-02-18) |
| `regions/usa.md` | 美国 | draft (完整验证, 2026-02-19) |
| `regions/france.md` | 法国 | draft (待验证, 2026-02-19) |
| `regions/belgium.md` | 比利时 | draft (待验证, 2026-02-19) |
| `regions/italy.md` | 意大利 | draft (待验证, 2026-02-19) |
| `regions/spain.md` | 西班牙 | draft (待验证, 2026-02-19) |
| `regions/ireland.md` | 爱尔兰 | draft (待验证, 2026-02-19) |
| `regions/portugal.md` | 葡萄牙 | draft (待验证, 2026-02-19) |

## 学校知识卡列表

| 文件 | 学校 | 地区 | 状态 |
|------|------|------|------|
| `schools/monash_university.md` | Monash University | australia | draft (2026-02-19，Step 1 首次生成) |

## 链接验证标准

### 验证工具
使用 `src/web_fetch.py` 三层 fallback 策略（Tavily API Key 内嵌）。

### 验证状态判定逻辑

| 获取层 | 方式 | 标注 | 理由 |
|-------|------|------|------|
| Layer 1: curl | 直接 HTTP 请求 + 浏览器 User-Agent | **已验证** | 直接从源 URL 获取原始内容 |
| Layer 2: Tavily Extract | Tavily headless 浏览器访问**同一 URL** | **已验证** | 虽然绕过了 Cloudflare JS Challenge，但内容来自源 URL，等同于直接访问 |
| Layer 3: Tavily Search | 搜索引擎索引，非直接访问源 URL | **间接验证** | 未从源 URL 获取内容，而是通过搜索确认信息存在 |
| 全部失败 | 三层均无法获取 | **待验证** | 无法确认链接可达性或内容准确性 |

**核心原则**: Layer 1 和 Layer 2 的区别仅是绕过防火墙的技术手段不同，都是从**同一个 URL 获取同一份内容**，因此验证等级相同。只有 Layer 3（搜索）因为不直接访问源 URL，才标注为"间接验证"。

### 内容对齐验证（必须执行）

**仅确认链接可达是不够的**。每次验证必须记录：

1. **What — 原文摘录**: 从获取的页面中摘录与规则卡论断直接相关的原文段落（英文原文，不翻译）
2. **Why — 对齐说明**: 说明该原文如何支撑规则卡中的具体论断，引用规则卡的具体章节/行

#### 验证记录格式（写入 verification_log.md）

```
- R1 (来源名): **已验证** ✓ (Layer X)
  - **规则卡论断**: [规则卡中引用了 R1 的具体说法，如"Selection Panel 必须性别平衡"]
  - **原文摘录**: "[从源页面提取的英文原文片段]"
  - **对齐**: [原文如何支撑论断的简要说明]
```

#### 示例（好的验证记录）

```
- R20 (VU Policy): **已验证** ✓ (Layer 1)
  - **规则卡论断**: "Selection Panel 必须性别平衡" (australia.md §2)
  - **原文摘录**: "The panel must consist of two selection panel members and gender balance is required" (Clause 24)
  - **对齐**: Clause 24 原文直接确认了性别平衡要求，与规则卡描述完全一致
```

```
- R3 (UBC EDI Rubric): **已验证** ✓ (Layer 2)
  - **规则卡论断**: "EDI 声明评分维度含 Knowledge / Track Record / Future Plans 三项" (canada.md §3.5)
  - **原文摘录**: "Rubric dimensions: (1) Knowledge about EDI, (2) Track Record of EDI activities, (3) Plans for EDI contributions. Each scored as Excellent / Average / Low."
  - **对齐**: PDF 内容确认三维度评分框架和分级标准，与规则卡描述一致
```

#### 反面示例（不合格的验证记录）

```
# 不合格 — 仅确认链接可达，未验证内容
- R1 (KAUST Faculty Positions): **已验证** ✓ (Layer 1)
  - 页面存活，标题正确

# 不合格 — 摘录了原文但没有说明与规则卡哪条论断对齐
- R2 (Korea Times): **已验证** ✓ (Layer 1)
  - **原文摘录**: "SNU's foreign faculty face barriers in Korea's insider-dominated academia"
```

## 知识生命周期

### 知识状态
```
[draft] → [verified] → [needs_review] → [verified]
                             ↑
                     事件触发（发现不一致）
```

### 更新触发机制（事件驱动）

| 事件 | 触发场景 | 动作 |
|------|---------|------|
| **规则冲突** | overseas_pipeline Step 2 处理某校时，JD 与地区卡不符 | **暂停流水线**，显式提醒用户选择处理方式 |
| **手动标记** | 用户发现某条规则不对 | 运行"标记待验证"命令 |
| **链接失效** | 验证时发现 source 链接 404 | 搜索替代来源，更新或标记不确定 |
| **申请回写** | 某校申请完成后 | 更新学校卡申请历史，如有通用发现更新地区卡 |

### 规则冲突处理（关键：必须暂停提醒）

```
overseas_pipeline Step 2 发现规则冲突
    ↓
⚠ 立即暂停流水线，向用户显示：
  - 地区卡的规则（含 source 链接）
  - 该校 JD 的实际要求（含 URL）
  - 处理选项：
    A. 以该校 JD 为准（本次），更新学校卡
    B. 以该校 JD 为准，同时标记地区卡 needs_review
    C. 忽略冲突，仍按地区卡执行
    ↓
用户选择后 → 记录 → 继续流水线
```

**核心原则：冲突时不能静默处理，不能用可能错误的规则生成材料。**

## 用户命令

### "验证规则卡 {地区}"
1. 读取该地区规则卡
2. 检查 `needs_review` 列表中的条目
3. 对每条待验证规则：
   - 使用 `src/web_fetch.py` 访问原始 source 链接
   - 如 404 → 搜索替代来源
   - 如内容变化 → 更新规则，标注新 source
   - 如确认无误 → 清除 needs_review
4. **内容对齐验证**（关键步骤，不可省略）：
   - 对每个成功获取的链接，找到页面中与规则卡论断相关的原文段落
   - 在 `verification_log.md` 中按照"内容对齐验证"格式记录：规则卡论断 + 原文摘录 + 对齐说明
   - 如果源页面内容与规则卡论断**不一致**，立即标记 `needs_review` 并更新规则卡
5. 更新引用索引表中的验证状态和 `last_verified` 日期
6. 记录变更到 `verification_log.md`

### "更新规则卡 {地区}"
1. 搜索该地区最新的教职招聘政策变化
2. 检查 DeepResearch 文档中的引用链接是否有更新
3. 整合新信息到规则卡
4. 记录变更到 `verification_log.md`

### "新建规则卡 {地区}"
1. 检查 DeepResearch 文档中是否有该地区内容
2. 如有，蒸馏为规则卡格式
3. 如无，搜索该地区教职招聘机制信息
4. 创建新规则卡，标注所有 source 链接

### "标记待验证 {地区} {规则描述}"
1. 在该地区卡的 `needs_review` 列表中追加条目
2. 记录到 `verification_log.md`

### "查看验证日志"
1. 显示 `verification_log.md` 近期变更

## 与 overseas_pipeline 的交互

### 读取顺序（Step 2 使用时）
```
1. 确定学校所在 region
2. 读取 regions/{region}.md
3. 检查 schools/{school}.md 是否存在
   - 如存在 → 读取，用学校卡覆盖地区卡的差异部分
   - 如不存在 → 仅用地区卡
4. fit_report 中标注使用了哪些规则卡
```

### 回写（知识积累）
```
Step 1 处理学校时 → 创建/更新 schools/{school}.md
Step 2 发现冲突时 → 更新学校卡 / 地区卡 needs_review
申请完成后     → 更新 schools/{school}.md 申请历史
```

## 质量要求
- 每条规则必须标注 source（URL 或本地文件路径 + 行号）
- 不确定的信息标注 `[需验证]`
- 过时信息移入 `needs_review` 而非直接删除
- 学校卡中的决策人必须附 主页 URL 和 Google Scholar URL
