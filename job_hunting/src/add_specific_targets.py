import pandas as pd
from datetime import date
import os

# Define columns matching your project structure
columns = [
    'Deadline', 'University&Department', 'Positions Link', 'Position Title',
    'Position Research Direction (AI/HCI/HAI)', 'Lab/Research Center/Professor Link',
    'OverseaPolicy', 'Job Description', '联系方式', '联系方式的链接', '是否计划申请'
]

def create_entry(uni_dept, link, title, direction, policy, desc):
    return {
        'Deadline': 'Rolling/Check Website',
        'University&Department': uni_dept,
        'Positions Link': link,
        'Position Title': title,
        'Position Research Direction (AI/HCI/HAI)': direction,
        'Lab/Research Center/Professor Link': link,
        'OverseaPolicy': policy,
        'Job Description': desc,
        '联系方式': 'Check Website',
        '联系方式的链接': link,
        '是否计划申请': '是'
    }

# Data for the requested universities
new_targets = [
    create_entry(
        "深圳大学-计算机与软件学院",
        "https://csse.szu.edu.cn/vp/rczp",
        "Tenure-Track / 特聘教授 / 助理教授",
        "AI / HCI / Computer Vision",
        "海外优青 / 鹏城孔雀计划 / 百人计划",
        "深圳大学计算机学科CSRankings排名亮眼。提供极具竞争力的薪酬（年薪60万起+），享有深圳市'孔雀计划'人才补贴（160-300万免税），科研启动经费充足，拥有大数据系统计算技术国家工程实验室。"
    ),
    create_entry(
        "杜克昆山大学(DKU)-Data & CS",
        "https://dukekunshan.edu.cn/en/employment/faculty-positions",
        "Tenure-Track Assistant Professor",
        "Data Science / CS / AI",
        "Global Recruitment",
        "中外合作办学（Duke University授予学位），全英文教学环境，完全对接美国Tenure-track体系（3+1教学负担），提供具有全球竞争力的薪酬包（USD pegged）。"
    ),
    create_entry(
        "香港城市大学(东莞)-计算机科学",
        "https://www.cityu-dg.edu.cn/recruitment",
        "Assistant Professor / Associate Professor",
        "CS / AI / Data Science",
        "Global Recruitment / 粤港澳大湾区人才计划",
        "2024年正式成立，对标香港城市大学本部学术标准与薪酬体系。位于东莞松山湖科学城，享受大湾区科研资金与15%个税优惠政策。"
    ),
    create_entry(
        "北京交通大学-计算机与信息技术学院",
        "http://jgrsc.bjtu.edu.cn/rczp/",
        "“卓越百人”计划 / 教授 / 副教授",
        "AI / Traffic Intelligence / Network Science",
        "海外优青 / 卓越百人",
        "211双一流学科。交通特色鲜明，AI在轨道交通应用领域有深厚积累。'卓越百人'计划提供优厚待遇与独立博导资格。"
    ),
    create_entry(
        "南京理工大学-计算机科学与工程学院",
        "http://rczp.njust.edu.cn/",
        "“紫金学者” / 教授 / 副教授",
        "Pattern Recognition / AI / CV",
        "海外优青 / 紫金学者",
        "国防七子之一，拥有模式识别与智能系统国家重点学科（杨健教授团队）。提供充足科研经费与安家费，国防科研项目资源丰富。"
    ),
    create_entry(
        "南京航空航天大学-计算机科学与技术学院/人工智能学院",
        "http://rsc.nuaa.edu.cn/",
        "“长空学者” / 教授 / 副教授",
        "Pattern Recognition / AI / Neuro-computing",
        "海外优青 / 长空学者",
        "国防七子之一，航空航天特色。模式识别方向历史悠久，实力雄厚。'长空学者'提供高额岗位津贴。"
    )
]

# Create DataFrame
df = pd.DataFrame(new_targets, columns=columns)

# Output filename (today's date)
main_output_filename = f'china_job_list_{date.today()}.xlsx'

print(f"Preparing to add {len(df)} universities to {main_output_filename}...")

if os.path.exists(main_output_filename):
    try:
        df_existing = pd.read_excel(main_output_filename)
        # Merge, keeping the NEW definition if duplicates exist (based on University name)
        df_merged = pd.concat([df_existing, df]).drop_duplicates(subset=['University&Department'], keep='last')
        df_merged.to_excel(main_output_filename, index=False)
        print(f"✅ Success! Merged into {main_output_filename}. Total entries: {len(df_merged)}")
    except Exception as e:
        print(f"⚠️ Error reading existing file: {e}. Saving new file with only these targets.")
        df.to_excel(main_output_filename, index=False)
else:
    # Try to find base file if today's doesn't exist
    base_file = 'china_job_list.xlsx'
    if os.path.exists(base_file):
        print(f"Reading from base file {base_file}...")
        df_existing = pd.read_excel(base_file)
        df_merged = pd.concat([df_existing, df]).drop_duplicates(subset=['University&Department'], keep='last')
        df_merged.to_excel(main_output_filename, index=False)
        print(f"✅ Success! Created {main_output_filename} based on {base_file}.")
    else:
        df.to_excel(main_output_filename, index=False)
        print(f"✅ Created new file {main_output_filename}")
