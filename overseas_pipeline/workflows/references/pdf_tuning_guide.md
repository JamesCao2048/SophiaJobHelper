# PDF 排版微调策略

> **参考文件** — 由 workflow 步骤引用，不可独立执行。
> **引用方**：`workflows/step3_materials.md` step 8

---

## 页数验证

用 `pdfinfo` 获取实际页数：
```bash
pdfinfo output.pdf | grep Pages
# 或
python3 -c "import subprocess; r=subprocess.run(['pdfinfo','main.pdf'],capture_output=True,text=True); print([l for l in r.stdout.splitlines() if 'Pages' in l])"
```

## 页数目标与处理规则

| 材料 | 目标 | 超出处理 | 明显不足处理 |
|------|------|---------|------------|
| Cover Letter | 2 页 | 精简段落，优先删 Service 段细节 | < 1.5 页：提示补充 Fit 段 |
| Research Statement | 5 页（TT）| 精简 Background 铺垫，删次要 subsection | < 4 页：提示补充 Future Plans |
| Teaching Statement | 2 页 | 精简 Mentorship 或 Course list | < 1.5 页：提示补充 |
| Diversity Statement | 1 页（默认）| 精简 Service 段；若 2 页目标则精简 Plans | < 0.8 页：提示补充 |
| Selection Criteria | 无固定 | 不触发，按 criteria 数量自然延伸 | — |

**超出处理分两层：先做 PDF-aware 微调（不改内容），再做内容精简。**

**明显不足判断标准**：实际页数 < 目标页数 × 0.75（如目标 4 页但只有 3 页以下）

---

## 第一层：PDF-aware 排版微调（不改写内容）

编译后先检查**最后一页的实际行数**（用 `pdftotext` 或肉眼判断）。如果最后一页只有少量行（≤ 页面高度的 1/4），说明只需挤掉几行就能消除整页溢出——此时优先用排版手段，不删内容：

**微调手段（按推荐顺序）：**

| # | 手段 | 命令/操作 | 效果 | 适用场景 |
|---|------|----------|------|---------|
| T1 | **段落挤行** | 在溢出附近的长段落末尾加 `\looseness=-1` | 让该段少排 1 行 | 最常用，几乎无视觉差异 |
| T2 | **缩小段间距** | `\setlength{\parskip}{0.25em}`（局部或全局） | 每段间省 ~1pt | 段落多时效果累积显著 |
| T3 | **压缩列表间距** | `\setlist{itemsep=0.1em, parsep=0pt}` | 列表项更紧凑 | 有 itemize/enumerate 时 |
| T4 | **收紧 section 间距** | `\titlespacing*{\section}{0pt}{0.6em}{0.2em}` | 每个 section 省 ~2pt | section 多时 |
| T5 | **压缩图片周围空白** | wrapfigure 内 `\vspace{-1.5em}` 或减小图片宽度 | 图片周围回收空间 | RS 含图时 |
| T6 | **微调页边距** | geometry 选项 top/bottom 各减 0.05in | 每页多 ~2 行 | 差 2-3 行时 |

**操作流程：**
1. 编译 → `pdfinfo` 检查页数
2. 如超出目标且最后一页 ≤ 1/4 满 → 尝试 T1-T6（通常 T1+T2 即可）
3. 重新编译 → 再检查
4. 如果微调后仍超出 → 进入第二层（内容精简）

---

## 第二层：内容精简（改写/删除文本）

PDF-aware 微调无法解决时（超出 > 半页），按以下优先级精简内容：

1. 删除或缩短"背景铺垫"段（读者已知的领域常识）
2. 合并相似 subsection
3. 缩短 Future Plans（保留 2-3 句而非完整段落）
4. 压缩 Service/Outreach 段到 1-2 句
5. 如仍超出：在 step3_summary.md 标注 `⚠ 页数超出，Sophia 需进一步精简`
