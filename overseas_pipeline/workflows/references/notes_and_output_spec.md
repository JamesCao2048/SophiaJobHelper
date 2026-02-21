# notes.md 格式 + 产出物清单 + 一致性检查

> **参考文件** — 由 workflow 步骤引用，不可独立执行。
> **引用方**：`workflows/step3_materials.md` step 6/9

---

## notes.md 格式（强制，不可简化）

notes.md 是给 Sophia 审核的"修改日志"，必须让她无需打开 .tex 文件就能理解所有修改。

```markdown
# {材料名} 修改说明 -- {学校}

## 生成日期

## 总体策略
<!-- 2-3 句话说明整体定制方向和关键定位决策 -->

## 参考资料清单
| # | 类型 | 资料 | 链接/路径 |
|---|------|------|-----------|
| R1 | 区域规则卡 | {地区}规则卡 Section X（行号）| region_knowledge/regions/{region}.md L58-138 |
| R2 | Fit Report | 匹配分析 | output/{school}/{dept}/fit_report.md |
| R3 | Sophia 材料 | Research Statement | overseas_pipeline/materials/Research_Statement.md |
<!-- 必须标注具体章节/行号 -->

## 逐段修改说明

### 1. {段落标识} [NEW / MODIFIED / UNCHANGED]
**原文：** > 引用原始文本（新增标注"无对应原文"）
**修改为：** > 引用修改后的关键句子
**原因：**
- 引用 [R1: 具体章节/行号] ...

### N. 未修改部分
<!-- 必须列出所有未修改的主要段落，说明保留原因 -->

## 样式说明与 Debug 记录
<!-- 编译器选择、字体、编译问题修复 -->

## 给 Sophia 的审核重点
<!-- 3-5 条具体可操作的审核项，非泛泛"请审核" -->
```

## notes.md 质量自检（Step 3 完成前）

- [ ] 每个修改段落都有原文 vs 修改的对比
- [ ] 每个修改原因都引用了具体参考资料编号和章节
- [ ] 未修改的部分也有说明（为什么保留）
- [ ] 有编译/样式说明
- [ ] "给 Sophia 的审核重点"包含具体可操作的审核项

---

## 同校多系一致性检查

如 `related_applications` 字段存在，在每份 notes.md 末尾追加：

```markdown
## 同校多系一致性检查
- 本校另一份申请：{department}（{strategy} 策略）
- 核心叙事一致性：✅/⚠ {说明}
- 侧重点差异：本系版（{简述}）vs 另一系版（{简述}）
- ⚠ 注意：{具体提醒}
```

---

## 产出物清单（step3_summary.md 记录）

```
materials/
├── Cover Letter/
│   ├── main.tex / main.pdf          ✅/❌
│   └── cover_letter.notes.md
├── Research Statement/              ✅/❌（或 Research Interests/）
│   ├── main.tex / main.pdf
│   └── research_statement.notes.md
├── Teaching Statement/              ✅/❌
│   ├── Teaching_Statement.tex / .pdf
│   └── teaching_statement.notes.md
├── Diversity Statement/             ✅/❌/不提交（JD 未要求）
│   ├── main.tex / main.pdf
│   └── diversity_statement.notes.md
├── CV/                              ✅/❌/直接复制（base 变体）
│   ├── main.tex / main.pdf
│   └── cv.notes.md
└── Selection Criteria Response/     ✅/❌/不适用（非澳洲）
    ├── selection_criteria_response.tex / .pdf
    └── selection_criteria_response.notes.md
```
