import os
import shutil
import re
import argparse

def parse_summary(summary_path):
    """
    Parses the summary.md file to extract key information for the cover letter.
    """
    with open(summary_path, 'r', encoding='utf-8') as f:
        content = f.read()

    info = {}
    
    # Extract University Name from Title
    # e.g. # 山东大学 (Shandong University) - 岗位总结
    uni_match = re.search(r'# .*?\((.*?)\)', content)
    if uni_match:
        info['university_name'] = uni_match.group(1)
    else:
        info['university_name'] = "University"

    # Extract Department
    # - **所属学院**: 计算机科学与技术学院 (School of Computer Science and Technology)
    dept_match = re.search(r'- \*\*所属学院\*\*: .*?\((.*?)\)', content)
    if dept_match:
        info['department_name'] = dept_match.group(1)
    else:
        # Try simpler match
        dept_match = re.search(r'- \*\*所属学院\*\*: (.*)', content)
        if dept_match:
             info['department_name'] = dept_match.group(1).split('-')[0].strip() # Remove " - Qingdao Campus" if any
        else:
             info['department_name'] = "Department of Computer Science"

    # Extract Position
    # - **目标岗位**: 齐鲁青年学者 (Qilu Young Scholar) / 教授 / 副教授
    pos_match = re.search(r'- \*\*目标岗位\*\*: (.*)', content)
    if pos_match:
        # Prefer English part if available
        en_pos = re.search(r'\((.*?)\)', pos_match.group(1))
        if en_pos:
            info['position'] = en_pos.group(1) + " / Professor"
        else:
            info['position'] = "Faculty Position"
    else:
        info['position'] = "Faculty Position"
        
    # Extract Research Direction
    # - **关键研究方向**: Human-Computer Interaction (HCI), ...
    dir_match = re.search(r'- \*\*关键研究方向\*\*: (.*)', content)
    if dir_match:
        info['research_focus'] = dir_match.group(1)
    else:
        info['research_focus'] = "Human-Computer Interaction and AI"

    # Extract Key Person
    # - **领军人物**: 孟祥旭 (Meng Xiangxu) 教授
    person_match = re.search(r'- \*\*领军人物\*\*: (.*)', content)
    if person_match:
        # Extract name
        name_match = re.search(r'\((.*?)\)', person_match.group(1))
        if name_match:
            info['key_person'] = name_match.group(1)
        else:
            info['key_person'] = person_match.group(1).replace("教授", "").strip()
    else:
        info['key_person'] = "faculty members"

    return info

def generate_cover_letter(uni_dir, info, template_dir):
    """
    Generates main.tex and copies necessary files.
    """
    target_dir = os.path.join(uni_dir, 'Cover_Letter')
    os.makedirs(target_dir, exist_ok=True)

    # Copy dependencies
    for file in ['OUCletter.cls', 'jhu-icon.pdf', 'signature.pdf', 'content']:
        src = os.path.join(template_dir, file)
        dst = os.path.join(target_dir, file)
        if os.path.isdir(src):
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)

    # Read template
    with open(os.path.join(template_dir, 'main.tex'), 'r', encoding='utf-8') as f:
        template = f.read()

    # Replace content
    # \newcommand{\searchingfocus}{\textbf{Software Engineering}}
    # \newcommand{\departmentname}{Department of Electrical and Computer Engineering}
    # \newcommand{\universityname}{McGill University}
    
    # Escape backslashes in info values to prevent regex errors
    def escape_tex(text):
        return text.replace('\\', '\\\\')

    # We replace the definitions
    template = re.sub(r'\\newcommand{\\searchingfocus}{.*}', 
                      r'\\newcommand{\\searchingfocus}{\\textbf{' + escape_tex(info['research_focus']) + '}}', template)
    
    template = re.sub(r'\\newcommand{\\departmentname}{.*}', 
                      r'\\newcommand{\\departmentname}{' + escape_tex(info['department_name']) + '}', template)
    
    template = re.sub(r'\\newcommand{\\universityname}{.*}', 
                      r'\\newcommand{\\universityname}{' + escape_tex(info['university_name']) + '}', template)

    # Replace Position Link/Title in body
    # \href{...}{Tenure-track Assistant Professor}
    # We might need to just replace "Tenure-track Assistant Professor" with our position
    template = re.sub(r'\\href{.*?}{Tenure-track Assistant Professor}', 
                      r'\\textbf{' + escape_tex(info['position']) + '}', template)
    
    # Replace the "I am interested in the work of..." section
    interest_sentence = f"Within \\\\universityname, I am particularly interested in the work of Prof. {info['key_person']} and the related teams."
    
    # Let's try to replace the bolded interest sentence
    # We need to be careful with regex matching the target string which contains backslashes
    template = re.sub(r'\\textbf\{Within \\universityname, I am interested in the work of .*?\}', 
                      r'\\textbf{' + interest_sentence + '}', template)

    # Write new main.tex
    with open(os.path.join(target_dir, 'main.tex'), 'w', encoding='utf-8') as f:
        f.write(template)
    
    print(f"Generated Cover Letter for {info['university_name']}")

def generate_email(uni_dir, info):
    """
    Generates a draft email in Chinese.
    """
    email_path = os.path.join(uni_dir, 'email.md')
    
    content = f"""# Email Draft for {info['university_name']}

**Subject**: 咨询{info['university_name']}教职招聘 / Inquiry about Faculty Position - {info['university_name']}

尊敬的{info['department_name']}招聘委员会 / {info['key_person']}教授：

您好！

我是Junming，目前是[Current Position] at [Current Institution]。我主要从事**{info['research_focus']}**方向的研究，特别是Human-AI Collaboration和Trustworthy AI。

我关注到贵院正在招聘**{info['position']}**，我对{info['university_name']}在{info['research_focus']}领域的深厚积累（特别是{info['key_person']}教授团队的工作）非常仰慕。我的研究致力于设计以人为中心的AI系统，支持定性数据分析和软件工程等复杂任务，这与贵院的研究方向高度契合。

附件是我的简历(CV)和研究陈述(Research Statement)。我非常希望能有机会申请贵院的教职岗位，并期待能为{info['university_name']}的学科建设贡献力量。

期待您的回复。

祝好，

Junming
[Your Website]
"""
    with open(email_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generated Email Draft for {info['university_name']}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--universities', nargs='+', help='List of university directory names')
    args = parser.parse_args()

    base_dir = os.path.abspath('drafts')
    template_dir = os.path.abspath('materials/Cover_Letter_UIUC')

    universities = args.universities if args.universities else os.listdir(base_dir)

    for uni in universities:
        uni_dir = os.path.join(base_dir, uni)
        summary_path = os.path.join(uni_dir, 'summary.md')
        
        if os.path.exists(summary_path):
            print(f"Processing {uni}...")
            info = parse_summary(summary_path)
            generate_cover_letter(uni_dir, info, template_dir)
            generate_email(uni_dir, info)
        else:
            print(f"Skipping {uni}: summary.md not found.")

if __name__ == "__main__":
    main()
