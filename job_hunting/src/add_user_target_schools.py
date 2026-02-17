import pandas as pd
from datetime import date
import os

# Define columns
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

# Helper to create entry
def create_entry(uni_dept, link, title="Tenure-track Faculty / Overseas Talent", 
                 direction="AI / HCI", lab_link="", policy="海外优青", 
                 desc="诚聘海内外优秀人才，提供具有竞争力的薪酬和科研启动经费。"):
    return {
        'Deadline': 'Rolling',
        'University&Department': uni_dept,
        'Positions Link': link,
        'Position Title': title,
        'Position Research Direction (AI/HCI/HAI)': direction,
        'Lab/Research Center/Professor Link': lab_link if lab_link else link,
        'OverseaPolicy': policy,
        'Job Description': desc,
        '联系方式': '',
        '联系方式的链接': link,
        '是否计划申请': '是'
    }

data = []

# --- 1. Top Tier Campuses (Independent PhD Recruitment) ---
data.append(create_entry("清华大学深圳国际研究生院(SIGS)-信息学科", "https://www.sigs.tsinghua.edu.cn/1141/list.htm", 
                         direction="AI / HCI", policy="海外优青, 深圳孔雀计划", 
                         desc="具备独立博导资格，招生名额充足。深圳市提供额外人才补贴。"))

data.append(create_entry("哈尔滨工业大学(深圳)-计算机科学与技术学院", "http://www.hitsz.edu.cn/job/index.html", 
                         direction="CS / AI", policy="海外优青, 鹏城孔雀计划", 
                         desc="具备独立博导资格，共享本部A类学科资源。"))

data.append(create_entry("南京大学苏州校区-智能科学与技术学院", "https://rczp.nju.edu.cn/", 
                         direction="AI / Intelligent Systems", policy="海外优青, 姑苏领军人才", 
                         desc="新校区重点建设学院，具备南大博导资格，单列招生指标。"))

# --- 2. Sino-Foreign & HK Campuses ---
data.append(create_entry("香港中文大学(深圳)-数据科学学院(SDS)", "https://sds.cuhk.edu.cn/recruitment", 
                         title="Assistant/Associate Professor", direction="Data Science / AI", 
                         policy="Global Recruitment", desc="采用CUHK学术标准，独立博导资格，年薪对标国际一流大学。"))
data.append(create_entry("香港中文大学(深圳)-理工学院(SSE)", "https://sse.cuhk.edu.cn/recruitment", 
                         title="Assistant/Associate Professor", direction="CS / AI / Robotics", 
                         policy="Global Recruitment"))

data.append(create_entry("香港科技大学(广州)-信息枢纽(Information Hub)", "https://hkust-gz.edu.cn/careers", 
                         title="Assistant/Associate Professor", direction="AI / IoT / Data", 
                         policy="Global Recruitment", desc="枢纽-学域制，独立博导资格，重点发展交叉学科。"))

data.append(create_entry("上海纽约大学(NYU Shanghai)-计算机科学", "https://shanghai.nyu.edu/about/work/faculty-positions", 
                         title="Tenure-track Assistant Professor", direction="CS / Data Science", 
                         policy="Global Recruitment", desc="全英文教学，美国Tenure-track体系，全球顶尖薪酬。"))

data.append(create_entry("西交利物浦大学(XJTLU)-计算机科学与软件工程系", "https://www.xjtlu.edu.cn/en/about/career", 
                         title="Assistant/Associate Professor", direction="AI / HCI", 
                         policy="Global Recruitment", desc="位于苏州，全英文环境，薪酬有竞争力。"))

# --- 3. Additional Strong Universities ---
data.append(create_entry("苏州大学-计算机科学与技术学院", "http://scst.suda.edu.cn/rczp/list.htm", 
                         direction="HCI / CS", policy="海外优青, 优秀青年学者", 
                         desc="HCI是特色方向，提供有竞争力的薪酬和苏州安家费。"))

data.append(create_entry("上海大学-计算机工程与科学学院", "https://cs.shu.edu.cn/szdw/rczp.htm", 
                         direction="CS / AI", policy="海外优青", 
                         desc="上海市属211，AI方向有重点实验室支撑。"))

# Create DataFrame
df = pd.DataFrame(data, columns=columns)

# Save to temporary Excel
output_path = 'scan/additional_targets.xlsx'
df.to_excel(output_path, index=False)
print(f"Created {output_path} with {len(df)} entries.")

# Update main list
main_output_filename = f'china_job_list_{date.today()}.xlsx'
if os.path.exists(main_output_filename):
    try:
        df_existing = pd.read_excel(main_output_filename)
        # Merge, prioritizing new scan data for duplicates
        df_merged = pd.concat([df_existing, df]).drop_duplicates(subset=['University&Department'], keep='last')
        df_merged.to_excel(main_output_filename, index=False)
        print(f"Merged into {main_output_filename}. Total entries: {len(df_merged)}")
    except Exception as e:
        print(f"Error reading existing file: {e}. Saving new file only.")
        df.to_excel(main_output_filename, index=False)
else:
    # If today's file doesn't exist, try reading the base one or just save new
    if os.path.exists('china_job_list.xlsx'):
         df_existing = pd.read_excel('china_job_list.xlsx')
         df_merged = pd.concat([df_existing, df]).drop_duplicates(subset=['University&Department'], keep='last')
         df_merged.to_excel(main_output_filename, index=False)
    else:
        df.to_excel(main_output_filename, index=False)
    print(f"Created {main_output_filename}")
