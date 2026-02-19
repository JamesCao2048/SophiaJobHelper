import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import datetime

def extract_date(text):
    # Regex for YYYY-MM-DD, YYYY/MM/DD, YYYY年MM月DD日
    patterns = [
        r'(\d{4})[-/年](\d{1,2})[-/月](\d{1,2})[日]?',
        r'(\d{4})\.(\d{1,2})\.(\d{1,2})'
    ]
    
    # Look for "截止", "deadline" context
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if '截止' in line or 'Deadline' in line or '结束' in line:
            # Check this line and next line
            context = line
            if i + 1 < len(lines):
                context += " " + lines[i+1]
            
            for pattern in patterns:
                match = re.search(pattern, context)
                if match:
                    try:
                        year, month, day = match.groups()
                        return f"{year}-{int(month):02d}-{int(day):02d}"
                    except:
                        continue
    return None

def extract_contact(text):
    contacts = []
    # Email
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    # Filter out common false positives if any
    valid_emails = [e for e in emails if not e.endswith('.png') and not e.endswith('.jpg')]
    if valid_emails:
        contacts.append(f"Email: {', '.join(set(valid_emails))}")
    
    # Phone (Simple China mobile or landline)
    # phone_pattern = r'1[3-9]\d{9}|\d{3,4}-\d{7,8}'
    # phones = re.findall(phone_pattern, text)
    # if phones:
    #    contacts.append(f"Phone: {', '.join(set(phones))}")
        
    return "\n".join(contacts)

def extract_research_direction(text):
    directions = []
    text_lower = text.lower()
    if 'hci' in text_lower or 'human-computer interaction' in text_lower or '人机交互' in text_lower:
        directions.append('HCI')
    if 'ai' in text_lower or 'artificial intelligence' in text_lower or '人工智能' in text_lower:
        directions.append('AI')
    
    return "/".join(set(directions))

def extract_oversea_policy(text):
    if '海外优青' in text or '优青（海外）' in text or '优青(海外)' in text:
        return '海外优青'
    if '海外' in text and '人才' in text:
        return '海外人才计划'
    return None

def clean_text(text):
    if not text:
        return ""
    # Remove excessive newlines and spaces
    return re.sub(r'\s+', ' ', text).strip()

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fill_job_list():
    file_path = 'china_job_list.xlsx'
    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    updated_count = 0
    for index, row in df.iterrows():
        url = row['Positions Link']
        
        # Skip if URL is missing or not a string
        if pd.isna(url) or not isinstance(url, str) or not url.startswith('http'):
            continue
            
        print(f"Processing row {index+2}: {url}")
        
        try:
            # Use verify=False to bypass SSL errors for some university sites
            response = requests.get(url, headers=headers, timeout=15, verify=False)
            response.encoding = response.apparent_encoding # Fix encoding issues
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.extract()
                
                text = soup.get_text(separator='\n')
                cleaned_text = clean_text(text)
                
                # Fill Title if missing
                if pd.isna(row['Position Title']):
                    title = soup.title.string if soup.title else ""
                    # Try to find h1
                    h1 = soup.find('h1')
                    if h1:
                        title = h1.get_text().strip()
                    df.at[index, 'Position Title'] = title
                
                # Fill Deadline
                if pd.isna(row['Deadline']):
                    date = extract_date(text)
                    if date:
                        df.at[index, 'Deadline'] = date
                
                # Fill Research Direction
                if pd.isna(row['Position Research Direction (AI/HCI/HAI)']):
                    direction = extract_research_direction(text)
                    if direction:
                        df.at[index, 'Position Research Direction (AI/HCI/HAI)'] = direction

                # Fill OverseaPolicy
                if pd.isna(row['OverseaPolicy']):
                    policy = extract_oversea_policy(text)
                    if policy:
                        df.at[index, 'OverseaPolicy'] = policy
                
                # Fill Contact
                if pd.isna(row['联系方式']):
                    contact = extract_contact(text)
                    if contact:
                        df.at[index, '联系方式'] = contact
                
                # Fill Job Description (Limit length to avoid Excel issues, store summary or first N chars)
                # Ideally, we should summarize. For now, let's store the first 2000 chars of cleaned text
                if pd.isna(row['Job Description']):
                    df.at[index, 'Job Description'] = cleaned_text[:2000] + "..."
                
                updated_count += 1
                
            else:
                print(f"Failed to fetch {url}: Status {response.status_code}")
                
        except Exception as e:
            print(f"Error processing {url}: {e}")

    if updated_count > 0:
        df.to_excel(file_path, index=False)
        print(f"Successfully updated {updated_count} rows in {file_path}")
    else:
        print("No rows updated.")

if __name__ == "__main__":
    fill_job_list()
