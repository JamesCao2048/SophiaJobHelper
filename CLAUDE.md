# SophiaJobHelper Project Guidelines

## 📊 Google Sheets Synchronization

本项目配置了 Google Sheets 双向同步工具，位于 `google-sheets-sync/` 目录。

### 常用命令

- **从云端同步最新数据（推荐）**  
  从 Google Sheets 导出数据，保留格式（颜色、筛选器等），并自动清洗以兼容 Mac Excel。
  ```bash
  cd google-sheets-sync && python3 export_excel.py
  ```
  > 输出文件位置：`google-sheets-sync/agent_sophia_job_list.xlsx`

- **代码级数据操作（高级）**  
  如果需要通过 Python 代码双向读写数据（不保留格式，仅处理纯数据）：
  ```bash
  cd google-sheets-sync && python3 sheets_sync.py
  ```

### 配置说明

1. **Service Account**: 密钥文件位于 `google-sheets-sync/credentials/service_account.json`。
2. **权限**: 必须将 Service Account 邮箱添加为 Google Sheet 的 **Editor**。
3. **环境**: 依赖库见 `google-sheets-sync/requirements.txt`。

## 📂 目录结构

- `google-sheets-sync/`: 同步工具源码和配置
- `job_hunting/`: 教职申请相关任务和文档
- `job_filling/`: 可能是针对填表任务的目录（待确认）
- `general/`: 通用规则和计划文档
