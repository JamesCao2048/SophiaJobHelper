# 申请材料样式指南

> 本文档说明：样式模板在哪里、如何预览、如何修改样式。  
> **不需要懂 LaTeX**——所有操作都可以通过 Claude Code 指令完成。

---

## 目录

1. [样式系统概览](#样式系统概览)
2. [⚠ 已知问题：lmodern 字体导致页数偏多](#已知问题lmodern-字体导致页数偏多)
3. [模板在哪里](#模板在哪里)
4. [一键编译预览（Claude Code 指令）](#一键编译预览)
5. [如何修改样式](#如何修改样式)
6. [格式 vs 内容：两个目录的分工](#格式-vs-内容)

---

## 样式系统概览

所有申请材料（Cover Letter、Research Statement、Teaching Statement、Diversity Statement、Selection Criteria Response）使用统一的视觉风格：

| 设计要素 | 当前设定 | 说明 |
|---------|---------|------|
| **主色调** | Caramel 暖棕 `#B87350` | 与 CV 一致 |
| **字体** | lmodern（Computer Modern 系列） | 学术气质，与 CV 一致 |
| **Section 标题** | 暖棕色粗体 + 60% 透明度下划线 | 直接沿用 CV 样式 |
| **页眉** | 左：姓名，右：文档标题（暖棕色） | |
| **页脚** | 居中页码 `1/N`（暖棕色 70%） | |
| **Cover Letter** | Caramel 版 OUCletter.cls | 信件格式，颜色统一 |

---

## ⚠ 已知问题：lmodern 字体导致页数偏多

> **在使用模板生成正式申请材料前，请先确认页数是否符合要求。**

### 当前实测页数 vs 目标页数

| 文档 | 目标页数 | 当前模板页数 | 偏差 |
|------|---------|------------|------|
| Research Statement | **4 页** | 6 页 | +2 ⚠ |
| Teaching Statement | **2 页** | 3 页 | +1 ⚠ |
| Diversity Statement | **1–2 页** | 1 页 | ✓ |

### 原因

新样式使用 **lmodern（Computer Modern）** 字体以与 CV 风格统一，但该字体比原始模板所用的 **mathptmx（Times）** 更宽，导致相同内容需要更多页面。

### 压缩空间的修改建议

以下修改均可通过告诉 Claude Code 来完成，**按效果从大到小排列**：

#### 方案 1：缩小正文字号（推荐，影响最大）
```
把所有 Statement 的正文字号从 11pt 改成 10.5pt，重新编译看效果
```
> 预计效果：Research Statement −1 页，Teaching Statement −0.5 页。字体风格不变。

#### 方案 2：换用 Times 系列字体（效果最大，但与 CV 风格不一致）
```
把 sophia-statement.sty 的字体从 lmodern 换成 mathptmx（Times），重新编译
```
> 预计效果：Research Statement −2 页（接近原始 4 页），Teaching Statement −1 页。CV 与 Statement 字体不再统一。

#### 方案 3：收紧段间距
```
把 sophia-statement.sty 的 parskip 从 0.35em 改成 0.2em，重新编译
```
> 预计效果：各文档减少约 0.3–0.5 页。阅读体验略显紧凑。

#### 方案 4：收紧页边距
```
把 Statement 的上下边距从 0.65in 改成 0.55in，左右从 0.75in 改成 0.65in，重新编译
```
> 预计效果：各文档减少约 0.3–0.5 页。内容更靠近页面边缘，视觉上稍密。

#### 方案 5（临时）：Step 3 生成时裁剪
不修改样式，Step 3 编译后自动检测页数，按优先级裁剪内容到目标页数。适合不想改全局样式、只对某所学校临时处理的情况。

---

## 模板在哪里

```
overseas_pipeline/templates/
│
├── sophia-statement.sty             ← ★ 核心样式文件（统一所有 Statement 的格式）
│
├── research_statement/
│   ├── sophia-statement.sty         ← 本地副本（独立编译用）
│   ├── main.tex                     ← Research Statement 模板（目标 4 页，TT 版）
│   └── main.pdf                     ← 编译好的预览 PDF
│
├── teaching_statement/
│   ├── sophia-statement.sty
│   ├── main.tex                     ← Teaching Statement 模板（目标 2 页）
│   └── main.pdf
│
├── diversity_statement/
│   ├── sophia-statement.sty
│   ├── main.tex                     ← Diversity Statement 模板（默认 1 页）
│   └── main.pdf
│
├── selection_criteria_response/
│   ├── sophia-statement.sty
│   ├── main.tex                     ← Selection Criteria 模板（澳洲用，STAR 格式）
│   └── main.pdf
│
└── cover_letter/
    ├── OUCletter.cls                ← Cover Letter 专用样式（Caramel 配色版）
    ├── main_template.tex            ← Cover Letter 模板（目标 2 页）
    └── main_template.pdf            ← 编译好的预览 PDF
```

**关键文件说明：**

- **`sophia-statement.sty`**（根目录）：所有 Statement 类文档的样式核心。改这一个文件，Research/Teaching/Diversity/Selection Criteria 全部同步变更。
- **各子目录的 `sophia-statement.sty`**：和根目录完全相同的副本，让每个模板目录可以独立编译，不依赖外部路径。修改样式时，需要同步更新根目录的版本（AI 会帮你做）。
- **`OUCletter.cls`**：只影响 Cover Letter，单独修改。

---

## 一键编译预览

在 Claude Code 中说以下任意一句话，AI 会自动编译并打开预览：

### 预览所有模板

```
帮我编译所有样式模板，编译完打开 PDF 让我看看
```

```
把 templates/ 下面所有模板都重新编译一遍
```

### 预览单个模板

```
编译一下 Research Statement 模板，让我看看样式
```

```
把 teaching_statement 的模板 PDF 给我打开
```

```
重新生成 Cover Letter 模板的 PDF
```

### 修改样式后重新编译

```
我修改了 sophia-statement.sty，帮我重新同步到各子目录并重新编译所有模板
```

```
更新了主色调，帮我重新编译所有 Statement 模板预览
```

---

### 自己手动编译（可选）

如果你需要在 Claude Code 之外自己编译，从终端运行（需要已安装 MacTeX）：

**Statement 类文档**（Research / Teaching / Diversity / Selection Criteria）：
```bash
# 以 research_statement 为例
pdflatex -output-directory templates/research_statement templates/research_statement/main.tex
open templates/research_statement/main.pdf
```

**Cover Letter**（需要 xelatex）：
```bash
xelatex -output-directory templates/cover_letter templates/cover_letter/main_template.tex
open templates/cover_letter/main_template.pdf
```

> **安装 LaTeX**（如尚未安装）：`brew install --cask mactex-no-gui`（约 4 GB，含全套编译工具）

---

## 如何修改样式

### 场景 A：修改所有 Statement 文档的样式

**改颜色（比如主色调从暖棕换成深蓝）：**
```
把所有 Statement 的主色调改成深蓝 #1A3A6B，重新编译让我看看效果
```

**改字号：**
```
把所有 Statement 的正文字号从 11pt 改成 10.5pt
```

**改页边距：**
```
把 Statement 的左右边距从 0.75 英寸改成 0.7 英寸，上下从 0.65 英寸改成 0.6 英寸
```

**改 Section 标题样式：**
```
把 Section 标题的下划线去掉，只保留颜色粗体
```

→ AI 会修改 **`templates/sophia-statement.sty`**，同步到各子目录，并重新编译所有模板供你预览。

---

### 场景 B：只修改某一份材料的样式

**只改 Research Statement 的字号：**
```
Research Statement 模板的正文字号改成 10.5pt，其他不变
```

**只改 Cover Letter 的颜色：**
```
Cover Letter 的颜色改成 #2C5F8A，其他 Statement 不变
```

→ AI 会修改对应模板的 `.tex` 或 `.cls` 文件，不影响其他文档。

---

### 场景 C：修改样式后，让所有已生成的材料也更新

Step 3 已经为某所学校生成了材料，现在想用新样式重新生成：

```
我改了样式模板，帮我重新编译 output/university_of_auckland/cs/ 下所有已生成的 PDF
```

→ AI 会找到所有 output 目录下的 `.tex` 文件，确保使用最新样式，重新编译。

---

### 样式文件速查：改什么在哪里

| 想修改的内容 | 文件位置 | 变量名 / 位置 |
|------------|---------|------------|
| 所有文档主色调 | `templates/sophia-statement.sty` | `\definecolor{headingcolor}{HTML}{B87350}` |
| 所有文档链接颜色 | `templates/sophia-statement.sty` | `\definecolor{linkcolor}{HTML}{B87350}` |
| 所有文档字体 | `templates/sophia-statement.sty` | `\RequirePackage{lmodern}` 行（改为其他字体包） |
| 所有文档页边距 | `templates/sophia-statement.sty` | `\RequirePackage[...]{geometry}` 行 |
| Section 标题样式 | `templates/sophia-statement.sty` | `\titleformat{\section}` 块 |
| 页眉/页脚格式 | `templates/sophia-statement.sty` | `\fancyhead` / `\fancyfoot` 行 |
| Cover Letter 颜色 | `templates/cover_letter/OUCletter.cls` | `\definecolor{slcolor}{HTML}{B87350}` |
| Cover Letter 正文格式 | `templates/cover_letter/main_template.tex` | 在 preamble 中 |
| 某个 Statement 独有的格式 | 对应子目录的 `main.tex` | 在 `\begin{document}` 之前 |

---

## 格式 vs 内容

Step 3 生成材料时使用两类完全不同的资源：

| 目录 | 作用 | 说明 |
|------|------|------|
| `templates/` | **格式**：决定材料的视觉风格 | 统一 Caramel 配色、lmodern 字体、heading 样式。Step 3 以此为起点复制到 `output/`。**改样式改这里。** |
| `overleaf-projects/Faculty Position/` | **内容**：Sophia 真实的申请材料文本 | 包含实际的研究描述、教学故事、各校专属 Cover Letter 等。Step 3 从这里提取段落填入模板。**改内容改这里。** |
| `materials/` | **参考**：Markdown 格式的材料概要 | AI 读取用于分析匹配度，不直接生成 LaTeX。 |

> **为什么要分开？**  
> 格式和内容分离，意味着你可以随时统一更新所有材料的视觉风格，而不影响任何已写好的内容。反过来，更新内容（比如添加新发表的论文）也不会破坏排版格式。
