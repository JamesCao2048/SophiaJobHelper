% OUCletter.cls — Caramel variant
% Modified for Sophia's application pipeline: color scheme unified to CV_latest Caramel (#B87350)
%
% Changes vs original:
%   - slcolor: #882B21 → #B87350 (Caramel, matching CV_latest)
%   - scured alias added for backward compat with main.tex that uses \color{scured}
%   - Changed to a4paper

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{OUCletter}
\RequirePackage{graphicx}
\RequirePackage{epstopdf}
\RequirePackage{epsfig}
\RequirePackage{ifthen}
\RequirePackage{xcolor}

% --- COLOR: Caramel (matching CV_latest headingcolor) ---
\definecolor{slcolor}{HTML}{B87350}
\colorlet{scured}{slcolor}

\DeclareGraphicsExtensions {.png}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{letter}}
\ProcessOptions
\LoadClass[a4paper]{letter}

\newcommand{\subjectname}{Subject}
\newcommand{\@subject}{}
\newcommand{\subject}[1]{\renewcommand{\@subject}{\subjectname: #1}}

\newboolean{logofound}
\IfFileExists{jhu-icon.pdf}
    {\setboolean{logofound}{true}}
    {\setboolean{logofound}{false}}

\RequirePackage{lastpage}
\RequirePackage{fancyhdr}

\setlength{\textwidth}{7in}
\setlength{\textheight}{10in}
\setlength{\topskip}{0.0in}
\setlength{\footskip}{0.4in}
\setlength{\oddsidemargin}{-0.25in}
\setlength{\evensidemargin}{-0.25in}
\setlength{\topmargin}{-1.2in}

\DeclareFixedFont{\xcmrbn}{OT1}{cmr}{b}{n}{10}
\DeclareFixedFont{\xcmrmn}{OT1}{cmr}{m}{n}{10}
\DeclareFixedFont{\ixcmrmn}{OT1}{cmr}{m}{n}{9}

\newsavebox{\departmenthead}
\newsavebox{\departmentfoot}
\newsavebox{\emptyfoot}

\sbox{\departmenthead}{
    \parbox[b]{\textwidth}{
        \raggedleft
        \ifthenelse{\boolean{logofound}}
           {\includegraphics[height=0.4in]{jhu-icon.pdf}}
           {}
        \par
        \centering \large \textbf{\color{slcolor}Cover Letter}
    }
}

\savebox{\emptyfoot}[\textwidth][c]{\ixcmrmn
    \hspace*{\textwidth}
}

\renewcommand{\ps@firstpage}{
    \setlength{\headheight}{1.0in}
    \setlength{\headsep}{0.1in}
    \renewcommand{\@oddhead}{\usebox{\departmenthead}}
    \renewcommand{\@evenhead}{}
    \renewcommand{\@evenfoot}{}
}

\renewcommand{\ps@empty}{
    \setlength{\headheight}{0.5in}
    \setlength{\headsep}{0.2in}
    \renewcommand{\@oddhead}{}
    \renewcommand{\@oddfoot}{\hfil \thepage\ / \pageref{LastPage} \hfil}
    \renewcommand{\@evenhead}{}
    \renewcommand{\@evenfoot}{\hfil \thepage\ / \pageref{LastPage} \hfil}
}

\providecommand{\@evenhead}{}
\providecommand{\@oddhead}{}
\providecommand{\@evenfoot}{}
\providecommand{\@oddfoot}{}

\pagestyle{empty}

\renewcommand{\opening}[1]{\thispagestyle{firstpage}%
    \ifx\@empty\fromaddress
    \else
        {\raggedleft
            \begin{tabular}{l@{}}\ignorespaces
            \fromaddress \\ *[1\parskip]%
            \end{tabular}\par
        }%
        \vspace{-6\parskip}
     \fi
     \@date \vspace{2\parskip}\\
     {\raggedright \toname \\ \toaddress \par}%
     \vspace{1\parskip}%
     \ifthenelse{\equal{\@subject}{}}{}{\@subject\par}
     \vspace{1\parskip}%
     #1\par\nobreak
}

\renewcommand{\closing}[1]{%
  \par\vspace{\parskip}%
  \parbox{0.6\textwidth}{%
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
