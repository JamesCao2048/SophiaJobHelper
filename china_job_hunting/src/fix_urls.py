import pandas as pd

def fix_urls():
    file_path = 'china_job_list.xlsx'
    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return

    # Mapping of titles (or partial titles) to correct URLs
    url_mapping = {
        '浙江大学人工智能学院诚聘海内外英才': 'http://talent.zju.edu.cn/2025/0924/c71694a3085038/page.htm',
        '诚邀全球英才依托申报优青项目（海外）！': 'http://talent.zju.edu.cn/2025/0121/c71694a3013129/page.htm', # 浙江大学
        '2025年北京大学智能学院教学科研岗位招聘启事（更新）': 'https://hr.pku.edu.cn/rczp/jxky/4b3dd6354cf94c7d9646183b3b4590fd.htm',
        'https://hr.pku.edu.cn/rczp/jxky/4b3dd6354cf94c7d9646183b3d2b0e9a.htm': 'https://hr.pku.edu.cn/rczp/jxky/4b3dd6354cf94c7d9646183b3b4590fd.htm', # Fix previous error
        '2025海外优青丨诚邀依托上海交通大学人工智能学院申报！': 'https://soai.sjtu.edu.cn/cn/show/246',
        '复旦大学计算与智能创新学院招聘公告': 'https://ai.fudan.edu.cn/93/7b/c24260a758651/page.htm'
    }

    # Iterate through the DataFrame and update 'Positions Link' if it matches a key in url_mapping
    # Also handle partial matches if necessary, but exact match is safer first.
    
    count = 0
    for index, row in df.iterrows():
        current_val = row['Positions Link']
        if pd.isna(current_val):
            continue
            
        current_val = str(current_val).strip()
        
        # Check exact match
        if current_val in url_mapping:
            df.at[index, 'Positions Link'] = url_mapping[current_val]
            count += 1
            print(f"Updated row {index+2}: {current_val} -> {url_mapping[current_val]}")
        else:
            # Check partial match (e.g. if the excel has extra spaces or slightly different title)
            for title, url in url_mapping.items():
                if title in current_val:
                     df.at[index, 'Positions Link'] = url
                     count += 1
                     print(f"Updated row {index+2}: {current_val} -> {url}")
                     break

    if count > 0:
        df.to_excel(file_path, index=False)
        print(f"Successfully updated {count} URLs in {file_path}")
    else:
        print("No URLs needed to be updated.")

if __name__ == "__main__":
    fix_urls()
