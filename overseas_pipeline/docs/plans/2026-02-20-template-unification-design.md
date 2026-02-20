# Template Unification Design — 2026-02-20

## 目标

1. 统一所有 Statement 类文档（Research/Teaching/Diversity Statement、Selection Criteria Response）的视觉风格到 CV_latest 的 Caramel 色系
2. 对 Step 3 材料强制页数默认值，JD 另有要求时传导给用户并自动覆盖
3. 建立独立可编译的基础模板目录，与内容源（overleaf-projects）分工明确

---

## 设计决策

| 决策项 | 选择 | 原因 |
|--------|------|------|
| 字体 | lmodern（与 CV 一致） | 整套材料视觉统一 |
| 色彩 | Caramel（#B87350，来自 CV_latest） | CV 已有成熟方案，直接复用 |
| Section heading 样式 | 直接移植 CV_latest 的 `\sectiontitle` | 视觉一致性最强 |
| Header/footer | Statement 保留页眉（左：姓名，右：文档标题），颜色统一为 Caramel | 学术文档惯例，便于阅读 |
| Cover Letter | 统一到 Caramel（改 OUCletter.cls 颜色+字体，结构不变） | 整套申请材料颜色一致 |
| 模板组织 | 独立可编译项目 + 共享 `.sty` 文件 | 方便验证、方便 Step 3 复制使用 |

---

## 色彩系统（来自 CV_latest）

```latex
\definecolor{headingcolor}{HTML}{B87350}   % 标题/强调色（暖棕）
\definecolor{linkcolor}{HTML}{B87350}       % 链接色
\definecolor{tagbg}{HTML}{F0DDD2}           % 标签背景（浅粉棕）
\definecolor{tagframe}{HTML}{D4B8A6}        % 标签边框
\definecolor{textgray}{RGB}{80, 60, 50}    % 正文颜色（可选）
```

---

## 文件结构

```
overseas_pipeline/
├── templates/                           ← 新增：格式模板目录
│   ├── sophia-statement.sty             ← 共享样式包
│   ├── research_statement/
│   │   └── main.tex                     ← 独立可编译（4 页基础模板）
│   ├── teaching_statement/
│   │   └── main.tex                     ← 独立可编译（2 页基础模板）
│   ├── diversity_statement/
│   │   └── main.tex                     ← 独立可编译（1 页基础模板）
│   ├── selection_criteria_response/
│   │   └── main.tex                     ← 独立可编译（STAR 格式）
│   └── cover_letter/
│       ├── OUCletter.cls                ← Caramel 修改版
│       └── main_template.tex
│
└── overleaf-projects/Faculty Position/  ← 保留：内容来源（Sophia 实际文本）
    ├── Research Statement/              ← Step 3 读取真实内容
    ├── Teaching Statement/
    ├── DEI-structured-1p/2p/
    └── CV_latest/                       ← CV 样式参考来源
```

**分工原则：**
- `templates/`：只管格式，占位内容，Step 3 以此为起点复制到 `output/{school}/{dept}/materials/`
- `overleaf-projects/`：只管内容，是 Sophia 真实的申请材料文本，Step 3 从这里提取内容填入模板

---

## 页数默认值

| 文档 | 默认页数 | 说明 |
|------|---------|------|
| Cover Letter | 2 页 | |
| Research Statement | 4 页 | TT 完整版；NTT 压缩为 2-3 页 |
| Teaching Statement | 2 页 | |
| Diversity Statement | 1 页（可扩展至 2 页） | 默认 1p；JD 要求或内容需要时扩展至 2p |
| Selection Criteria Response | 无固定（通常 6-10 页） | 按 criteria 数量决定 |

**JD 覆盖流程：**
1. Step 2 分析 JD 时扫描页数限制关键词（"not exceeding X pages", "X-page", "maximum X pages" 等）
2. 如有，在 `fit_report.md` 的各材料调整建议中标注 `⚠ JD 明确要求：X 页（覆盖默认 Y 页）`
3. 在 `step2_summary.md` 顶部醒目列出所有页数偏差
4. Step 3 从 fit_report 读取页数要求，优先使用 JD 值

**页数验证（Step 3 编译后）：**
- 检查生成的 PDF 页数
- 超出：删减次要内容（Diversity Statement 的 Future Plans、Research Statement 的背景铺垫等）
- 明显不足（如目标 4 页但只有 2 页）：在 step3_summary.md 标注警告，提示 Sophia 补充

---

## Step 3 工作流变化

**旧流程：**从 `overleaf-projects/` 复制 → 替换内容 → 编译

**新流程：**
1. 从 `templates/{doc_type}/` 复制完整项目到 `output/{school}/{dept}/materials/{doc_type}/`
2. 从 `overleaf-projects/` 读取 Sophia 的真实内容段落
3. 将真实内容替换模板占位符，按 fit_report 定制
4. 编译 PDF
5. 验证页数是否在目标范围

---

## sophia-statement.sty 接口

```latex
% 使用方式
\usepackage[doctitle={Research Statement}, totalpages={4}]{sophia-statement}

% 提供的命令
\highlight{text}      % 暖棕色粗体
\me{name}             % 暖棕色粗体（标注 Sophia 名字）

% section 格式：自动继承 CV_latest sectiontitle 样式
% header/footer：自动设置，doctitle 参数传入右页眉标题
% totalpages 参数：传入页脚右侧显示的总页数（动态计算用 \pageref{LastPage}）
```
