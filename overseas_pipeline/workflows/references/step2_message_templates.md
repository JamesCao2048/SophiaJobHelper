# Step 2 消息模板

> **参考文件** — 由 workflow 步骤引用，不可独立执行。
> **引用方**：`workflows/step2_analysis.md` step 5/7

---

## 页数偏差警示区块（step2_summary.md 顶部）

**当 JD 指定与默认值不同的页数时，在 step2_summary.md 顶部插入此区块（让用户在开始 Step 3 之前看到）：**

```markdown
## ⚠ 页数要求偏差（JD 覆盖默认值）

| 材料 | 默认页数 | JD 要求 | 备注 |
|------|---------|---------|------|
| Research Statement | 4 页 | **3 页** | JD 原文："research statement of no more than 3 pages" |
| Teaching Statement | 2 页 | **1 页** | JD 原文："one-page teaching statement" |

> Step 3 将按 JD 要求的页数生成，不使用默认值。如对此有异议，请在开始 Step 3 前告知。
```

如无偏差，step2_summary.md 中不出现此区块。

---

## 规则冲突处理对话

```
⚠ 发现规则冲突，暂停流水线。

【地区卡规则】{具体规则内容}（来源：{source URL}）
【JD 实际要求】{JD 中的具体要求}（来源：{job URL}）

请选择处理方式：
A. 以该校 JD 为准（本次），记录到学校卡
B. 以该校 JD 为准，同时标记地区卡 needs_review
C. 忽略冲突，仍按地区卡执行

请回复 A、B 或 C。
```
