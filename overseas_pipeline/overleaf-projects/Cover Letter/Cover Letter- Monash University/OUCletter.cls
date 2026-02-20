
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{OUCletter}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{letter}}
\ProcessOptions
\LoadClass[letterpaper]{letter}

\RequirePackage{graphicx}
\RequirePackage{xcolor}
\RequirePackage{ifthen}
\RequirePackage{lastpage}
\RequirePackage{fancyhdr}
\RequirePackage{tikz}

% ---- Color ----
\definecolor{cvcopper}{RGB}{196, 140, 86}

% ---- Page geometry ----
% 1in default margin on each side; these offsets adjust from that baseline
\setlength{\textwidth}{6.5in}       % 1in left + 6.5in text + 1in right = 8.5in
\setlength{\oddsidemargin}{0in}     % 1in left margin
\setlength{\evensidemargin}{0in}
\setlength{\topmargin}{-0.5in}      % effective top margin ~0.5in
\setlength{\textheight}{7.5in}      % leave room for footer + bottom margin
\setlength{\topskip}{0in}
\setlength{\footskip}{0.2in}        % space from text bottom to footer

% ---- JHU logo check ----
\newboolean{logofound}
\IfFileExists{jhu-icon.pdf}
  {\setboolean{logofound}{true}}
  {\setboolean{logofound}{false}}

% ---- Header: JHU logo + Name + contact + copper rule (CV style) ----
\newsavebox{\cvheader}
\sbox{\cvheader}{%
  \parbox[b]{\textwidth}{%
    \ifthenelse{\boolean{logofound}}{%
      \raggedleft\includegraphics[height=0.4in]{jhu-icon.pdf}\par\vspace{4pt}%
    }{}%
    {\fontsize{28}{34}\selectfont\color{cvcopper}\bfseries Jie Gao}\\[6pt]
    {\small jgao77@jh.edu\enspace$\cdot$\enspace gaojie058.github.io\enspace$\cdot$\enspace +1\,(410)\,710-0555}\\[2pt]
    {\small\textbf{Malone Postdoctoral Fellow, Johns Hopkins University}}\\[1pt]
    {\small Department of Computer Science}\\[1pt]
    {\small Malone Center for Engineering in Healthcare \& Center for Language and Speech Processing}\\[1pt]
    {\small Malone Hall, 3400 N Charles St, Baltimore, MD 21218, USA}\\[6pt]
    {\color{cvcopper}\rule{\textwidth}{0.8pt}}%
  }%
}

% ---- First page style ----
\renewcommand{\ps@firstpage}{%
  \setlength{\headheight}{2.0in}
  \setlength{\headsep}{0.15in}
  \renewcommand{\@oddhead}{\usebox{\cvheader}}
  \renewcommand{\@oddfoot}{\hfil{\small\thepage\,/\,\pageref{LastPage}}\hfil}
  \renewcommand{\@evenhead}{}
  \renewcommand{\@evenfoot}{}
}

% ---- Subsequent pages style ----
\renewcommand{\ps@empty}{%
  \setlength{\headheight}{0.3in}
  \setlength{\headsep}{0.2in}
  \renewcommand{\@oddhead}{\hfil{\small\color{cvcopper}Jie Gao\enspace$\cdot$\enspace Cover Letter}\hfil}
  \renewcommand{\@oddfoot}{\hfil{\small\thepage\,/\,\pageref{LastPage}}\hfil}
  \renewcommand{\@evenhead}{}
  \renewcommand{\@evenfoot}{\hfil{\small\thepage\,/\,\pageref{LastPage}}\hfil}
}

\providecommand{\@evenhead}{}
\providecommand{\@oddhead}{}
\providecommand{\@evenfoot}{}
\providecommand{\@oddfoot}{}

\pagestyle{empty}

% ---- Subject command ----
\newcommand{\subjectname}{Subject}
\newcommand{\@subject}{}
\newcommand{\subject}[1]{\renewcommand{\@subject}{\subjectname: #1}}

% ---- Opening ----
\renewcommand{\opening}[1]{\thispagestyle{firstpage}%
  \vspace*{0.1in}%
  \@date\par
  \vspace{0.15in}%
  {\raggedright \toname \\ \toaddress \par}%
  \vspace{0.15in}%
  \ifthenelse{\equal{\@subject}{}}{}{\@subject\par\vspace{0.1in}}%
  #1\par\nobreak
}

% ---- Closing ----
\renewcommand{\closing}[1]{%
  \par\vspace{0.15in}%
  \parbox{0.55\textwidth}{%
    \raggedright
    \ignorespaces #1\par
    \ifx\@empty\fromsig
      \fromname
    \else
      \fromsig
    \fi
    \strut
  }%
}
