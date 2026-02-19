# Google Sheets 双向同步工具

实现 Google Sheets 与本地代码的双向同步，支持读取、修改、增量更新和智能合并。

## 🚀 快速开始

### 1. 设置 Google Cloud 项目

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建新项目（或选择已有项目）
3. 启用以下 API：
   - **Google Sheets API**
   - **Google Drive API**
4. 创建 Service Account：
   - 进入 "APIs & Services" → "Credentials"
   - 点击 "Create Credentials" → "Service account"
   - 命名并创建
   - 在 Service Account 详情页 → "Keys" → "Add Key" → "Create new key" → JSON
   - 下载 JSON 密钥文件

### 2. 配置本地环境

```bash
# 安装依赖
pip install -r requirements.txt

# 复制配置文件
cp .env.example .env

# 将下载的 JSON 密钥放到指定位置
mkdir -p credentials
mv ~/Downloads/your-service-account-key.json ./credentials/service_account.json
```

### 3. 共享 Google Sheet

⚠️ **这一步非常重要！**

将 Service Account 的邮箱地址添加为你 Google Sheet 的**编辑者**：

1. JSON 密钥文件中找到 `client_email` 字段（类似 `xxx@xxx.iam.gserviceaccount.com`）
2. 打开你的 Google Sheet
3. 点击右上角 "共享" 按钮
4. 输入 Service Account 邮箱
5. 设置权限为 "编辑者"
6. 点击发送

### 4. 运行

```bash
# 首次运行 - 拉取所有数据
python sheets_sync.py

# 运行示例
python examples.py
```

## 📖 使用说明

### 基本用法

```python
from sheets_sync import GoogleSheetsSync

sync = GoogleSheetsSync()

# 列出所有 Sheet
sheets = sync.list_sheets()

# 拉取所有数据到本地
all_data = sync.pull_all(save_local=True)

# 拉取特定 Sheet
df = sync.pull_sheet("Sheet1")

# 修改后推送
df.loc[0, "状态"] = "已完成"
sync.push_sheet("Sheet1", df)
```

### 增量更新（推荐）

增量更新不会影响筛选条件和格式：

```python
# 更新特定单元格
sync.update_cells("Sheet1", [
    {"row": 2, "col": 3, "value": "新值"},
])

# 按列名更新某行
sync.update_row("Sheet1", row_index=0, row_data={
    "状态": "已完成",
    "备注": "代码更新",
})

# 追加新行
sync.append_rows("Sheet1", new_df)
```

### 智能同步（处理双向编辑）

当你和其他人都在编辑同一个 Sheet 时：

```python
# 拉取最新 → 本地修改 → 仅推送差异
df = sync.pull_sheet("Sheet1")
df.loc[df["名称"] == "某项", "状态"] = "完成"

report = sync.smart_sync(
    sheet_name="Sheet1",
    local_df=df,
    key_column="名称",  # 唯一键列
)
```

## 📁 文件结构

```
google-sheets-sync/
├── .env.example          # 环境变量模板
├── .env                  # 你的配置（不提交到 git）
├── requirements.txt      # Python 依赖
├── sheets_sync.py        # 核心同步模块
├── examples.py           # 使用示例
├── credentials/          # Service Account 密钥（不提交到 git）
│   └── service_account.json
└── synced_data/          # 本地同步的数据
    ├── synced_spreadsheet.xlsx  # 完整 Excel
    ├── csv/                     # 每个 Sheet 的 CSV
    │   ├── Sheet1.csv
    │   └── Sheet2.csv
    └── sync_metadata.json       # 同步元数据
```

## ⚠️ 关于筛选条件

- **筛选视图 (Filter Views)**：使用本工具操作数据**不会**破坏筛选视图，因为它们是独立于数据的
- **基本筛选器 (Basic Filter)**：如果使用 `push_sheet` 的 `clear_first=True`（默认），可能会清除基本筛选器。建议使用 `update_cells` 或 `update_row` 进行增量更新
- **建议**：在 Google Sheet 中使用"筛选视图"而非"基本筛选器"，这样代码操作不会影响筛选设置

## 🔒 安全注意事项

以下文件不应提交到 Git：
- `.env` - 包含配置
- `credentials/` - 包含敏感密钥
- `synced_data/` - 包含同步数据

确保 `.gitignore` 中包含这些路径。
