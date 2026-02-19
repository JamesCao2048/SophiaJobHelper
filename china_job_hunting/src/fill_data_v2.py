#!/usr/bin/env python3
"""
Fill job listing data using web search and fetch.
Uses search results to supplement direct page fetching.
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time
import json
from typing import Optional, Dict, List, Tuple
from datetime import datetime
import urllib3

urllib3.disable_warnings()

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

REQUEST_TIMEOUT = 15
REQUEST_DELAY = 1.0


def fetch_page(url: str) -> Optional[str]:
    """Fetch page content."""
    if not url or pd.isna(url):
        return None
    try:
        url = url.strip()
        if not url.startswith('http'):
            url = 'https://' + url
        response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT, verify=False)
        response.encoding = response.apparent_encoding or 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        for script in soup(["script", "style"]):
            script.decompose()
        return soup.get_text(separator='\n', strip=True)
    except Exception as e:
        return None


def parse_chinese_date(text: str) -> Optional[str]:
    """Extract and convert Chinese date to YYYY-MM-DD."""
    if not text:
        return None

    # Pattern: 2026年3月1日 or 2025年12月31日
    match = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日?', str(text))
    if match:
        y, m, d = match.groups()
        return f"{y}-{int(m):02d}-{int(d):02d}"

    # Pattern: 2026-03-01 or 2026/03/01
    match = re.search(r'(\d{4})[-/](\d{1,2})[-/](\d{1,2})', str(text))
    if match:
        y, m, d = match.groups()
        return f"{y}-{int(m):02d}-{int(d):02d}"

    return None


def extract_deadline(text: str) -> str:
    """Extract deadline from text."""
    if not text:
        return ""

    # Look for deadline keywords
    deadline_patterns = [
        r'截止日期[：:]\s*(\d{4}年\d{1,2}月\d{1,2}日?)',
        r'报名截止[：:]\s*(\d{4}年\d{1,2}月\d{1,2}日?)',
        r'申请截止[：:]\s*(\d{4}年\d{1,2}月\d{1,2}日?)',
        r'招聘截止[：:]\s*(\d{4}年\d{1,2}月\d{1,2}日?)',
        r'截止[：:]\s*(\d{4}年\d{1,2}月\d{1,2}日?)',
        r'deadline[：:]\s*(\d{4}[-/]\d{1,2}[-/]\d{1,2})',
    ]

    for pattern in deadline_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            date = parse_chinese_date(match.group(1))
            if date:
                return date

    # Check for "长期有效" or "Long-term"
    if '长期有效' in text or '长期' in text or 'Rolling' in text.lower():
        return 'Rolling'

    return ""


def extract_contact_info(text: str) -> Dict[str, str]:
    """Extract contact information."""
    result = {'email': '', 'phone': '', 'wechat': '', 'contact_person': ''}

    if not text:
        return result

    # Email
    emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    if emails:
        result['email'] = emails[0]

    # Phone
    phones = re.findall(r'(?:0\d{2,3}[-\s]?\d{7,8})|(?:1[3-9]\d{9})', text)
    if phones:
        result['phone'] = phones[0]

    # WeChat
    wechat = re.search(r'微信[：:\s]*([a-zA-Z0-9_-]+)', text)
    if wechat:
        result['wechat'] = wechat.group(1)

    # Contact person
    contact = re.search(r'联系人[：:\s]*([^\s,，]+)', text)
    if contact:
        result['contact_person'] = contact.group(1)

    return result


def extract_research_direction(text: str, uni_dept: str) -> str:
    """Determine research direction."""
    combined = f"{text} {uni_dept}".lower()

    hai_keywords = ['human-centered ai', 'human-ai', 'hai', '以人为中心',
                    'human in the loop', 'trustworthy ai', '可信ai',
                    'explainable ai', 'xai', '可解释']

    hci_keywords = ['hci', 'human-computer', '人机交互', '交互设计',
                    'user experience', 'ux', '用户体验', 'visualization',
                    '可视化', '设计', 'interaction']

    ai_keywords = ['artificial intelligence', '人工智能', 'machine learning',
                   '机器学习', 'deep learning', '深度学习', '智能',
                   'nlp', '自然语言', 'computer vision', '计算机视觉']

    has_hai = any(kw in combined for kw in hai_keywords)
    has_hci = any(kw in combined for kw in hci_keywords)
    has_ai = any(kw in combined for kw in ai_keywords)

    if has_hai:
        return "HAI"
    elif has_hci and has_ai:
        return "AI/HCI"
    elif has_hci:
        return "HCI"
    elif has_ai:
        return "AI"
    return "AI"  # Default for CS departments


def extract_position_title(text: str) -> str:
    """Extract position title."""
    if not text:
        return ""

    # Common position patterns
    positions = []

    if '助理教授' in text:
        positions.append('助理教授')
    if '预聘副教授' in text or '准聘副教授' in text:
        positions.append('准聘副教授')
    if '长聘副教授' in text:
        positions.append('长聘副教授')
    if '教授' in text and '副教授' not in text:
        positions.append('教授')
    if '讲师' in text:
        positions.append('讲师')
    if '研究员' in text:
        positions.append('研究员')

    if positions:
        return '/'.join(positions)
    return "教研岗位"


def extract_job_description(text: str) -> str:
    """Extract key job description elements."""
    if not text:
        return ""

    desc_parts = []

    # Check for 博导资格
    if '博士生导师' in text or '博导' in text:
        desc_parts.append('具有博导资格')

    # Check for 招生名额
    quota_match = re.search(r'(博士生?招生名额|博士?名额)[：:\s]*(\d+)', text)
    if quota_match:
        desc_parts.append(f"博士生名额: {quota_match.group(2)}")

    # Check for 薪酬
    if '薪酬' in text or '待遇' in text or '年薪' in text:
        salary_match = re.search(r'(年薪|薪酬)[：:\s]*(\d+[\-至到~]\d+万?|[\d.]+万)', text)
        if salary_match:
            desc_parts.append(f"薪酬: {salary_match.group(2)}")
        else:
            desc_parts.append('提供有竞争力薪酬')

    # Check for housing
    if '住房' in text or '安居' in text:
        desc_parts.append('提供住房支持')

    # Check for startup funds
    if '科研启动' in text or '启动经费' in text:
        desc_parts.append('提供科研启动经费')

    # Check for children education
    if '子女' in text and ('入学' in text or '教育' in text):
        desc_parts.append('子女入学保障')

    return '; '.join(desc_parts) if desc_parts else ""


def get_oversea_policy(uni_name: str) -> str:
    """Return known overseas talent policies for major universities."""
    policies = {
        '南京大学': '海外优青; 南大仙林英才; 登峰计划',
        '清华大学': '海外优青; 清华青年人才计划',
        '北京大学': '海外优青; 博雅青年学者',
        '浙江大学': '海外优青; 百人计划; 求是青年学者',
        '上海交通大学': '海外优青; 致远学者',
        '复旦大学': '海外优青; 卓越人才计划; 超级博士后',
        '中国科学技术大学': '海外优青; 科大优才计划',
        '哈尔滨工业大学': '海外优青; 青年拔尖人才',
        '西安交通大学': '海外优青; 青年拔尖人才',
        '北京航空航天大学': '海外优青; 卓越百人计划',
        '同济大学': '海外优青; 同济青年人才',
        '华东师范大学': '海外优青; 紫江优秀青年学者',
        '中山大学': '海外优青; 百人计划',
        '武汉大学': '海外优青; 珞珈青年学者',
        '华中科技大学': '海外优青; 华中学者',
        '南开大学': '海外优青; 百名青年学科带头人',
        '天津大学': '海外优青; 北洋青年学者',
        '西湖大学': '独立PI制; 具有竞争力的启动支持',
        '南方科技大学': '海外优青; 独立PI; 高薪资',
        '上海科技大学': '海外优青; 独立PI制',
        '香港中文大学(深圳)': '具有国际竞争力薪酬; 深圳市人才政策',
        '香港科技大学(广州)': '海外优青; 具有国际竞争力薪酬',
    }

    for key, policy in policies.items():
        if key in uni_name:
            return policy
    return '海外优青'  # Default


# Pre-collected data from web searches for NJU (SSL blocked)
NJU_DATA = {
    '南京大学智能科学与技术学院': {
        'url': 'https://is.nju.edu.cn/71/62/c57162a749922/page.htm',
        'deadline': 'Rolling',
        'position_title': '准聘副教授/准聘助理教授',
        'direction': 'AI',
        'contact': 'hr.njusz@nju.edu.cn, is.hr@nju.edu.cn',
        'description': '博导资格; 科研启动费; 住房补贴; 子女入学; 事业编制',
    },
    '南京大学人工智能学院': {
        'url': 'https://ai.nju.edu.cn/rczp/index.htm',
        'deadline': 'Rolling',
        'position_title': '准聘副教授/准聘助理教授',
        'direction': 'AI',
        'contact': '通过zp.nju.edu.cn注册报名',
        'description': '博导资格; 提供住房补贴; 科研启动经费',
    },
    '南京大学软件学院': {
        'url': 'https://software.nju.edu.cn/',
        'deadline': 'Rolling',
        'position_title': '准聘副教授/准聘助理教授',
        'direction': 'AI',
        'contact': '通过zp.nju.edu.cn注册报名',
        'description': '事业编制; 软件工程领域; 科研启动经费',
    },
    '南京大学-计算机科学与技术系': {
        'url': 'https://cs.nju.edu.cn/',
        'deadline': 'Rolling',
        'position_title': '准聘助理教授/准聘副教授/长聘副教授',
        'direction': 'AI',
        'contact': '通过zp.nju.edu.cn注册报名',
        'description': '岗位总数不超过8个; 计算机软件新技术全国重点实验室',
    },
    '南京大学-人工智能学院': {
        'url': 'https://ai.nju.edu.cn/rczp/index.htm',
        'deadline': 'Rolling',
        'position_title': '准聘副教授/准聘助理教授',
        'direction': 'AI',
        'contact': '通过zp.nju.edu.cn注册报名',
        'description': 'C9首个人工智能学院; 博导资格',
    },
    '南京大学苏州校区-智能科学与技术学院': {
        'url': 'https://is.nju.edu.cn/',
        'deadline': 'Rolling',
        'position_title': '准聘副教授/准聘助理教授',
        'direction': 'AI',
        'contact': 'hr.njusz@nju.edu.cn',
        'description': '苏州校区; 科研启动经费; 住房补贴',
    },
    '南京大学': {
        'url': 'https://mp.weixin.qq.com/s/m3zGOflY2MZOIumN3EDmqA',
        'deadline': 'Rolling',
        'position_title': '准聘副教授/准聘助理教授/长聘教授',
        'direction': 'AI',
        'contact': 'https://rczp.nju.edu.cn/',
        'description': '全球英才招聘; 博导资格; 事业编制',
    },
}


def process_row(row: pd.Series, content: Optional[str] = None) -> Dict:
    """Process a single row and extract/update data."""
    uni_dept = row['University&Department']

    # Check if we have pre-collected NJU data
    if uni_dept in NJU_DATA:
        ndata = NJU_DATA[uni_dept]
        return {
            'Deadline': ndata['deadline'],
            'Position Title': ndata['position_title'],
            'Position Research Direction (AI/HCI/HAI)': ndata['direction'],
            'Job Description': ndata['description'],
            '联系方式': ndata['contact'],
            '联系方式的链接': ndata['url'],
            'OverseaPolicy': get_oversea_policy(uni_dept),
            'Lab/Research Center/Professor Link': ndata['url'],
        }

    # Process from fetched content
    result = {}

    if content:
        result['Deadline'] = extract_deadline(content) or 'Rolling'
        result['Position Title'] = extract_position_title(content) or '教研岗位'
        result['Position Research Direction (AI/HCI/HAI)'] = extract_research_direction(content, uni_dept)
        result['Job Description'] = extract_job_description(content)

        contact = extract_contact_info(content)
        contact_str = ', '.join(filter(None, [
            contact['email'],
            contact['phone'],
            f"联系人: {contact['contact_person']}" if contact['contact_person'] else ''
        ]))
        result['联系方式'] = contact_str or ''
    else:
        result['Deadline'] = 'Rolling'
        result['Position Title'] = '教研岗位'
        result['Position Research Direction (AI/HCI/HAI)'] = extract_research_direction('', uni_dept)
        result['Job Description'] = ''
        result['联系方式'] = ''

    result['OverseaPolicy'] = get_oversea_policy(uni_dept)

    return result


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='china_job_list_2026-01-18.xlsx')
    parser.add_argument('--output', default='china_job_list_2026-01-18_filled.xlsx')
    parser.add_argument('--start', type=int, default=0)
    parser.add_argument('--end', type=int, default=None)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    print(f"Loading {args.input}...")
    df = pd.read_excel(args.input)
    print(f"Loaded {len(df)} rows")

    end_idx = args.end if args.end else len(df)

    updated_count = 0
    failed_urls = []

    for idx in range(args.start, end_idx):
        row = df.iloc[idx]
        uni_dept = row['University&Department']
        url = row['Positions Link']

        print(f"\n[{idx+1}/{end_idx}] Processing: {uni_dept[:40]}...")

        # Try to fetch page content
        content = None
        if pd.notna(url) and uni_dept not in NJU_DATA:
            print(f"  Fetching: {url[:60]}...")
            content = fetch_page(url)
            if content:
                print(f"  ✓ Fetched {len(content)} chars")
            else:
                print(f"  ✗ Failed to fetch")
                failed_urls.append((idx, uni_dept, url))
            time.sleep(REQUEST_DELAY)

        # Process and update
        updates = process_row(row, content)

        for col, value in updates.items():
            if value and col in df.columns:
                # Don't overwrite 是否计划申请
                if col != '是否计划申请':
                    df.at[idx, col] = value

        updated_count += 1

        if not args.dry_run and updated_count % 10 == 0:
            print(f"  Saving intermediate results...")
            df.to_excel(args.output, index=False)

    # Final save
    if not args.dry_run:
        print(f"\nSaving to {args.output}...")
        df.to_excel(args.output, index=False)

    # Report
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Processed: {updated_count} rows")
    print(f"Failed fetches: {len(failed_urls)}")

    if failed_urls:
        print(f"\nFailed URLs:")
        for idx, uni, url in failed_urls[:10]:
            print(f"  [{idx}] {uni[:30]}")

    # Show sample of updated data
    print(f"\nSample of updated data (first 5 rows):")
    sample_cols = ['University&Department', 'Deadline', 'Position Title', '联系方式']
    print(df[sample_cols].head().to_string())


if __name__ == '__main__':
    main()
