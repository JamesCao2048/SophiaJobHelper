# CV 定制策略

## 五种变体

| 变体 | 触发条件 | 核心调整 |
|------|----------|----------|
| `base` | USA/UK/Canada/Australia TT 岗 | 不变，直接复制 |
| `ntt` | NTT / Teaching-track / 教学导向岗 | Teaching + Mentoring 节提前 |
| `metrics-first` | 意大利/西班牙/中国大陆/中东（沙特/UAE） | 首页加 Bibliometrics 摘要表 |
| `cv-analytique` | 法国 | 格式完全不同，需 Sophia 手动完成 |
| `dach` | 德国/瑞士/奥地利 | 加个人信息区域 + Habilitation 叙事 |

---

## `ntt` 变体：Section 排序调整

**标准 TT 顺序（base）：**
1. Research Interests
2. Work & Research Experience
3. Education
4. Manuscripts / Ongoing Work
5. Key Publications
6. Short Papers
7. Honors & Awards
8. Invited Talks & Presentations
9. Academic Service
10. Mentoring Experience
11. Teaching Experience
12. References

**NTT/教学导向顺序（ntt）：**
1. Research Interests（简化，加教学视角句）
2. Education
3. Teaching Experience ← **从末位提前**
4. Mentoring Experience ← **从末位提前**
5. Work & Research Experience
6. Key Publications
7. Short Papers / Manuscripts
8. Honors & Awards
9. Invited Talks & Presentations
10. Academic Service
11. References

**执行方法（LaTeX）：** CV_latest 使用模块化结构（`content/` 下各节单独 .tex），修改 `main.tex` 中的 `\input` 顺序即可，无需改内容。

**Research Interests 段额外调整（ntt）：** 在研究方向描述末尾加一句点明教学转化，例如：
> "These research lines directly inform courses in Human--AI Interaction, Computational Qualitative Analysis, and Human Aspects of Software Engineering."

---

## `metrics-first` 变体：Bibliometrics 首页

在 CV 第一页 Education 之前插入一个 Bibliometrics 摘要框：

```latex
\begin{center}
\begin{tabular}{lll}
\toprule
\textbf{Metric} & \textbf{Value} & \textbf{Source} \\
\midrule
h-index & X & Google Scholar \\
Total Citations & X+ & Google Scholar \\
Key Publications & X (CHI/CSCW/TOCHI/UIST) & \\
CCF-A Papers & X & (CHI/CSCW/UIST/EMNLP) \\
\bottomrule
\end{tabular}
\end{center}
```

**地区特殊要求：**

| 地区 | 额外要求 |
|------|---------|
| 意大利 | 加 Scopus Author ID；验证每篇论文是否 Scopus 收录 |
| 西班牙 | 加 ANECA accreditation 状态（如已获得）|
| 中国大陆 | 加 CCF 分类标注；加 "连续海外工作 36 个月" 时间轴 |
| 沙特/UAE | h-index 是"脸面"，放到最醒目位置 |

---

## `cv-analytique` 变体（法国）

法国 CV 格式与英美体系完全不同，当前 CV_latest 无法直接适配。**管道行为：**

1. 识别到目标地区为法国时，在 step3_summary.md 中标注：
   ```
   ⚠ 法国申请需 CV Analytique 格式，自动生成不可靠。
   建议 Sophia 手动准备，或使用 DEI-prose-2p/ 作为参考结构。
   ```
2. 提供一份人工 checklist（教学学时/行政职责/集体责任）
3. 其余材料照常生成

---

## `dach` 变体（德国/瑞士/奥地利）

- 在 CV 首部加个人信息区（Name / Date of Birth / Nationality / Address）
- 照片槽位（可选，在 \photo{} 命令处留空）
- 研究描述使用 Habilitation-style 累积叙事（不同于 TT 的"未来蓝图"）
- W1 职位（无终身轨）和 W2/W3 职位对应不同的措辞重心

当前 CV_latest 无 Habilitation 叙事，**管道行为**：生成提示，让 Sophia 决定是否手动补充。

---

## 各地区 CHI/HCI 论文的标注策略

| 地区 | 标注方式 |
|------|---------|
| USA/UK/Canada/AU | 加括注："CHI (Acceptance Rate: ~23%)" |
| 香港/新加坡 | 同上，Best Paper / HM 加粗 |
| 日本 | 补充 SCI/Scopus 期刊版本（如有） |
| 中国大陆 | 标注 "CCF-A" 分类 |
| 意大利/西班牙 | 验证 Scopus 收录状态，标注 Scopus ID |
| 中东 | 不着重 HCI 标签，强调 AI/System 技术属性 |

---

## 输出路径

CV 定制结果输出到：`output/{school_id}/{dept_id}/materials/CV/`

目录结构（从 CV_latest/ 复制后修改）：
```
materials/CV/
├── main.tex              ← 修改 \input 顺序（ntt 变体）或添加 Bibliometrics（metrics-first）
├── content/              ← 各节 .tex（通常不修改内容）
│   ├── 0_name.tex
│   ├── 1_interests.tex
│   ├── 2_employment.tex
│   ├── 3_education.tex
│   ├── 4_ongoing.tex
│   ├── 5_pubs.tex
│   ├── 6_talks.tex
│   ├── 7_service.tex
│   ├── 8_mentorship.tex
│   └── 9_teaching.tex
└── main.pdf              ← 编译后的 PDF
```

编译命令：`xelatex main.tex && xelatex main.tex`
