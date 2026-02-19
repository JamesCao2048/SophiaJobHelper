#!/usr/bin/env python3
"""
Fill and validate job listing data from china_job_list Excel file.
"""

import pandas as pd
import requests
import re
import time
from urllib.parse import urlparse
from typing import Optional, Dict, Tuple
import json
from datetime import datetime

# Request settings
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}
REQUEST_TIMEOUT = 15
REQUEST_DELAY = 1.5  # seconds between requests


def validate_url(url: str) -> Tuple[bool, int, str]:
    """
    Validate if a URL is accessible.
    Returns: (is_valid, status_code, message)
    """
    if not url or pd.isna(url):
        return False, 0, "Empty URL"

    try:
        # Clean URL
        url = url.strip()
        if not url.startswith('http'):
            url = 'https://' + url

        # Special handling for WeChat articles
        if 'mp.weixin.qq.com' in url:
            # WeChat articles need GET, not HEAD
            response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT, allow_redirects=True)
        else:
            # Try HEAD first, fallback to GET
            try:
                response = requests.head(url, headers=HEADERS, timeout=REQUEST_TIMEOUT, allow_redirects=True)
                if response.status_code >= 400:
                    response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT, allow_redirects=True)
            except:
                response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT, allow_redirects=True)

        status = response.status_code
        if status < 400:
            return True, status, "Valid"
        else:
            return False, status, f"HTTP {status}"

    except requests.exceptions.Timeout:
        return False, 0, "Timeout"
    except requests.exceptions.ConnectionError:
        return False, 0, "Connection Error"
    except Exception as e:
        return False, 0, str(e)[:50]


def parse_chinese_date(date_str: str) -> Optional[str]:
    """
    Convert Chinese date formats to YYYY-MM-DD.
    Examples: "2026年3月1日" -> "2026-03-01"
    """
    if not date_str or pd.isna(date_str):
        return None

    date_str = str(date_str).strip()

    # Already in correct format
    if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        return date_str

    # Pattern: 2026年3月1日
    match = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', date_str)
    if match:
        y, m, d = match.groups()
        return f"{y}-{int(m):02d}-{int(d):02d}"

    # Pattern: 2026/3/1 or 2026.3.1
    match = re.search(r'(\d{4})[/.](\d{1,2})[/.](\d{1,2})', date_str)
    if match:
        y, m, d = match.groups()
        return f"{y}-{int(m):02d}-{int(d):02d}"

    return None


def extract_research_direction(text: str) -> str:
    """
    Determine research direction from text: AI, HCI, HAI, or combinations.
    """
    if not text:
        return ""

    text = text.lower()

    hci_keywords = ['hci', 'human-computer', '人机交互', '人机界面', 'user experience',
                    'ux', '用户体验', 'interaction design', '交互设计', 'ubiquitous',
                    '普适计算', 'wearable', '可穿戴', 'visualization', '可视化']

    ai_keywords = ['artificial intelligence', '人工智能', 'machine learning', '机器学习',
                   'deep learning', '深度学习', 'neural network', '神经网络', 'nlp',
                   '自然语言', 'computer vision', '计算机视觉', 'reinforcement learning']

    hai_keywords = ['human-centered ai', 'human-ai', 'hai', '以人为中心',
                    'human in the loop', 'human-centric', 'trustworthy ai', '可信ai',
                    'explainable ai', 'xai', '可解释']

    has_hci = any(kw in text for kw in hci_keywords)
    has_ai = any(kw in text for kw in ai_keywords)
    has_hai = any(kw in text for kw in hai_keywords)

    if has_hai:
        return "HAI"
    elif has_hci and has_ai:
        return "AI/HCI"
    elif has_hci:
        return "HCI"
    elif has_ai:
        return "AI"

    return ""


def extract_contact_info(text: str) -> Dict[str, str]:
    """
    Extract contact information from text.
    Returns dict with 'email', 'phone', 'wechat' keys.
    """
    result = {'email': '', 'phone': '', 'wechat': ''}

    if not text:
        return result

    # Email pattern
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    if email_match:
        result['email'] = email_match.group(0)

    # Phone pattern (Chinese mobile: 1xx-xxxx-xxxx or landline: 0xx-xxxxxxxx)
    phone_match = re.search(r'(?:86)?1[3-9]\d{9}|0\d{2,3}[-\s]?\d{7,8}', text)
    if phone_match:
        result['phone'] = phone_match.group(0)

    # WeChat pattern
    wechat_match = re.search(r'微信[：:\s]*([a-zA-Z0-9_-]+)', text)
    if wechat_match:
        result['wechat'] = wechat_match.group(1)

    return result


def fetch_page_content(url: str) -> Optional[str]:
    """
    Fetch page content as text.
    """
    if not url or pd.isna(url):
        return None

    try:
        url = url.strip()
        if not url.startswith('http'):
            url = 'https://' + url

        response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        response.encoding = response.apparent_encoding or 'utf-8'
        return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def validate_all_urls(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate all URLs in Positions Link column.
    Returns DataFrame with validation results.
    """
    results = []
    total = len(df)

    for idx, row in df.iterrows():
        url = row['Positions Link']
        uni = row['University&Department']

        print(f"[{idx+1}/{total}] Validating: {uni[:30]}...")
        is_valid, status, msg = validate_url(url)

        results.append({
            'index': idx,
            'university': uni,
            'url': url,
            'valid': is_valid,
            'status': status,
            'message': msg
        })

        time.sleep(REQUEST_DELAY)

    return pd.DataFrame(results)


def main():
    """Main entry point."""
    import argparse
    parser = argparse.ArgumentParser(description='Fill and validate job listing data')
    parser.add_argument('--input', default='china_job_list_2026-01-18.xlsx', help='Input Excel file')
    parser.add_argument('--output', default='china_job_list_2026-01-18_filled.xlsx', help='Output Excel file')
    parser.add_argument('--validate-only', action='store_true', help='Only validate URLs')
    parser.add_argument('--start', type=int, default=0, help='Start row index')
    parser.add_argument('--end', type=int, default=None, help='End row index')

    args = parser.parse_args()

    print(f"Loading {args.input}...")
    df = pd.read_excel(args.input)
    print(f"Loaded {len(df)} rows")

    if args.validate_only:
        print("\n=== URL Validation ===")
        results = validate_all_urls(df)

        valid_count = results['valid'].sum()
        print(f"\nResults: {valid_count}/{len(results)} URLs valid")

        # Show invalid URLs
        invalid = results[~results['valid']]
        if len(invalid) > 0:
            print("\nInvalid URLs:")
            for _, row in invalid.iterrows():
                print(f"  [{row['index']}] {row['university']}: {row['message']}")

        results.to_csv('url_validation_results.csv', index=False)
        print("\nResults saved to url_validation_results.csv")
    else:
        print("\n=== Data Filling Mode ===")
        print("Use --validate-only for URL validation")
        print("Full data filling requires web search integration")


if __name__ == '__main__':
    main()
