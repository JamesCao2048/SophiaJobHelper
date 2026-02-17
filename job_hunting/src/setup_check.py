import pandas as pd
import re

def is_valid_url(url):
    if pd.isna(url):
        return True # Empty is allowed for now, or should be flagged? Let's flag non-empty non-urls
    if not isinstance(url, str):
        return False
    # Simple regex for URL
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
        r'localhost|' # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

def setup_check():
    file_path = 'china_job_list.xlsx'
    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return

    # 1. Check Columns (Already verified manually, but good to have in script)
    expected_columns = [
        'Deadline', 'University&Department', 'Positions Link', 'Position Title',
        'Position Research Direction (AI/HCI/HAI)', 'Lab/Research Center/Professor Link',
        'OverseaPolicy', 'Job Description', '联系方式', '联系方式的链接', '是否计划申请'
    ]
    
    missing_cols = [col for col in expected_columns if col not in df.columns]
    if missing_cols:
        print(f"Missing columns: {missing_cols}")
        # Add missing columns
        for col in missing_cols:
            df[col] = None
        print("Added missing columns.")
    
    # 2. Check Data Format (URL check)
    url_cols = ['Positions Link', 'Lab/Research Center/Professor Link', '联系方式的链接']
    for col in url_cols:
        if col in df.columns:
            invalid_urls = df[~df[col].apply(is_valid_url) & df[col].notna()]
            if not invalid_urls.empty:
                print(f"Warning: Found invalid URLs in column '{col}':")
                for idx, row in invalid_urls.iterrows():
                    print(f"  Row {idx+2}: {row[col]}") # Excel row is index+2

    # 3. Check Duplicates
    if 'University&Department' in df.columns and 'Position Title' in df.columns:
        duplicates = df[df.duplicated(subset=['University&Department', 'Position Title'], keep=False)]
        if not duplicates.empty:
            print("Warning: Found duplicate entries for University&Department and Position Title:")
            print(duplicates[['University&Department', 'Position Title']])
        else:
            print("No duplicates found.")

    # Save changes if any columns were added
    if missing_cols:
        df.to_excel(file_path, index=False)
        print(f"Updated {file_path} with correct columns.")
    else:
        print("Column structure is correct.")

if __name__ == "__main__":
    setup_check()
