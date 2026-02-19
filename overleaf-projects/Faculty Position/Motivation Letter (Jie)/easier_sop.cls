%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% SPDX-License-Identifier: BSD-3-Clause
% Copyright (c) 2020, Salman Ahmad Faris
% https://github.com/salfaris/EasyPS
% Copyright (c) 2024, Daize Dong
% https://github.com/DaizeDong/Easier-PS-and-SoP
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{easier_sop}[2024/10/21 Modified from EasyPS]
\LoadClass[11pt]{article} % Load the base article class with 12pt font size
% \pdfgentounicode=1  % Ensure generated PDF is ATS parsable
\RequirePackage[bottom]{footmisc}
\RequirePackage{lipsum}         % Generates placeholder text, remove if unnecessary
\RequirePackage{geometry}       % For layout and margin control
\RequirePackage{fancyhdr}       % For headers and footers
\RequirePackage{setspace}       % For controlling line spacing
\RequirePackage{titlesec}       % For section title formatting
\RequirePackage{lmodern}        % Load LM Roman (Latin Modern Roman)
\RequirePackage{xcolor}         % For custom colors
\RequirePackage{hyperref}       % For hyperlinking citations
\RequirePackage[sort,numbers]{natbib}
\usepackage{ragged2e}
\RequirePackage{fontspec}



% \setmainfont{Times New Roman}      % 正文
% \setsansfont{Arial}                % 无衬线
% \setmonofont{Courier New}   

% \setmainfont{TeX Gyre Termes}       % 类 Times
% \setsansfont{TeX Gyre Heros}        % 类 Helvetica
% \setmonofont{TeX Gyre Cursor}       % 类 Courier

% \setmainfont{Garamond}           % 主字体 Garamond
% \setsansfont{Garamond}           % 无衬线字体也用 Garamond（或可改为 Gill Sans 等搭配）
% \setmonofont{Courier New}        % 等宽字体依然保持 Courier 类



% \setmainfont{EB Garamond}        % 免费 Garamond 替代
% \setsansfont{Gill Sans}          % 常见搭配无衬线字体
% \setmonofont{Inconsolata}        % 等宽字体


% Font settings for XeLaTeX
\ifxetex
  % New Computer Modern font configuration
  \setmainfont{NewComputerModern10}[
    Ligatures=TeX,
    Numbers=OldStyle,
    BoldFont=NewComputerModern10-Bold,
    ItalicFont=NewComputerModern10-Italic,
    BoldItalicFont=NewComputerModern10-BoldItalic
  ]       % New Computer Modern Roman
  \setsansfont{NewComputerModernSans10}[
    Ligatures=TeX,
    Scale=MatchLowercase,
    BoldFont=NewComputerModernSans10-Bold,
    ItalicFont=NewComputerModernSans10-BookOblique,
    BoldItalicFont=NewComputerModernSans10-BoldOblique
  ]        % New Computer Modern Sans
  \setmonofont{NewComputerModernMono10}[
    Scale=MatchLowercase,
    BoldFont=NewComputerModernMono10-Bold,
    ItalicFont=NewComputerModernMono10-BookItalic,
    BoldItalicFont=NewComputerModernMono10-BoldOblique
  ]       % New Computer Modern Mono
  
  % Alternative font options (uncomment to use):
  % Previous TeX Gyre fonts:
  % \setmainfont{TeX Gyre Termes}[Ligatures=TeX,Numbers=OldStyle]
  % \setsansfont{TeX Gyre Heros}[Ligatures=TeX,Scale=MatchLowercase]
  % \setmonofont{TeX Gyre Cursor}[Scale=MatchLowercase]
  
  % System fonts:
  % \setmainfont{Times New Roman}[Ligatures=TeX]      % 正文
  % \setsansfont{Arial}[Scale=MatchLowercase]         % 无衬线
  % \setmonofont{Courier New}[Scale=MatchLowercase]   % 等宽
\fi





% BASIC INFO
\def\@StudentName{Jie Gao}
\newcommand*{\SetStudentName}[1]{\def\@StudentName{#1}}
\newcommand*{\GetStudentName}{\@StudentName}
\def\@UniversityName{University Name Here}
\newcommand*{\SetUniversityName}[1]{\def\@UniversityName{#1}}
\newcommand*{\GetUniversityName}{\@UniversityName}
\def\@UniversityAbbr{\@UniversityName}
\newcommand*{\SetUniversityAbbr}[1]{\def\@UniversityAbbr{#1}}
\newcommand*{\GetUniversityAbbr}{\@UniversityAbbr}

% CONTENTS INFO
\def\@BaseContentPath{main/content/base}
\newcommand*{\SetBaseContentPath}[1]{\def\@BaseContentPath{#1}}
\newcommand*{\GetBaseContentPath}{\@BaseContentPath}
\def\@UniContentPath{main/content/base}
\newcommand*{\SetUniContentPath}[1]{\def\@UniContentPath{#1}}
\newcommand*{\GetUniContentPath}{\@UniContentPath}

% LAYOUT SETTINGS
\geometry{a4paper, includeheadfoot, left=0.6in, right=0.6in, top=0.2in, bottom=0.5in}
\setlength{\footskip}{1pt} % 页脚基线到纸张底边的距离
\setlength{\parskip}{0em}     % Space between paragraphs
\linespread{1.06}               % Line spacing

% HEADER AND FOOTER SETTINGS
\pagestyle{fancy}               % Use fancy headers/footers
\fancyhf{}                      % Clear default header/footer
\fancyhead[L]{\@StudentName}    % Custom left header: Student Name
\fancyhead[R]{\@UniversityName} % Custom right header: University Name
\fancyfoot[C]{\thepage}         % Add a page number in the footer
\setlength{\headheight}{20pt}   % Adjust the height of the header
\setlength{\headsep}{5pt}      % Space between the header and content


\fancypagestyle{firstpageheader}{
  \fancyhf{} % 清空默认页眉页脚
  \fancyhead[L]{\Large \@StudentName} % 左侧：学生名字
  \fancyhead[R]{\Large \textsc{Motivation Letter}} % 右侧：Diversity Statement
  \fancyfoot[C]{\thepage} % 页脚居中显示页码
  \setlength{\headheight}{34pt}
  \setlength{\headsep}{2pt}
}



% CITATION SETTINGS
\renewcommand{\thefootnote}{\fnsymbol{footnote}}
\renewcommand{\refname}{\normalsize References\\[-30pt]}
% \AtEndDocument{\footnotetext{* denotes equal contribution.}}
\bibliographystyle{unsrtnat}
\hypersetup{
    colorlinks=true,
    citecolor=[HTML]{EC028D}, % Set citation color to pink
    linkcolor=blue,
    urlcolor=blue
}


\setlength{\parindent}{0em} % 段首缩进（可调整）
\setlength{\parskip}{0.5em}   % 段落间距（可调整）
\justifying                 
