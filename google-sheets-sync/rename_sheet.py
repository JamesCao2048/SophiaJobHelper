"""
Google Drive 文件重命名脚本

功能：
将指定的 Google Sheet 文件名加上 "agent_" 前缀。
"""

import os
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()

# 配置
SCOPES = ['https://www.googleapis.com/auth/drive']
CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", "./credentials/service_account.json")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

def rename_spreadsheet():
    print(f"正在连接 Google Drive API...")
    
    creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)

    # 1. 获取当前文件名
    file_metadata = service.files().get(fileId=SPREADSHEET_ID, fields='name').execute()
    current_name = file_metadata.get('name')
    print(f"当前文件名: {current_name}")

    # 2. 检查是否已经有前缀
    if current_name.startswith("agent_"):
        print("文件名已经包含 'agent_' 前缀，跳过重命名。")
        return

    # 3. 更新文件名
    new_name = f"agent_{current_name}"
    file_update_metadata = {'name': new_name}
    
    updated_file = service.files().update(
        fileId=SPREADSHEET_ID,
        body=file_update_metadata,
        fields='name'
    ).execute()

    print(f"✅ 文件重命名成功！")
    print(f"新文件名: {updated_file.get('name')}")

if __name__ == '__main__':
    try:
        rename_spreadsheet()
    except Exception as e:
        print(f"❌ 重命名失败: {e}")
