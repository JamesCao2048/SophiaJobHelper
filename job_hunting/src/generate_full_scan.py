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
                 desc="诚聘海内外优秀人才，提供具有竞争力的薪酬和科研启动经费。重点支持海外优青申报。"):
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

# --- 1. Top Tier ---
data.append(create_entry("清华大学-计算机科学与技术系", "https://www.cs.tsinghua.edu.cn/rczp.htm", direction="HCI / AI", lab_link="http://media.cs.tsinghua.edu.cn/"))
data.append(create_entry("清华大学-交叉信息研究院(IIIS)", "https://iiis.tsinghua.edu.cn/list-266-1.html", direction="AI / Theory"))
data.append(create_entry("清华大学-美术学院(信息艺术设计系)", "https://www.ad.tsinghua.edu.cn/", direction="HCI / Interaction Design"))

data.append(create_entry("北京大学-智能学院", "https://ai.pku.edu.cn/rczp/index.htm", direction="AI / Vision / HCI"))
data.append(create_entry("北京大学-前沿计算研究中心(CFCS)", "https://cfcs.pku.edu.cn/join/faculty/index.htm", direction="AI / HCI / Graphics"))
data.append(create_entry("北京大学-计算机学院", "https://cs.pku.edu.cn/", direction="CS / AI"))

data.append(create_entry("浙江大学-计算机科学与技术学院(CAD&CG)", "http://www.cs.zju.edu.cn/13224/list.htm", direction="Graphics / HCI / AI", lab_link="http://www.cad.zju.edu.cn/"))
data.append(create_entry("浙江大学-上海高等研究院", "http://talent.zju.edu.cn/", direction="AI + X"))

data.append(create_entry("上海交通大学-电子信息与电气工程学院", "https://www.seiee.sjtu.edu.cn/xzzp_xb.html", direction="CS / AI"))
data.append(create_entry("上海交通大学-约翰·霍普克罗夫特中心", "https://jhc.sjtu.edu.cn/recruit/", direction="CS / AI"))
data.append(create_entry("上海交通大学-人工智能研究院", "https://ai.sjtu.edu.cn/", direction="AI"))

data.append(create_entry("南京大学-计算机科学与技术系", "https://cs.nju.edu.cn/1654/list.htm", direction="CS / AI"))
data.append(create_entry("南京大学-人工智能学院", "https://ai.nju.edu.cn/rczp/index.htm", direction="AI / Machine Learning"))

data.append(create_entry("中国科学技术大学-计算机科学与技术学院", "http://cs.ustc.edu.cn/rczp/list.htm", direction="CS / AI"))
data.append(create_entry("中国科学技术大学-信息科学技术学院", "http://employment.ustc.edu.cn/cn/", direction="AI / Brain-inspired Intelligence"))

data.append(create_entry("复旦大学-计算机科学技术学院", "https://cs.fudan.edu.cn/22228/list.htm", direction="CS / HCI / AI"))
data.append(create_entry("复旦大学-智能复杂体系实验室", "https://hr.fudan.edu.cn/", direction="AI / Complex Systems"))

data.append(create_entry("哈尔滨工业大学-计算学部", "http://computing.hit.edu.cn/11467/list.htm", direction="CS / AI / NLP"))
data.append(create_entry("哈尔滨工业大学-人工智能研究院", "http://www.hit.edu.cn/11540/list.htm", direction="AI"))

data.append(create_entry("西安交通大学-人工智能学院", "http://hr.xjtu.edu.cn/", direction="AI / Vision"))

# --- 2. North China ---
data.append(create_entry("北京航空航天大学-计算机学院", "http://scse.buaa.edu.cn/rczp/szdw.htm", direction="VR / HCI / AI"))
data.append(create_entry("北京航空航天大学-人工智能研究院", "http://rsc.buaa.edu.cn/", direction="AI"))

data.append(create_entry("北京理工大学-计算机学院", "https://cs.bit.edu.cn/xygk/rczp/index.htm", direction="CS / AI"))
data.append(create_entry("中国人民大学-高瓴人工智能学院", "http://ai.ruc.edu.cn/joinus/", direction="AI / IR"))
data.append(create_entry("北京师范大学-人工智能学院", "https://ai.bnu.edu.cn/rczp/index.htm", direction="AI / EdTech"))
data.append(create_entry("南开大学-人工智能学院", "https://ai.nankai.edu.cn/rczp/list.htm", direction="AI / Robotics"))
data.append(create_entry("天津大学-智能与计算学部", "http://cic.tju.edu.cn/szdw/rczp.htm", direction="CS / AI"))
data.append(create_entry("山东大学-计算机科学与技术学院", "https://www.cs.sdu.edu.cn/szdw/rczp.htm", direction="CS / VR / HCI"))

# --- 3. East China ---
data.append(create_entry("同济大学-设计创意学院", "https://tjdi.tongji.edu.cn/", direction="HCI / Design", desc="HCI强校，设计与智能交叉。"))
data.append(create_entry("同济大学-电子与信息工程学院", "https://see.tongji.edu.cn/szdw/rczp.htm", direction="CS / AI"))
data.append(create_entry("华东师范大学-计算机科学与技术学院", "https://cs.ecnu.edu.cn/14468/list.htm", direction="CS / AI"))
data.append(create_entry("东南大学-计算机科学与工程学院", "https://rsc.seu.edu.cn/", direction="CS / AI"))
data.append(create_entry("厦门大学-信息学院", "https://informatics.xmu.edu.cn/rczp.htm", direction="AI / CS"))
data.append(create_entry("华南理工大学-计算机科学与工程学院", "https://www2.scut.edu.cn/cs/rczp/list.htm", direction="CS / AI"))
data.append(create_entry("中山大学-计算机学院", "https://cse.sysu.edu.cn/rczp", direction="CS / AI"))

# --- 4. Central/West/NorthEast ---
data.append(create_entry("华中科技大学-计算机科学与技术学院", "http://cs.hust.edu.cn/szdw/rczp.htm", direction="CS / Storage / AI"))
data.append(create_entry("武汉大学-计算机学院", "http://cs.whu.edu.cn/rczp.htm", direction="CS / AI"))
data.append(create_entry("中南大学-计算机学院", "http://rsc.csu.edu.cn/", direction="CS / AI"))
data.append(create_entry("湖南大学-信息科学与工程学院", "http://csee.hnu.edu.cn/rczp.htm", direction="CS / AI"))
data.append(create_entry("四川大学-计算机学院", "https://cs.scu.edu.cn/rczp.htm", direction="CS / AI"))
data.append(create_entry("电子科技大学-计算机科学与工程学院", "https://www.scse.uestc.edu.cn/szdw/rczp.htm", direction="CS / AI / OS"))
data.append(create_entry("重庆大学-计算机学院", "http://www.cs.cqu.edu.cn/szdw/rczp.htm", direction="CS / AI"))
data.append(create_entry("西北工业大学-计算机学院", "https://jsj.nwpu.edu.cn/rczp.htm", direction="CS / AI"))
data.append(create_entry("吉林大学-计算机科学与技术学院", "https://ccst.jlu.edu.cn/szdw/rczp.htm", direction="CS / AI"))
data.append(create_entry("大连理工大学-计算机科学与技术学院", "http://cs.dlut.edu.cn/szdw/rczp.htm", direction="CS / AI"))
data.append(create_entry("东北大学-计算机科学与工程学院", "http://www.cse.neu.edu.cn/", direction="CS / AI"))
data.append(create_entry("兰州大学-信息科学与工程学院", "http://ldrsc.lzu.edu.cn/", direction="CS / AI"))

# --- 5. Emerging & Strong 211 ---
data.append(create_entry("西湖大学-工学院", "https://www.westlake.edu.cn/Careers/Open_Positions/Faculty/202006/t20200628_6146.shtml", direction="AI / Data Science"))
data.append(create_entry("南方科技大学-计算机科学与工程系", "https://cse.sustech.edu.cn/job/index.html", direction="CS / AI"))
data.append(create_entry("上海科技大学-信息科学与技术学院", "https://sist.shanghaitech.edu.cn/2723/list.htm", direction="CS / AI / Vision"))
data.append(create_entry("北京邮电大学-计算机学院", "https://cs.bupt.edu.cn/szdw/rczp.htm", direction="CS / AI"))
data.append(create_entry("北京邮电大学-交互技术与体验系统文旅部重点实验室", "https://www.bupt.edu.cn/rczp.htm", direction="HCI", desc="HCI特色实验室"))
data.append(create_entry("西安电子科技大学-计算机科学与技术学院", "https://cs.xidian.edu.cn/szdw/rczp.htm", direction="CS / AI"))
data.append(create_entry("西安电子科技大学-人工智能学院", "https://sai.xidian.edu.cn/", direction="AI"))

# Create DataFrame
df = pd.DataFrame(data, columns=columns)

# Save to Excel
output_path = 'scan/target_school_list.xlsx'
df.to_excel(output_path, index=False)
print(f"Created {output_path} with {len(df)} entries.")

# Update main list
main_output_filename = f'china_job_list_{date.today()}.xlsx'
if os.path.exists('china_job_list.xlsx'):
    try:
        df_existing = pd.read_excel('china_job_list.xlsx')
        # Merge, prioritizing new scan data for duplicates
        df_merged = pd.concat([df_existing, df]).drop_duplicates(subset=['University&Department'], keep='last')
        df_merged.to_excel(main_output_filename, index=False)
        print(f"Merged and created {main_output_filename}")
    except Exception as e:
        print(f"Error reading existing file: {e}. Saving new file only.")
        df.to_excel(main_output_filename, index=False)
else:
    df.to_excel(main_output_filename, index=False)
    print(f"Created {main_output_filename}")
