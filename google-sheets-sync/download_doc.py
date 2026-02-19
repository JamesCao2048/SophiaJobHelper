"""
Download Google Doc Script

Exports a Google Doc as a .docx file using the existing Service Account.
"""

import os
import io
import argparse
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()

# Configuration
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
# Reuse existing credentials path
CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", "./credentials/service_account.json")

import socket

# Set default socket timeout (30 seconds)
socket.setdefaulttimeout(30)

def download_doc(doc_id):
    """
    Downloads a Google Doc as a DOCX file.
    """
    print(f"🚀 Script started. Target Doc ID: {doc_id}")
    print(f"🔧 Loading credentials from: {CREDENTIALS_PATH}")
    print(f"📡 Connecting to Google Drive API...")
    
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
        service = build('drive', 'v3', credentials=creds)
    except Exception as e:
        print(f"❌ Failed to authorize with credentials: {e}")
        return

    # Get file metadata to determine filename
    try:
        file_metadata = service.files().get(fileId=doc_id, fields='name').execute()
        file_name = file_metadata.get('name', 'google_doc_download')
        # Sanitize filename (remove potentially problematic characters)
        file_name = "".join([c for c in file_name if c.isalnum() or c in (' ', '-', '_')]).strip()
        output_path = f"{file_name}.docx"
    except Exception as e:
        print(f"❌ Failed to get file metadata (Check permissions): {e}")
        return

    print(f"Preparing to download: '{file_name}' (ID: {doc_id})")
    print(f"Exporting format: DOCX")

    # Export MIME type for Google Docs to DOCX
    mime_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

    try:
        request = service.files().export_media(fileId=doc_id, mimeType=mime_type)
        
        with io.FileIO(output_path, 'wb') as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"  Download progress: {int(status.progress() * 100)}%")

        print(f"✅ Download complete! Saved to: {os.path.abspath(output_path)}")
    except Exception as e:
        print(f"❌ Export failed: {e}")

if __name__ == '__main__':
    # Hardcoded doc ID from user request
    TARGET_DOC_ID = "1nkH2pbOrgiUYgLh0EKxcqL165zNH02ddVpfkVJO9egI"
    download_doc(TARGET_DOC_ID)
