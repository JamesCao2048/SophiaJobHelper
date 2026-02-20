
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{OUCletter}
\RequirePackage{graphicx}
\RequirePackage{epstopdf}
\RequirePackage{epsfig}
\RequirePackage{ifthen}
\RequirePackage{xcolor}
\definecolor{slcolor}{HTML}{882B21}
%\RequirePackage{fontspec}
\DeclareGraphicsExtensions {.png} %{.pdf}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{letter}}
\ProcessOptions
\LoadClass[letterpaper]{letter} % we always use letter paper

\newcommand{\subjectname}{Subject}
\newcommand{\@subject}{}
\newcommand{\subject}[1]{\renewcommand{\@subject}{\subjectname: #1}}

\newboolean{logofound}
\IfFileExists{jhu-icon.pdf}
    {\setboolean{logofound}{true}}
    {\setboolean{logofound}{false}}

\setlength{\textwidth}{6.875in}
\setlength{\textheight}{7.2in}
\setlength{\topskip}{0.1in}
\setlength{\footskip}{0.8in}
\setlength{\oddsidemargin}{-0.25in}
\setlength{\evensidemargin}{-0.25in}
\setlength{\topmargin}{-0.5in}

\DeclareFixedFont{\xcmrbn}{OT1}{cmr}{b}{n}{10}
\DeclareFixedFont{\xcmrmn}{OT1}{cmr}{m}{n}{10}
\DeclareFixedFont{\ixcmrmn}{OT1}{cmr}{m}{n}{9}

\newsavebox{\departmenthead}
\newsavebox{\departmentfoot}
\newsavebox{\emptyfoot}

\newcommand{\printdepartmenthead}{
    \begin{tabular*}{\textwidth}
                    {@{}l@{\extracolsep{\fill}}r@{}}           
    \parbox[c]{3.5in}
    {\raggedright
        \ifthenelse{\boolean{logofound}}
           {\includegraphics[height=0.7in]{jhu-icon.pdf}}
           {\parbox[c][1in][c]{2in}{\hfill} 
            \ClassWarning{OUCletter}{ouclogo.eps COULD NOT BE FOUND!}}
    } &
    \parbox[c]{3.0in}{\raggedleft\small\newaddress}
    \end{tabular*}
}

\savebox{\emptyfoot}[\textwidth][c]{\ixcmrmn
    \hspace*{\textwidth}
}

% header and footer should be placed only on the first page
\renewcommand{\ps@firstpage}{
    \setlength{\headheight}{1.375in}
    \setlength{\headsep}{1.0in}
    \renewcommand{\@oddhead}{\printdepartmenthead}
    \renewcommand{\@oddfoot}{\usebox{\departmentfoot}}
    \renewcommand{\@evenhead}{}
    \renewcommand{\@evenfoot}{}
}

\renewcommand{\ps@empty}{
    \setlength{\headheight}{0in}
    \setlength{\headsep}{0.2in}
    \renewcommand{\@oddhead}{}
    \renewcommand{\@oddfoot}{\usebox{\emptyfoot}}
    \renewcommand{\@evenhead}{}
    \renewcommand{\@evenfoot}{\usebox{\emptyfoot}}
}

\providecommand{\@evenhead}{}
\providecommand{\@oddhead}{}
\providecommand{\@evenfoot}{}
\providecommand{\@oddfoot}{}

\pagestyle{empty}

% we add the subject command to the opening
\renewcommand{\opening}[1]{\thispagestyle{firstpage}%
    \ifx\@empty\fromaddress
        %{\raggedleft\@date\par}%
    \else  % home address
        {\raggedleft
            \begin{tabular}{l@{}}\ignorespaces
            \fromaddress \\ *[1\parskip]%
            %\@date
            \end{tabular}\par
        }%
     \fi
     \vspace{-1\parskip}
     \@date \vspace{2\parskip}\\
     {\raggedright \toname \\ \toaddress \par}%
     \vspace{1\parskip}%
     \ifthenelse{\equal{\@subject}{}}{}{\@subject\par}
     \vspace{1\parskip}%
     #1\par\nobreak
}

% % we push closing to the left
% \renewcommand{\closing}[1]{\par\nobreak\vspace{\parskip}%
%     \stopbreaks
%     \noindent
%     \parbox{0.6\textwidth}{\raggedright
%     \ignorespaces #1\\[4\medskipamount]%
%     \ifx\@empty\fromsig
%         \fromname
%     \else \fromsig 
%     \fi\strut}%
%     \par
% }

\renewcommand{\closing}[1]{%
  \par\vspace{\parskip}%  这里不再用 \nobreak
  \stopbreaks
  \noindent
  \parbox{0.6\textwidth}{%
    \raggedright
    \ignorespaces #1\par
    \vspace{1\medskipamount}%
    \ifx\@empty\fromsig
      \fromname
    \else
      \fromsig
    \fi
    \strut
  }%
}