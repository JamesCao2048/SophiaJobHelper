
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
        % \vspace{0.05in}
        \centering \large \textbf{Cover Letter}
    }
}

\savebox{\emptyfoot}[\textwidth][c]{\ixcmrmn
    \hspace*{\textwidth}
}

% header and footer should be placed only on the first page
\renewcommand{\ps@firstpage}{
    \setlength{\headheight}{1.0in}
    \setlength{\headsep}{0.1in}
    \renewcommand{\@oddhead}{\usebox{\departmenthead}}
    % \renewcommand{\@oddfoot}{\hfil \thepage\ / \pageref{LastPage} \hfil}
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
        \vspace{-6\parskip}
     \fi
     %\vspace{-6\parskip}
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
    \vspace{4\medskipamount}%
    \ifx\@empty\fromsig
      \fromname
    \else
      \fromsig
    \fi
    \strut
  }%
}