"""
Google Sheets 双向同步工具

功能：
1. 从 Google Sheets 拉取所有 Sheet 数据到本地（DataFrame / Excel）
2. 本地修改后推送回 Google Sheets
3. 支持增量更新特定单元格/行/列
4. 保留云端的筛选条件和格式（API 操作不会破坏筛选视图）

使用步骤：
1. 在 Google Cloud Console 创建 Service Account 并下载 JSON 密钥
2. 将 Service Account 邮箱添加为 Google Sheet 的编辑者
3. 将密钥放到 ./credentials/service_account.json
4. 复制 .env.example 为 .env 并填写配置
"""

import os
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional

import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


class GoogleSheetsSync:
    """Google Sheets 双向同步管理器"""

    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    def __init__(
        self,
        credentials_path: Optional[str] = None,
        spreadsheet_id: Optional[str] = None,
    ):
        """
        初始化同步管理器

        Args:
            credentials_path: Service Account JSON 密钥文件路径
            spreadsheet_id: Google Spreadsheet ID
        """
        self.credentials_path = credentials_path or os.getenv("GOOGLE_CREDENTIALS_PATH")
        self.spreadsheet_id = spreadsheet_id or os.getenv("SPREADSHEET_ID")
        self.local_sync_dir = Path(os.getenv("LOCAL_SYNC_DIR", "./synced_data"))
        self.local_sync_dir.mkdir(parents=True, exist_ok=True)

        if not self.credentials_path or not Path(self.credentials_path).exists():
            raise FileNotFoundError(
                f"Service Account 密钥文件未找到: {self.credentials_path}\n"
                "请按照 README.md 中的步骤设置 Google Cloud 项目和 Service Account"
            )

        self._client = None
        self._spreadsheet = None

    @property
    def client(self) -> gspread.Client:
        """懒加载 gspread 客户端"""
        if self._client is None:
            creds = Credentials.from_service_account_file(
                self.credentials_path, scopes=self.SCOPES
            )
            self._client = gspread.authorize(creds)
        return self._client

    @property
    def spreadsheet(self) -> gspread.Spreadsheet:
        """懒加载 Spreadsheet 对象"""
        if self._spreadsheet is None:
            self._spreadsheet = self.client.open_by_key(self.spreadsheet_id)
        return self._spreadsheet

    # ==================== 读取操作 ====================

    def list_sheets(self) -> list[dict]:
        """列出所有 Sheet 的名称和 ID"""
        worksheets = self.spreadsheet.worksheets()
        return [
            {
                "title": ws.title,
                "id": ws.id,
                "rows": ws.row_count,
                "cols": ws.col_count,
            }
            for ws in worksheets
        ]

    def pull_sheet(self, sheet_name: str) -> pd.DataFrame:
        """
        从云端拉取单个 Sheet 的数据为 DataFrame

        Args:
            sheet_name: Sheet 名称

        Returns:
            pd.DataFrame: Sheet 数据
        """
        worksheet = self.spreadsheet.worksheet(sheet_name)
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        return df

    def pull_all(self, save_local: bool = True) -> dict[str, pd.DataFrame]:
        """
        拉取所有 Sheet 的数据

        Args:
            save_local: 是否同时保存到本地文件

        Returns:
            dict: {sheet_name: DataFrame} 的字典
        """
        all_data = {}
        worksheets = self.spreadsheet.worksheets()

        for ws in worksheets:
            print(f"  📥 正在拉取: {ws.title} ...")
            try:
                data = ws.get_all_records()
                df = pd.DataFrame(data)
                all_data[ws.title] = df
                print(f"     ✅ {len(df)} 行 x {len(df.columns)} 列")
            except Exception as e:
                print(f"     ⚠️ 拉取 {ws.title} 失败: {e}")
                # 尝试使用 get_all_values 作为备选方案
                try:
                    values = ws.get_all_values()
                    if values:
                        df = pd.DataFrame(values[1:], columns=values[0])
                        all_data[ws.title] = df
                        print(f"     ✅ (备选方案) {len(df)} 行 x {len(df.columns)} 列")
                except Exception as e2:
                    print(f"     ❌ 备选方案也失败: {e2}")

        if save_local:
            self._save_local(all_data)

        return all_data

    def _save_local(self, all_data: dict[str, pd.DataFrame]):
        """保存所有数据到本地"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # 保存为 Excel（多 Sheet）
        excel_path = self.local_sync_dir / "synced_spreadsheet.xlsx"
        with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
            for sheet_name, df in all_data.items():
                # Excel Sheet 名称最长 31 个字符，且不能包含非法字符
                safe_name = sheet_name.replace("/", "_").replace("\\", "_").replace("?", "").replace("*", "").replace("[", "").replace("]", "").replace(":", "")[:31]
                df.to_excel(writer, sheet_name=safe_name, index=False)
        print(f"\n  💾 已保存到: {excel_path}")

        # 同时保存每个 Sheet 为独立 CSV（方便用代码读取）
        csv_dir = self.local_sync_dir / "csv"
        csv_dir.mkdir(exist_ok=True)
        for sheet_name, df in all_data.items():
            safe_name = sheet_name.replace("/", "_").replace("\\", "_")
            csv_path = csv_dir / f"{safe_name}.csv"
            df.to_csv(csv_path, index=False)

        # 保存元数据
        meta = {
            "last_sync": timestamp,
            "spreadsheet_id": self.spreadsheet_id,
            "sheets": {
                name: {
                    "rows": len(df),
                    "columns": list(df.columns),
                    "checksum": hashlib.md5(
                        df.to_csv(index=False).encode()
                    ).hexdigest(),
                }
                for name, df in all_data.items()
            },
        }
        meta_path = self.local_sync_dir / "sync_metadata.json"
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
        print(f"  📋 元数据已保存到: {meta_path}")

    # ==================== 写入操作 ====================

    def push_sheet(self, sheet_name: str, df: pd.DataFrame, clear_first: bool = True):
        """
        将 DataFrame 推送到指定 Sheet

        注意：此操作不会影响筛选视图（Filter Views），因为筛选视图是独立于数据的。
        但如果你使用的是基本筛选器（Basic Filter），clear_first=True 可能会清除它。

        Args:
            sheet_name: 目标 Sheet 名称
            df: 要推送的数据
            clear_first: 是否先清空 Sheet
        """
        try:
            worksheet = self.spreadsheet.worksheet(sheet_name)
        except gspread.exceptions.WorksheetNotFound:
            # 如果 Sheet 不存在，创建一个新的
            worksheet = self.spreadsheet.add_worksheet(
                title=sheet_name, rows=len(df) + 1, cols=len(df.columns)
            )
            print(f"  📄 已创建新 Sheet: {sheet_name}")

        if clear_first:
            worksheet.clear()

        # 准备数据：表头 + 数据行
        # 将所有值转换为字符串以避免类型问题
        header = df.columns.tolist()
        values = df.fillna("").astype(str).values.tolist()
        all_values = [header] + values

        worksheet.update(all_values, value_input_option="USER_ENTERED")
        print(f"  📤 已推送到 Sheet '{sheet_name}': {len(df)} 行")

    def update_cells(self, sheet_name: str, updates: list[dict]):
        """
        增量更新特定单元格（不影响其他数据和筛选条件）

        Args:
            sheet_name: Sheet 名称
            updates: 更新列表，每个元素为 {
                "row": 行号 (1-indexed, 包含表头),
                "col": 列号 (1-indexed),
                "value": 新值
            }

        示例：
            sync.update_cells("Sheet1", [
                {"row": 2, "col": 3, "value": "新值"},
                {"row": 5, "col": 1, "value": "更新"},
            ])
        """
        worksheet = self.spreadsheet.worksheet(sheet_name)

        cells_to_update = []
        for update in updates:
            cell = worksheet.cell(update["row"], update["col"])
            cell.value = update["value"]
            cells_to_update.append(cell)

        worksheet.update_cells(cells_to_update, value_input_option="USER_ENTERED")
        print(f"  ✏️ 已更新 {len(updates)} 个单元格")

    def update_row(self, sheet_name: str, row_index: int, row_data: dict):
        """
        更新指定行的数据（按列名匹配）

        Args:
            sheet_name: Sheet 名称
            row_index: 数据行索引 (0-indexed, 不包含表头)
            row_data: {列名: 值} 的字典
        """
        worksheet = self.spreadsheet.worksheet(sheet_name)
        headers = worksheet.row_values(1)

        updates = []
        for col_name, value in row_data.items():
            if col_name in headers:
                col_idx = headers.index(col_name) + 1  # 1-indexed
                updates.append({
                    "row": row_index + 2,  # +1 for header, +1 for 1-indexed
                    "col": col_idx,
                    "value": value,
                })

        if updates:
            self.update_cells(sheet_name, updates)

    def append_rows(self, sheet_name: str, df: pd.DataFrame):
        """
        在 Sheet 末尾追加行（不影响现有数据和筛选条件）

        Args:
            sheet_name: Sheet 名称
            df: 要追加的数据
        """
        worksheet = self.spreadsheet.worksheet(sheet_name)
        values = df.fillna("").astype(str).values.tolist()
        worksheet.append_rows(values, value_input_option="USER_ENTERED")
        print(f"  ➕ 已追加 {len(values)} 行到 '{sheet_name}'")

    # ==================== 智能同步 ====================

    def smart_sync(self, sheet_name: str, local_df: pd.DataFrame, key_column: str):
        """
        智能同步：对比本地和云端数据，仅更新有差异的行

        这是处理双向编辑的推荐方式。它会：
        1. 拉取云端最新数据
        2. 对比本地修改
        3. 仅推送有变化的行

        Args:
            sheet_name: Sheet 名称
            local_df: 本地修改后的 DataFrame
            key_column: 用于匹配行的唯一键列名

        Returns:
            dict: 同步报告
        """
        # 拉取云端最新数据
        cloud_df = self.pull_sheet(sheet_name)

        report = {
            "updated": 0,
            "added": 0,
            "unchanged": 0,
            "details": [],
        }

        # 获取 worksheet 和表头
        worksheet = self.spreadsheet.worksheet(sheet_name)
        headers = worksheet.row_values(1)

        # 对比和更新
        cloud_keys = set(cloud_df[key_column].astype(str).tolist()) if key_column in cloud_df.columns else set()
        local_keys = set(local_df[key_column].astype(str).tolist())

        for _, local_row in local_df.iterrows():
            key = str(local_row[key_column])

            if key in cloud_keys:
                # 行存在，检查是否有变化
                cloud_row = cloud_df[cloud_df[key_column].astype(str) == key].iloc[0]
                changes = {}

                for col in local_df.columns:
                    local_val = str(local_row[col]) if pd.notna(local_row[col]) else ""
                    cloud_val = str(cloud_row[col]) if col in cloud_row.index and pd.notna(cloud_row[col]) else ""
                    if local_val != cloud_val:
                        changes[col] = {"old": cloud_val, "new": local_val}

                if changes:
                    # 找到云端行号
                    cloud_idx = cloud_df[cloud_df[key_column].astype(str) == key].index[0]
                    self.update_row(sheet_name, cloud_idx, {
                        col: change["new"] for col, change in changes.items()
                    })
                    report["updated"] += 1
                    report["details"].append({
                        "key": key,
                        "action": "updated",
                        "changes": changes,
                    })
                else:
                    report["unchanged"] += 1
            else:
                # 新行，追加
                row_df = local_row.to_frame().T
                self.append_rows(sheet_name, row_df)
                report["added"] += 1
                report["details"].append({
                    "key": key,
                    "action": "added",
                })

        print(f"\n  📊 同步报告:")
        print(f"     更新: {report['updated']} 行")
        print(f"     新增: {report['added']} 行")
        print(f"     未变: {report['unchanged']} 行")

        return report


# ==================== 便捷函数 ====================

def quick_pull(spreadsheet_id: Optional[str] = None) -> dict[str, pd.DataFrame]:
    """快速拉取所有 Sheet 数据"""
    sync = GoogleSheetsSync(spreadsheet_id=spreadsheet_id)
    return sync.pull_all()


def quick_push(sheet_name: str, df: pd.DataFrame, spreadsheet_id: Optional[str] = None):
    """快速推送 DataFrame 到指定 Sheet"""
    sync = GoogleSheetsSync(spreadsheet_id=spreadsheet_id)
    sync.push_sheet(sheet_name, df)


if __name__ == "__main__":
    # 使用示例
    print("=" * 50)
    print("Google Sheets 同步工具")
    print("=" * 50)

    try:
        sync = GoogleSheetsSync()

        # 1. 列出所有 Sheet
        print("\n📋 所有 Sheet:")
        sheets = sync.list_sheets()
        for s in sheets:
            print(f"   - {s['title']} ({s['rows']} 行 x {s['cols']} 列)")

        # 2. 拉取所有数据
        print("\n📥 拉取所有数据...")
        all_data = sync.pull_all(save_local=True)

        # 3. 显示每个 Sheet 的前几行
        for name, df in all_data.items():
            print(f"\n📊 {name}:")
            print(df.head(3).to_string())

    except FileNotFoundError as e:
        print(f"\n❌ {e}")
        print("\n📝 设置步骤:")
        print("   1. 访问 https://console.cloud.google.com/")
        print("   2. 创建项目 → 启用 Sheets API 和 Drive API")
        print("   3. 创建 Service Account → 下载 JSON 密钥")
        print("   4. 将密钥放到 ./credentials/service_account.json")
        print("   5. 复制 .env.example 为 .env")
        print("   6. 在 Google Sheet 中将 Service Account 邮箱添加为编辑者")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
