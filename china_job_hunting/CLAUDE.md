# Faculty Application Assistant Agent - Project Guidelines

This project is an automated faculty job application manager for a candidate specializing in **AI & HCI (Human-Centered AI)** with an **Overseas** background. The goal is to manage application tracking, deadline monitoring, and email drafting for universities.

## 📂 Project Structure
- `china_job_list_{$crawl_update_date}.xlsx`: The MASTER database for job listings. Modify it only when you want to add new universities or update existing ones. **Columns**: 
  - `Deadline`: 提交申请的截止日期，年-月-日。 
  - `University&Department`： 申请的学校和部门，例如 `清华大学-人机交互中心`。
  - `Positions Link`： 岗位详情页面的链接。
  - `Position Title`: 岗位标题，例如 `人机交互中心-人机交互研究助理`。
  - `Position Research Direction (AI/HCI/HAI)`： 岗位研究方向，例如 `HCI`。
  - `Lab/Research Center/Professor Link`： 岗位所属的实验室或研究中心或相关知名学者 （要去学校对应的）的链接。
  - `OverseaPolicy`： 海外政策，例如 `某某海外学者计划`。
  - `Job Description`： 岗位描述，详细介绍岗位的要求，职责，**博导资格，博士生招生名额**，薪酬福利，人才待遇等。
  - `联系方式`： 联系学校的方式，例如 `邮箱`，`微信`，`电话`等。**着重关注微信联系方式**。
  - `联系方式的链接`： 保存学校联系方式的链接，例如 `https://www.tsinghua.edu.cn/info/1038/1039.htm`。
  - `是否计划申请`： 是否计划申请该岗位，这一列人工填写，AI不能修改这一列的内容。
- `china_job_list_apply_tracking.xlsx`: The tracking database for application status. Do not modify without backing up.  **Columns**:
  - `University&Department`： 申请的学校和部门，例如 `清华大学-人机交互中心`。
  - `Application Status`： 申请状态，例如 `已申请`，`已回复`，`已拒绝`等。
  - `Application Date`： 申请提交日期，年-月-日。
  - `Response Date`： 学校回复日期，年-月-日。
  - `Follow-up Date`： 申请跟进日期(收到反馈等)，年-月-日。
  - `Notes`： 其他备注，例如 `需要补充材料`，`需要调整申请`等。
- `materials/`: Folder containing My original PDFs (CV, Research Statement, Paper Reprints).
  - `materials/CV.pdf`: My CV.
  - `materials/Research_Statement.pdf`: My Research Statement.
  - `materials/publication**.pdf`: My three Paper Reprints.
  - `materials/Teaching_Statement.pdf`: My Teaching Statement.
  - `materials/Impact_Statement.pdf`: My Impact Statement.
  - `materials/Cover_Letter_UIUC/main.tex`: 样例学校的Cover Letter的latex文件。编译命令为 `xelatex main.tex`。
- `drafts/`: Folder for each university materials, including cover letter, email or wechat greeting message drafts.
  - `drafts/{University}/summary.md`: 目标学校的岗位总结，描述其岗位研究方向，依托的实验室/教授情况简介，职责，薪酬福利，人才待遇。并根据我的研究背景，列出我在申请该岗位时的优势与缺点，总结我在申请时应该强调的部分。
  - `drafts/{University}/Cover_Letter/`: 根据summary.md, 以及materials/Cover_Letter_UIUC/main.tex模板，生成目标学校的Cover Letter的latex文件。
  - `drafts/{University}/email.md`: 根据summary.md, 生成联系目标学校的email中文草稿。
- `src/`: Python scripts for scraping and automation.
- `backups/`: Auto-generated backups of the Excel sheet.

## 🛠 Common Commands

### Setup & Maintenance
- **install**: `pip install pandas openpyxl requests beautifulsoup4 tavily-python`
- **backup**: `cp china_job_list.xls backups/job_list_backup_$(date +%F).xls`

### Task Lisk (Run these specific tasks)
我每次启动程序都会要求你执行下列task之一或多个，你需要基于./workflow/{task_name}.md文件进行（如果有)：
- **plan**: 根据我提供的任务描述以及所有的资料，给我在./workflow目录下针对每一个task都单独写一个命令描述。
- **setup**: 检查并安装必要的库（网络搜素与爬取，excel操作等）。检查并修改excel数据格式，excel的列名需要修改为与我在Project Structure的描述一致。检查已有excel的各列已有的值是否符合要求，例如url列中的值不能为岗位名称。检查已有的行指向的岗位。是否有重复关系，如果有要标注出来。
- **fill**: 根据已有的最新的hina_job_list_{$crawl_update_date}.xlsx，通过网络爬取分析的方式，填充各列信息。
- **scan**: 目的是搜索新的可以投的学校岗位，搜索过程中记录在./scan文件夹目录下。
  - 搜索中国的985计划，以及HCI/AI较强的顶尖211，或别的中国大陆有学术声誉度（尤其是HCI/AI)的学校，保存为一个target_school_list的文件。
  - 搜索这些学校的CS/AI/HCI相关的学院，岗位及相关信息，按照china_job_list_{$crawl_update_date}.xlsx的格式，更新到target_school_list.xlsx文件。
  -  Focus on "HCI", "Overseas Talent" (海外优青), and "Faculty Recruitment" (诚聘教职)。创建新的hina_job_list_{$crawl_update_date}.xlsx，将结果保存到新的文件里。
- **draft-summary**: 根据china_job_list_{$crawl_update_date}.xlsx 和./scan/target_school_list.xlsx列的信息，在`drafts/{University}`目录下为每个学校生成summary.md。
- **draft-all**: 根据drafts/{University}/summary.md, 以及materials/Cover_Letter_UIUC/main.tex模板，生成目标学校的Cover Letter的latex文件, 以及email and wechat （如果有微信联系方式）草稿。


## 🧠 User Preferences & Context

### Target Profile
- **Research Area**: Artificial Intelligence & Human-Computer Interaction (AI + HCI), Human-Centered AI.
- **Target Roles**: Tenure-track Assistant Professor, Associate Professor, "Young Talent" programs (e.g., 海外优青, 百人计划). 必须有博导资格，博士生招生名额越多越好。
- **Region**: Mainly Mainland China.


## ⚠️ Coding & Execution Guidelines
1.  **Git Tracking**: 使用git进行版本管理.
2.  **Date Parsing**: Be robust with date formats found on Chinese university websites (e.g., "2026年3月1日" -> "2026-03-01").
3.  **Search Depth**: When searching for "Policies", look for explicit mentions of "Overseas" (海外) benefits.
4.  **Handling Libraries**: Use `pandas` for Excel manipulation. Ensure `xlrd` or `openpyxl` is compatible with the `.xls` or `.xlsx` format used.
5.  **Sensitive Schools Check**: Before executing `scan` or `draft` tasks for a specific university, ALWAYS check against `sensitive_schools_list.md`. If a school is on the "Defense Seven Sons" list or Entity List (e.g., Beihang, HIT, BIT, TJU, etc.), provide a visible WARNING to the user regarding visa (PP10043) and academic cooperation risks.