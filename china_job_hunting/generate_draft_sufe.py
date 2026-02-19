import os
import shutil
import re

target = {
    "id": "Shanghai_University_of_Finance_and_Economics",
    "name": "Shanghai University of Finance and Economics",
    "dept": "School of Computing and Artificial Intelligence",
    "focus": "AI for Finance and Economics",
    "professors": ["Dean Lu Pinyan", "Professor Shaokui Wei"],
    "email_target": "Dean Lu Pinyan / Faculty Search Committee"
}

source_dir = "materials/Cover_Letter_UIUC"
template_path = os.path.join(source_dir, "main.tex")

with open(template_path, 'r') as f:
    template_content = f.read()

uni_dir = os.path.join("drafts", target["id"])
cv_dir = os.path.join(uni_dir, "Cover_Letter")

if not os.path.exists(cv_dir):
    os.makedirs(cv_dir)

# Copy assets
for item in os.listdir(source_dir):
    s = os.path.join(source_dir, item)
    d = os.path.join(cv_dir, item)
    if os.path.isfile(s) and not item.startswith("main."):
        shutil.copy2(s, d)
    elif os.path.isdir(s) and item == "content":
        if os.path.exists(d):
            shutil.rmtree(d)
        shutil.copytree(s, d)

# Modify Template
content = template_content

# 1. Replace University Name
content = re.sub(r'\\newcommand\{\\universityname\}\{.*?\}', f'\\\\newcommand{{\\\\universityname}}{{{target["name"]}}}', content)

# 2. Replace Department Name
content = re.sub(r'\\newcommand\{\\departmentname\}\{.*?\}', f'\\\\newcommand{{\\\\departmentname}}{{{target["dept"]}}}', content)

# 3. Replace Focus
content = re.sub(r'\\newcommand\{\\searchingfocus\}\{.*?\}', f'\\\\newcommand{{\\\\searchingfocus}}{{\\\\textbf{{{target["focus"]}}}}}', content)

# 4. Replace Professors paragraph
prof_list = ", ".join([f"\\textbf{{{p}}}" for p in target["professors"]])
pattern = r'\\textbf\{Within \\universityname, I am interested in the work of .*?\}'
replacement = f"\\\\textbf{{Within \\\\universityname, I am particularly interested in the work of {prof_list}, and I hope to explore collaboration opportunities with them.}}"
content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Fix possible garbage from previous manual edits or template issues
content = re.sub(r'\}\{Gunter .*? with them\.\}', '', content, flags=re.DOTALL)
content = content.replace('Earth Science}}}', 'Earth Science}}') # Just in case

# Write main.tex
with open(os.path.join(cv_dir, "main.tex"), 'w') as f:
    f.write(content)
print(f"Generated main.tex for {target['name']}")

# Generate Email Draft
email_content = f"""# Email Draft for {target['name']}

**Subject**: Inquiry regarding Faculty Positions in School of Computing and AI - Jie Gao

**To**: {target['email_target']} (Dean Lu Pinyan)
**Cc**: {', '.join(target['professors'])}

Dear Dean Lu and Members of the Faculty Search Committee,

I am writing to express my strong interest in the **Tenure-track Assistant Professor** positions at the newly established **{target['dept']}** at **{target['name']}**.

I am currently a Malone Postdoctoral Fellow at **Johns Hopkins University**, specializing in **Human-Centered AI** and **Human-Computer Interaction (HCI)**. I am very excited to learn about the establishment of the new school and its vision of "AI empowering Finance/Economics".

My research focuses on designing trustworthy Human-AI Collaboration systems for complex data analysis. I believe my work aligns well with SUFE's strengths in **Theoretical Computer Science** and **AI Applications**:
1.  **Trustworthy AI**: I build systems that enhance human trust and agency (aligning with Prof. Shaokui Wei's direction).
2.  **Mechanism Design for Collaboration**: My work on "CollabCoder" can be viewed as designing mechanisms for effective human-AI interaction, which resonates with the school's strong background in Algorithmic Game Theory.
3.  **AI for Decision Making**: My tools support high-stakes decision-making (e.g., in healthcare), which translates well to financial and economic decision-making contexts.

I have published consistently in top-tier venues such as **CHI** and **TOCHI**. My open-source tools have been widely adopted, demonstrating practical impact.

I have attached my CV, Research Statement, and Representative Papers for your review. I would be honored to have the opportunity to contribute to the growth of the new school.

Thank you for your time and consideration.

Best regards,

Jie Gao
Malone Postdoctoral Fellow
Johns Hopkins University
Website: https://gaojie058.github.io/
"""

with open(os.path.join(uni_dir, "email.md"), 'w') as f:
    f.write(email_content)
print(f"Generated email.md for {target['name']}")

