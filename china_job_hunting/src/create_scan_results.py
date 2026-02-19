import pandas as pd
from datetime import date
import os

# Define columns as per CLAUDE.md
columns = [
    'Deadline',
    'University&Department',
    'Positions Link',
    'Position Title',
    'Position Research Direction (AI/HCI/HAI)',
    'Lab/Research Center/Professor Link',
    'OverseaPolicy',
    'Job Description',
    '联系方式',
    '联系方式的链接',
    '是否计划申请'
]

# Initial data found from search
data = [
    {
        'Deadline': 'Rolling',
        'University&Department': '清华大学-计算机科学与技术系(人机交互与媒体集成研究所)',
        'Positions Link': 'https://www.cs.tsinghua.edu.cn/rczp.htm',
        'Position Title': 'Assistant/Associate Professor',
        'Position Research Direction (AI/HCI/HAI)': 'HCI',
        'Lab/Research Center/Professor Link': 'http://media.cs.tsinghua.edu.cn/',
        'OverseaPolicy': '海外优青',
        'Job Description': '长期开放海外优秀人才引进，重点支持申请国家自然科学基金委“海外优青”项目。',
        '联系方式': '',
        '联系方式的链接': 'https://www.tsinghua.edu.cn/zpxx.htm',
        '是否计划申请': '是'
    },
    {
        'Deadline': 'Rolling',
        'University&Department': '北京大学-前沿计算研究中心(CFCS)',
        'Positions Link': 'https://cfcs.pku.edu.cn/join/faculty/index.htm',
        'Position Title': 'Tenure-track Assistant/Associate Professor',
        'Position Research Direction (AI/HCI/HAI)': 'AI/HCI',
        'Lab/Research Center/Professor Link': 'https://cfcs.pku.edu.cn/',
        'OverseaPolicy': '海外优青',
        'Job Description': '对标美国Top高校，提供具有国际竞争力的薪酬。长期接受申请。',
        '联系方式': '',
        '联系方式的链接': 'https://cfcs.pku.edu.cn/join/faculty/index.htm',
        '是否计划申请': '是'
    },
    {
        'Deadline': 'Rolling',
        'University&Department': '浙江大学-计算机科学与技术学院(CAD&CG国家重点实验室)',
        'Positions Link': 'http://www.cs.zju.edu.cn/13224/list.htm',
        'Position Title': '“百人计划”研究员',
        'Position Research Direction (AI/HCI/HAI)': 'HCI/Graphics',
        'Lab/Research Center/Professor Link': 'http://www.cad.zju.edu.cn/',
        'OverseaPolicy': '海外优青, 百人计划',
        'Job Description': '给予博导资格和充裕的启动经费，全力支持申报“海外优青”。',
        '联系方式': '',
        '联系方式的链接': 'http://www.cs.zju.edu.cn/13224/list.htm',
        '是否计划申请': '是'
    },
    {
        'Deadline': 'Rolling',
        'University&Department': '上海交通大学-约翰·霍普克罗夫特计算机科学中心',
        'Positions Link': 'https://jhc.sjtu.edu.cn/recruit/',
        'Position Title': 'Tenure-track Associate/Assistant Professor',
        'Position Research Direction (AI/HCI/HAI)': 'AI/HCI',
        'Lab/Research Center/Professor Link': 'https://jhc.sjtu.edu.cn/',
        'OverseaPolicy': '海外优青',
        'Job Description': '采用国际化评估体系，薪酬待遇优厚。提供50-80万+年薪及300-800万科研启动经费。',
        '联系方式': '',
        '联系方式的链接': 'https://jhc.sjtu.edu.cn/recruit/',
        '是否计划申请': '是'
    },
    {
        'Deadline': 'Rolling',
        'University&Department': '北京航空航天大学-计算机学院(虚拟现实技术与系统全国重点实验室)',
        'Positions Link': 'http://scse.buaa.edu.cn/rczp/szdw.htm',
        'Position Title': '准聘/长聘教职',
        'Position Research Direction (AI/HCI/HAI)': 'VR/AR/HCI',
        'Lab/Research Center/Professor Link': 'http://vrlab.buaa.edu.cn/',
        'OverseaPolicy': '海外优青, 卓越百人',
        'Job Description': '长期招聘海内外优秀青年学者，大力支持“海外优青”申报。',
        '联系方式': '',
        '联系方式的链接': 'http://scse.buaa.edu.cn/rczp/szdw.htm',
        '是否计划申请': '是'
    }
]

# Create DataFrame
df = pd.DataFrame(data, columns=columns)

# Ensure output directory exists
os.makedirs('scan', exist_ok=True)

# Save to Excel
output_path = 'scan/target_school_list.xlsx'
df.to_excel(output_path, index=False)
print(f"Created {output_path}")

# Also update the main list if requested, but task says 'scan' focuses on searching and saving to scan folder.
# The 'scan' task description says: "创建新的hina_job_list_{$crawl_update_date}.xlsx，将结果保存到新的文件里。"
# It seems I should also create the main file.

main_output_filename = f'china_job_list_{date.today()}.xlsx'
# Check if original exists to merge? 
# "根据已有的最新的hina_job_list_{$crawl_update_date}.xlsx...创建新的..."
# Since I'm in 'scan' mode, I'll just save the result as the new main list for now, or merge if I can read the old one.
# For safety, I will read the existing one if it exists.

existing_file = 'china_job_list.xlsx'
if os.path.exists(existing_file):
    try:
        df_existing = pd.read_excel(existing_file)
        # Merge
        df_merged = pd.concat([df_existing, df]).drop_duplicates(subset=['University&Department', 'Positions Link'], keep='last')
        df_merged.to_excel(main_output_filename, index=False)
        print(f"Merged and created {main_output_filename}")
    except Exception as e:
        print(f"Error reading existing file: {e}. Saving new file only.")
        df.to_excel(main_output_filename, index=False)
else:
    df.to_excel(main_output_filename, index=False)
    print(f"Created {main_output_filename}")
