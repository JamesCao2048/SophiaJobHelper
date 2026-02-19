"""
Google Sheets 导出工具 (保留格式)

功能：
1. 使用 Google Drive API 直接导出文件为 Excel 格式（保留样式、颜色、筛选器）
2. 用 openpyxl 重新保存，清理 Google 特有的非标准 XML 元素，确保 Mac Excel 能正常打开
"""

import os
import io
import tempfile
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import openpyxl

load_dotenv()

# 配置
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", "./credentials/service_account.json")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
OUTPUT_FILE = "./agent_sophia_job_list.xlsx"


def export_as_excel(output_path=None):
    output_path = output_path or OUTPUT_FILE
    print(f"正在导出 Spreadsheet ID: {SPREADSHEET_ID} ...")

    creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)

    mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    request = service.files().export_media(fileId=SPREADSHEET_ID, mimeType=mime_type)

    # 先下载到临时文件
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        tmp_path = tmp.name
        downloader = MediaIoBaseDownload(tmp, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"  下载进度: {int(status.progress() * 100)}%")

    # 用 openpyxl 重新保存，清理 Google 特有的非标准 XML 元素
    # 这样 Mac 上的 Microsoft Excel 才能正常打开
    print("  🧹 清理非标准 XML 元素...")
    wb = openpyxl.load_workbook(tmp_path)
    wb.save(output_path)
    wb.close()

    # 删除临时文件
    os.unlink(tmp_path)

    print(f"✅ 导出完成！文件已保存为: {output_path}")
    print("   此文件保留了样式、颜色和筛选器，且兼容 Mac Excel。")


if __name__ == '__main__':
    try:
        export_as_excel()
    except Exception as e:
        print(f"❌ 导出失败: {e}")
