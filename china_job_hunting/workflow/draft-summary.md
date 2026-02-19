# Draft-Summary - 生成学校申请总结

## 目标
为每个目标学校生成申请策略总结文档，分析岗位与候选人背景的匹配度。

## 前置条件
- `china_job_list.xlsx` 或 `scan/target_school_list.xlsx` 包含学校信息
- 候选人材料在 `materials/` 目录中（CV、Research Statement）

## 执行步骤

### 1. 读取学校信息
```python
import pandas as pd

# 读取主文件
df = pd.read_excel('china_job_list.xlsx')

# 筛选计划申请的学校
df_apply = df[df['是否计划申请'] == '是']  # 或其他标记
```

### 2. 为每个学校创建目录
```bash
mkdir -p drafts/{University}
```

命名规范:
- 使用学校简称，如 `drafts/清华大学/`、`drafts/北京大学/`
- 如有多个部门，使用 `drafts/清华大学-计算机系/`

### 3. 生成 summary.md

每个学校的 `drafts/{University}/summary.md` 包含:

#### 3.1 岗位概要
```markdown
# {University} 申请策略总结

## 岗位信息
- **学校/部门**: {University&Department}
- **岗位名称**: {Position Title}
- **研究方向**: {Position Research Direction}
- **截止日期**: {Deadline}
- **岗位链接**: {Positions Link}

## 实验室/研究组简介
{从 Lab/Research Center/Professor Link 抓取的信息}
- 实验室名称
- 主要研究方向
- 知名教授/PI
- 近期代表性工作

## 岗位详情
{Job Description 的关键信息}
- 职责描述
- 博导资格: {是/否/待定}
- 博士生名额: {具体数字或说明}
- 薪酬待遇
- 科研启动经费
- 住房/安家补贴
```

#### 3.2 海外政策分析
```markdown
## 海外人才政策
- **政策名称**: {OverseaPolicy}
- **政策内容**:
  - 申请条件
  - 待遇说明
  - 申报时间
- **适用性评估**: [高/中/低]
```

#### 3.3 候选人匹配分析
```markdown
## 候选人匹配分析

### 优势
1. **研究方向契合**:
   - 候选人: AI+HCI (Human-Centered AI)
   - 岗位: {Position Research Direction}
   - 匹配度: [高/中/低]

2. **海外背景**:
   - 符合海外优青/海外引进条件
   - {具体政策匹配分析}

3. **研究成果**:
   - CHI/UIST等顶会论文
   - 与该校研究方向的关联

### 不足/风险
1. {列出可能的不匹配点}
2. {需要额外准备的材料}
3. {竞争情况分析}

### 申请策略建议
1. **强调重点**: {针对该校应突出的研究方向}
2. **建立联系**: {是否有可联系的教授/校友}
3. **材料调整**: {Cover Letter需个性化的部分}
4. **时间规划**: {截止日期前的行动计划}
```

#### 3.4 联系方式
```markdown
## 联系方式
- **联系方式**: {联系方式}
- **来源链接**: {联系方式的链接}
- **建议联系方式**:
  - 首选: 微信（如有）
  - 次选: 邮件
```

### 4. 保存文件
确保每个学校的 summary 保存到正确位置:
```
drafts/
├── 清华大学-计算机系/
│   └── summary.md
├── 北京大学-智能学院/
│   └── summary.md
└── ...
```

## 输入
- `china_job_list.xlsx` / `scan/target_school_list.xlsx`
- 候选人背景信息（从 `materials/CV.pdf` 提取）
- 网络资源（用于补充实验室信息）

## 输出
- `drafts/{University}/summary.md` (每校一个)

## 质量检查
- [ ] 每个计划申请的学校都有 summary.md
- [ ] 岗位信息完整（截止日期、链接、研究方向）
- [ ] 包含博导资格和招生名额信息
- [ ] 候选人匹配分析有针对性
- [ ] 申请策略具体可行

## 注意事项
- 优先处理截止日期临近的学校
- 匹配分析要基于实际信息，避免空泛
- 如信息不足，标注需要进一步调研的点
- 策略建议要具体，包括可执行的行动项
- 保持客观，既要分析优势也要指出不足
