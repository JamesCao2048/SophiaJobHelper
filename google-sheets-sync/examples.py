"""
使用示例：展示各种常见的操作场景
"""

import pandas as pd
from sheets_sync import GoogleSheetsSync


def example_pull_and_read():
    """示例 1: 拉取数据并在本地处理"""
    sync = GoogleSheetsSync()

    # 拉取所有 Sheet
    all_data = sync.pull_all(save_local=True)

    # 读取特定 Sheet
    for sheet_name, df in all_data.items():
        print(f"\n{'='*40}")
        print(f"Sheet: {sheet_name}")
        print(f"行数: {len(df)}, 列数: {len(df.columns)}")
        print(f"列名: {list(df.columns)}")
        print(df.head())


def example_read_local():
    """示例 2: 读取本地缓存的数据（不需要网络）"""
    # 读取整个 Excel 文件
    df_dict = pd.read_excel(
        "./synced_data/synced_spreadsheet.xlsx",
        sheet_name=None,  # None = 读取所有 Sheet
    )

    for sheet_name, df in df_dict.items():
        print(f"\nSheet: {sheet_name}, 行数: {len(df)}")

    # 或者读取特定 CSV
    # df = pd.read_csv("./synced_data/csv/某个Sheet名.csv")


def example_modify_and_push():
    """示例 3: 修改数据后推送回云端"""
    sync = GoogleSheetsSync()

    # 拉取特定 Sheet
    df = sync.pull_sheet("Sheet1")  # 替换为你的 Sheet 名

    # 本地修改
    # df.loc[0, "某列"] = "新值"
    # df["新列"] = "默认值"

    # 推送回云端
    sync.push_sheet("Sheet1", df)


def example_incremental_update():
    """示例 4: 仅更新特定单元格（推荐，不影响筛选条件）"""
    sync = GoogleSheetsSync()

    # 更新特定单元格
    sync.update_cells("Sheet1", [
        {"row": 2, "col": 3, "value": "更新的值"},  # 第2行第3列
    ])

    # 更新指定行（通过列名匹配）
    sync.update_row("Sheet1", row_index=0, row_data={
        "状态": "已完成",
        "备注": "通过代码更新",
    })


def example_append_new_data():
    """示例 5: 追加新数据（不影响现有数据）"""
    sync = GoogleSheetsSync()

    # 创建新数据
    new_data = pd.DataFrame({
        "名称": ["新项目A", "新项目B"],
        "状态": ["进行中", "待开始"],
        "日期": ["2026-02-18", "2026-02-19"],
    })

    # 追加到 Sheet 末尾
    sync.append_rows("Sheet1", new_data)


def example_smart_sync():
    """
    示例 6: 智能同步（处理双向编辑的最佳方式）

    这在你和别人都在编辑同一个 Sheet 时特别有用：
    1. 拉取最新云端数据
    2. 你在本地做修改
    3. 用 smart_sync 推送，只更新你改动的部分
    """
    sync = GoogleSheetsSync()

    # 1. 先拉取最新数据
    df = sync.pull_sheet("Sheet1")

    # 2. 在本地做修改
    # df.loc[df["名称"] == "某项", "状态"] = "已完成"

    # 3. 智能同步 - 仅推送有变化的行
    report = sync.smart_sync(
        sheet_name="Sheet1",
        local_df=df,
        key_column="名称",  # 用于匹配行的唯一键
    )

    print(f"同步完成: {report}")


if __name__ == "__main__":
    print("选择要运行的示例:")
    print("1. 拉取并读取数据")
    print("2. 读取本地缓存")
    print("3. 修改并推送")
    print("4. 增量更新")
    print("5. 追加新数据")
    print("6. 智能同步")

    choice = input("\n请输入数字 (1-6): ").strip()

    examples = {
        "1": example_pull_and_read,
        "2": example_read_local,
        "3": example_modify_and_push,
        "4": example_incremental_update,
        "5": example_append_new_data,
        "6": example_smart_sync,
    }

    if choice in examples:
        examples[choice]()
    else:
        print("无效选择")
