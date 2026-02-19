# Setup - 环境安装与数据检查

## 目标
检查并安装必要的依赖库，验证并修正 Excel 数据格式，确保数据一致性。

## 前置条件
- Python 3.8+ 已安装
- 有网络连接（用于安装依赖）
- `china_job_list.xlsx` 文件存在

## 执行步骤

### 1. 安装依赖库
```bash
pip install pandas openpyxl requests beautifulsoup4 tavily-python
```

依赖说明:
- `pandas`: Excel 数据处理
- `openpyxl`: xlsx 格式读写
- `requests`: 网络请求
- `beautifulsoup4`: HTML 解析
- `tavily-python`: 网络搜索 API

### 2. 检查 Excel 列名规范
读取 Excel 文件，确保列名与 CLAUDE.md 定义一致:

| 列名 | 说明 |
|------|------|
| `Deadline` | 截止日期，格式: YYYY-MM-DD |
| `University&Department` | 学校与部门，如 `清华大学-人机交互中心` |
| `Positions Link` | 岗位详情页面 URL |
| `Position Title` | 岗位标题 |
| `Position Research Direction (AI/HCI/HAI)` | 研究方向 |
| `Lab/Research Center/Professor Link` | 实验室/教授链接 |
| `OverseaPolicy` | 海外人才政策 |
| `Job Description` | 岗位描述 |
| `联系方式` | 联系方式（邮箱/微信/电话） |
| `联系方式的链接` | 联系方式来源链接 |
| `是否计划申请` | 申请意向（人工填写，AI不能修改） |

### 3. 数据格式验证

#### 3.1 URL 验证
检查 `Positions Link`、`Lab/Research Center/Professor Link`、`联系方式的链接` 列:
- 值必须是有效的 URL（以 http:// 或 https:// 开头）
- 不能是岗位名称或其他文本
- 空值可以接受
- 通过网络爬取验证必须是可访问的

#### 3.2 日期格式验证
检查 `Deadline` 列:
- 格式应为 `YYYY-MM-DD` 或 `Rolling`
- 如遇中文日期 "2026年3月1日"，转换为 "2026-03-01"

### 4. 重复行检测
以 `University&Department` + `Position Title` 作为唯一键:
- 检测重复行
- 输出重复行列表供人工审核
- 标注重复关系（如同一学校不同岗位 vs 完全重复）

### 5. 备份原文件
```bash
cp china_job_list.xlsx backups/backup_$(date +%Y%m%d_%H%M%S).xlsx
```

## 输入
- `china_job_list.xlsx` (或 `china_job_list_{date}.xlsx`)

## 输出
- 修正后的 `china_job_list.xlsx`
- 备份文件 `backups/backup_{timestamp}.xlsx`
- 控制台输出: 检测到的问题清单

## 质量检查
- [ ] 所有依赖库安装成功
- [ ] Excel 列名符合规范
- [ ] URL 列中无非法值
- [ ] 日期格式统一
- [ ] 重复行已标注
- [ ] 原文件已备份

## 注意事项
- `是否计划申请` 列由人工维护，setup 任务不应修改此列
- 如发现列名不一致（如 "University" vs "University&Department"），需修正为标准列名
- 数据修正前务必先备份
