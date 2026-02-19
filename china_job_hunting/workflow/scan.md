# Scan - 搜索新学校岗位

## 目标
搜索中国高校（985/211/HCI-AI强校）的 HCI/AI 相关教职岗位，扩充目标学校列表。

## 前置条件
- 网络连接正常
- 搜索工具可用（WebSearch/Tavily）
- `./scan/` 目录已创建

## 执行步骤

### 1. 创建工作目录
```bash
mkdir -p scan
```

### 2. 建立目标学校列表

#### 2.1 985 工程高校（全覆盖）
优先搜索以下学校的 CS/AI/HCI 相关学院:
- 清华大学、北京大学、浙江大学、上海交通大学
- 复旦大学、南京大学、中国科学技术大学
- 哈尔滨工业大学、西安交通大学、华中科技大学
- 中山大学、同济大学、东南大学
- 北京航空航天大学、北京理工大学
- 天津大学、武汉大学、四川大学
- ... (全部39所)

#### 2.2 HCI/AI 强校（211及其他）
- 北京邮电大学（网络与交互）
- 华东师范大学（智能交互）
- 苏州大学（HCI研究组）
- 电子科技大学（AI与交互）
- 西北工业大学（人机工程）
- ...

#### 2.3 新兴研究机构
- 中科院研究所（自动化所、计算所、软件所）
- 深圳/杭州/苏州等地研究院
- 新型研究型大学（南方科技大学、西湖大学、上海科技大学）

### 3. 搜索岗位信息

对每个目标学校，执行以下搜索:

#### 3.1 搜索关键词组合
```
"{学校名} 计算机学院 招聘 2025 2026"
"{学校名} 人工智能学院 教职 诚聘"
"{学校名} HCI 人机交互 招聘"
"{学校名} 海外优青 人才引进"
"{学校名} faculty recruitment AI HCI"
```

#### 3.2 信息提取
从搜索结果中提取:
- 岗位链接（Positions Link）
- 截止日期（Deadline）
- 岗位名称（Position Title）
- 研究方向（AI/HCI/HAI）
- 海外政策（OverseaPolicy）

#### 3.3 重点关注
- **HCI**: "人机交互"、"交互设计"、"用户研究"、"智能交互"
- **海外人才**: "海外优青"、"海外引进"、"青年学者"
- **教职招聘**: "诚聘教职"、"长聘教授"、"Tenure-track"

### 4. 保存搜索结果

#### 4.1 目标学校列表
保存到 `scan/target_school_list.md`:
```markdown
# 目标学校列表

## 985高校
- 清华大学 - 计算机系、交叉信息院
- 北京大学 - 智能学院、前沿计算研究中心
...

## HCI/AI强校
- 北京邮电大学 - 网络技术研究院
...

## 研究机构
- 中科院自动化所
...
```

#### 4.2 岗位信息表
保存到 `scan/target_school_list.xlsx`:
- 格式与 `china_job_list.xlsx` 保持一致
- 包含所有新发现的岗位

### 5. 合并更新主文件
创建新版本 `china_job_list_{date}.xlsx`:
```python
import pandas as pd
from datetime import date

# 读取现有数据
df_existing = pd.read_excel('china_job_list.xlsx')

# 读取新扫描数据
df_new = pd.read_excel('scan/target_school_list.xlsx')

# 去重合并
df_merged = pd.concat([df_existing, df_new]).drop_duplicates(
    subset=['University&Department', 'Positions Link'],
    keep='first'
)

# 保存新版本
df_merged.to_excel(f'china_job_list_{date.today()}.xlsx', index=False)
```

## 输入
- 网络搜索资源
- 现有 `china_job_list.xlsx`（可选，用于去重）

## 输出
- `scan/target_school_list.md`: 目标学校文档
- `scan/target_school_list.xlsx`: 新发现岗位表
- `china_job_list_{date}.xlsx`: 合并后的新版主文件

## 质量检查
- [ ] 覆盖主要985高校的CS/AI/HCI学院
- [ ] 搜索关键词包含 HCI、海外优青、诚聘教职
- [ ] 新发现岗位信息完整（至少有学校、链接、方向）
- [ ] 与现有数据去重，无重复条目
- [ ] 新版文件以日期命名

## 注意事项
- 优先关注有 HCI 或 AI+HCI 交叉方向的岗位
- 记录博导资格要求和博士生招生名额
- 海外人才政策是重要加分项
- 注意区分长期招聘（Rolling）和有明确截止日期的岗位
- 搜索时注意请求频率，避免触发反爬机制
- "Write a python script to fetch content from [URL] using the Tavily API (search/extract) to bypass anti-scraping protections."
