# Region Knowledge -- 全球教职申请区域知识库设计文档

> 日期: 2026-02-18
> 状态: Draft
> 作者: James + Claude Code brainstorm
> 关联: `2026-02-18-overseas-pipeline-design.md`

---

## 一、定位

独立子模块，管理全球各地区和学校的教职申请规则、文化、策略知识。

**被谁使用：**
- `overseas_pipeline/` Step 2 (Fit Analysis): 读取地区卡 + 学校卡，分析匹配度
- `overseas_pipeline/` Step 3 (Materials): 读取规则卡，指导材料定制
- 未来可独立为 "全球教职申请知识库" 产品

**核心价值：**
将分散在研究报告、网页、申请经验中的"隐性知识"结构化、可验证、可持续更新。

---

## 二、双层知识架构

### 继承关系

```
region card (地区通用规则)
    ↓ 默认继承
school card (学校特有 + 覆盖 + 历史经验)
```

学校卡只记录与地区卡不同的部分 + 学校特有信息。使用时先读地区卡，再用学校卡做覆盖。

### 内容分层

| 内容 | 地区卡 | 学校卡 |
|------|--------|--------|
| 职级体系 | 通用规则 | 如有差异才记录 |
| 决策人 | 通用角色描述 | **具体人名 + 主页/Scholar 链接** |
| 材料格式 | 通用要求 | **该校特有格式差异** |
| 招聘流程 | 通用流程 | **该校特有步骤** |
| HCI group | 通用定位 | **具体 faculty 和研究组** |
| 课程信息 | 无 | **该校 CS 课程列表** |
| 申请历史 | 无 | **Sophia 申请该校的经验** |
| Grant 信息 | 地区资助体系 | 该校特有资助机会 |

---

## 三、目录结构

```
region_knowledge/
├── CLAUDE.md                # 模块定义和 workflow
├── verification_log.md      # 所有变更的审计日志
├── regions/                 # 地区规则卡（14 张）
│   ├── australia.md
│   ├── uk.md
│   ├── hong_kong.md
│   ├── singapore.md
│   ├── japan.md
│   ├── korea.md
│   ├── macau.md
│   ├── canada.md
│   ├── dach.md              # 德/奥/瑞（差异小，合并）
│   ├── netherlands_nordics.md  # 荷兰/北欧（差异小，合并）
│   ├── uae.md               # 阿联酋 (MBZUAI, NYU Abu Dhabi)
│   ├── saudi.md             # 沙特 (KAUST)
│   ├── new_zealand.md
│   └── china_mainland.md
└── schools/                 # 学校知识卡（随使用积累）
    ├── university_of_melbourne.md
    ├── university_of_sydney.md
    └── ...（Step 1 处理学校时自动创建）
```

### 地区划分原则
- 招聘文化差异显著的国家/地区独立成卡
- 差异较小的国家可合并（如 DACH、荷兰+北欧）
- 现有 14 个地区覆盖 Sophia 的目标市场

---

## 四、地区规则卡 Schema

```markdown
# {地区名} 教职申请规则卡

## 元信息
- region_id: {snake_case}
- last_verified: YYYY-MM-DD
- status: draft | verified
- source_documents:
  - {本地文件路径 + 行号}
- needs_review: []

---

## 1. 职级术语映射
| 当地职称 | ≈ 美国等级 | 薪资范围 | 说明 | source |

---

## 2. 关键决策人与招聘流程

### 决策链
| 阶段 | 决策人 | 看什么 | source |

### 隐形否决者
- {谁有实质否决权，看什么}

---

## 3. 申请材料要求

### 3.1 Cover Letter
- 格式 / 写法 / 长度 / 称呼

### 3.2 CV
- 格式差异

### 3.3 Research Statement
- 侧重点 / 必须提及的 grant scheme

### 3.4 Teaching Statement
- 证据要求 / 格式

### 3.5 特色材料
- 该地区特有的必须提交材料

### 3.6 通常不需要
- 该地区一般不要求的材料

---

## 4. 评审重点

### 最看重
### HCI 会议论文认可度
### Grant 期望

---

## 5. Cover Letter 策略
- 开头定调 / Faculty 提及方式 / 禁忌

---

## 6. Sophia 特有优势/风险

### 优势
### 风险

---

## 引用索引
| ID | 来源 | URL |
```

---

## 五、学校知识卡 Schema

```markdown
# {学校名} 知识卡

## 元信息
- school_id: {snake_case}
- region: {region_id}  ← 继承自 regions/{region_id}.md
- created: YYYY-MM-DD
- last_updated: YYYY-MM-DD
- status: draft | verified

---

## 1. 基本信息
- 全称 / 院系 / 院系主页 / 招聘页 / QS CS 排名

---

## 2. 关键决策人
| 角色 | 姓名 | 研究方向 | 主页 | Google Scholar | 备注 |

---

## 3. 与地区卡的差异（覆盖规则）
<!-- 只记录与 {region_id}.md 不同的部分 -->

---

## 4. HCI Group 信息
<!-- 来自 overseas_pipeline Step 1 -->

---

## 5. 课程信息
<!-- Teaching Statement 定制用 -->
| 课程代码 | 课程名 | 与 Sophia 教学能力匹配 |

---

## 6. 申请历史
<!-- Sophia 申请该校的经验记录 -->
```

---

## 六、知识生命周期

### 知识状态

```
[draft] → [verified] → [needs_review] → [verified]
                             ↑
                     事件触发（发现不一致）
```

### 短期策略（当前）
1. 从 DeepResearch 文档蒸馏 → 地区卡初始版本 (draft)
2. 原始链接轻验证 → 确认关键规则有效 (verified)
3. overseas_pipeline Step 1 处理学校时 → 自动创建学校卡 (draft)

### 长期策略（多源自动化）

| 来源类型 | 具体来源 | 获取方式 |
|---------|---------|---------|
| 学术招聘政策文档 | 大学 HR 页面、招聘指南 | 定期爬取 |
| 研究报告 | DeepResearch 新版本 | 手动触发 |
| 申请实战反馈 | Sophia 申请过程中的发现 | 事件驱动 |
| 社区信息 | Academia SE, Reddit, CS hiring wiki | 搜索验证 |
| 官方政策变更 | ARC/EPSRC/NSERC 等官网 | 定期检查 |

---

## 七、验证机制（事件驱动）

### 触发事件

| 事件 | 触发场景 | 动作 |
|------|---------|------|
| **规则冲突** | Step 2 处理某校时，JD 要求与地区卡不符 | **暂停流水线**，显式提醒用户，等用户判断后再继续 |
| **手动标记** | 用户发现某条规则不对 | 运行"标记待验证 {地区} {规则描述}" |
| **链接失效** | 验证时发现 source 链接 404 | 搜索替代来源，更新或标记不确定 |

### 规则冲突处理流程（关键）

```
Step 2 发现规则冲突
    ↓
⚠ 立即暂停，向用户显示：
  - 地区卡说什么（含 source 链接）
  - 该校 JD 实际要求什么（含 URL）
  - 建议处理选项：
    A. 以该校 JD 为准（本次），更新学校卡
    B. 以该校 JD 为准，同时标记地区卡待验证
    C. 忽略，仍按地区卡执行
    ↓
用户选择后：
  - 记录到学校卡 / 地区卡 needs_review
  - 记录到 verification_log.md
  - 继续流水线
```

**核心原则：冲突时不能静默处理，必须暂停等用户判断，不能用错误规则生成材料。**

### 验证 workflow

```
用户: "验证规则卡 {地区}"

Claude Code:
1. 读取该地区规则卡
2. 检查 needs_review 列表
3. 对每条待验证规则:
   - 访问原始 source URL → 确认是否仍有效
   - 如 404 → 搜索替代来源
   - 如内容变化 → 更新规则，标注新 source
   - 如确认无误 → 清除 needs_review
4. 检查 sources 中所有链接可达性
5. 更新 last_verified 日期
6. 记录变更到 verification_log.md
```

---

## 八、与 overseas_pipeline 的交互

### Step 2 (Fit Analysis) 读取顺序
```
1. 确定学校所在 region
2. 读取 regions/{region}.md
3. 检查 schools/{school}.md 是否存在
   - 如存在 → 读取，用学校卡覆盖地区卡的差异部分
   - 如不存在 → 仅用地区卡
4. 生成 fit_report 时标注使用了哪些规则卡
```

### Step 1 (Research) 回写
```
Step 1 处理学校时：
1. 爬取学校信息
2. 创建/更新 schools/{school}.md
   - 填入基本信息、决策人、HCI Group、课程信息
3. 如发现地区通用的新知识 → 建议更新 regions/{region}.md
```

### 申请完成后回写
```
申请某校后（无论结果）：
1. 更新 schools/{school}.md 的"申请历史"
2. 记录经验教训（什么有效、什么没用）
3. 如发现地区规则需修正 → 更新 regions/{region}.md
```

---

## 九、CLAUDE.md 命令定义

| 命令 | 功能 |
|------|------|
| "验证规则卡 {地区}" | 检查 needs_review，访问链接验证，更新规则 |
| "更新规则卡 {地区}" | 搜索最新信息，整合到规则卡 |
| "新建规则卡 {地区}" | 从 DeepResearch 文档或网络搜索创建新卡 |
| "标记待验证 {地区} {描述}" | 手动添加 needs_review 条目 |
| "查看验证日志" | 显示 verification_log.md 近期变更 |

---

## 十、实施计划

### Phase 1（本周）
1. 创建目录结构和 CLAUDE.md
2. 蒸馏 australia.md（最急需，Sophia 正在投澳洲）
3. 蒸馏 uk.md（Edinburgh, King's College 待投）
4. 蒸馏 hong_kong.md（大量 pending 申请）

### Phase 2（第 2-3 周）
5. 蒸馏 singapore.md, canada.md, new_zealand.md
6. 用 overseas_pipeline 实际处理几所学校，测试双层继承
7. 根据实测迭代 schema

### Phase 3（长期）
8. 补全剩余地区卡
9. 建立多源自动化采集能力
10. 积累学校卡，形成知识库资产
