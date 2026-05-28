%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Sparkle v 1.1
%
% Dr. John F. N. Salik Eng.
%
% This is a template that defines a document class based on the "book" archetype.  It is intended for
% rapidly producing documents for publication.  It is not intended for distribution and is the private
% intellectual property of the author.  Any use or modification should be done with the explicit 
% permission of the author.
%
% 2020-11-20 - Added nocopyright option to suppress the copyright statement.
% 2021-01-06 - Added starred chapter support (\chapter*); headings appear but are not numbered or listed in the TOC.
% 2026-05-27 - Added \documentlogo and \smalldocumentlogo preamble commands with a three-level fallback chain.
% 2026-05-28 - Exposed logo heights as \SparkleLogoHeight, \SparkleSmallLogoHeight, \SparkleSmallLogoStarHeight length registers.
% 2026-05-28 - Fixed \setlength overrides: use \the to expand length registers to pt strings before passing to graphicx.
% 2026-05-28 - Removed width cap from SmallDocumentLogo; chapter heading logo is now sized by height only.
% 2026-05-28 - Added color hooks: \SparkleRuleColor and \SparkleBoxColor (default black).
% 2026-05-28 - Added heading color hooks: \SparkleChapterNumberColor, \SparkleChapterTitleColor, \SparkleSectionColor.
% 2026-05-28 - Extended all color hooks with optional color-model argument (RGB, rgb, cmyk).
% 2026-05-28 - Added \SparkleCaptionColor hook for figure and table captions.
% 2026-05-28 - Added \SparkleTOCChapterColor hook for TOC chapter entry color and page number.
% 2026-05-28 - TOC is now always single-spaced even when doublespace option is active.
% 2026-05-28 - Added \SparkleCopyrightLogoHeight length for copyright page logo sizing.
% 2026-05-28 - Added nomoddate class option to suppress modification date on copyright page.
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% ============================================================
% CLASS IDENTITY
% ============================================================
\def\SparkleClassVersion{1.1}
\typeout{***********************************}
\typeout{Sparkle Class v\SparkleClassVersion}
\typeout{John F. N. Salik Eng.}
\typeout{November 23, 2013}
\typeout{***********************************}

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{Sparkle}[2013/09/23 Sparkle Document Class, John F. N. Salik Eng.]

% ============================================================
% CLASS OPTIONS
% ============================================================
\DeclareOption{oneside}{\onesidetrue}\newif\ifoneside
\DeclareOption{twoside}{\twosidetrue}\newif\iftwoside
\DeclareOption{doublespace}{\doublespacetrue}\newif\ifdoublespace
\DeclareOption{nocopyright}{\nocopyrighttrue}\newif\ifnocopyright
\DeclareOption{nomoddate}{\nomoddatetrue}\newif\ifnomoddate
\ProcessOptions

% ============================================================
% REQUIRED PACKAGES (loaded before \LoadClass so they are
% available during class option processing)
% ============================================================
\RequirePackage{graphicx}   % \includegraphics for logos and margin icons
\RequirePackage{ifpdf}      % detect PDF output mode for \pdfinfo block
\RequirePackage{setspace}   % \doublespacing for the doublespace option
\RequirePackage{xcolor}     % color support for rules, boxes, and annotations

% ============================================================
% DOCUMENT METADATA COMMANDS
% Set in the document preamble; all have built-in defaults.
% ============================================================
\def\documenttitle#1{\def\thedocumenttitle{#1}}
\def\authorname#1{\def\theauthorname{#1}}
\def\authoremail#1{\def\theauthoremail{#1}}
\def\authorphone#1{\def\theauthorphone{#1}}
\def\authortitle#1{\def\theauthortitle{#1}}
\def\authoraddress#1{\def\theauthoraddress{#1}}
\def\copyrightyear#1{\def\thecopyrightyear{#1}}
\def\documentID#1{\def\thedocumentID{#1}}   % omitted everywhere when not set
% \editor and \reviewer are optional.  When defined they add rows to the
% contact-information table on the copyright page.  Define them like any
% other metadata command:
%   \editor{Dr. A. Smith}
%   \reviewer{Dr. B. Jones}
% They have no built-in defaults; omitting them leaves those rows out entirely.

% Built-in defaults applied only when the author has not provided a value.
\ifx\theauthorname\undefined\def\theauthorname{John F. N. Salik,}\fi
\ifx\theauthoremail\undefined\def\theauthoremail{john\_salik@hotmail.com}\fi
\ifx\thedocumenttitle\undefined\def\thedocumenttitle{Research Documentation}\fi
\ifx\thecopyrightyear\undefined\def\thecopyrightyear{\the\year}\fi
\ifx\theauthoraddress\undefined\def\theauthoraddress{%
	\textbf{Department of Electrical \& Computer Engineering}\\%
	1515 St. Catherine St. West, EV16.185\\Montreal, Quebec\\H3G 2W1}\fi

% Logo selection flags — set by \documentlogo / \smalldocumentlogo in the preamble.
\newif\ifdocumentlogoset\documentlogosetfalse
\newif\ifsmalldocumentlogoset\smalldocumentlogosetfalse
\def\documentlogo#1{\def\thedocumentlogo{#1}\documentlogosettrue}
\def\smalldocumentlogo#1{\def\thesmalldocumentlogo{#1}\smalldocumentlogosettrue}

% ============================================================
% COLOR HOOKS
% Set in the document preamble to override colors.  Each command accepts an
% optional color-model argument so RGB, rgb, and cmyk specs work directly:
%
%   \SparkleChapterTitleColor{blue!70}           % xcolor name / mix
%   \SparkleChapterTitleColor[RGB]{0,70,127}     % 0-255 per channel
%   \SparkleChapterTitleColor[rgb]{0,0.27,0.5}   % 0.0-1.0 per channel
%   \SparkleChapterTitleColor[cmyk]{1,0.45,0,0.5}
%   \SparkleTOCChapterColor[RGB]{0,70,127}       % chapter titles + page numbers in TOC
%
% All colors default to black so documents compile unchanged without setting them.
% ============================================================
\newcommand{\SparkleRuleColor}[2][]{\def\theSparkleRuleColorModel{#1}\def\theSparkleRuleColor{#2}}
\newcommand{\SparkleBoxColor}[2][]{\def\theSparkleBoxColorModel{#1}\def\theSparkleBoxColor{#2}}
\newcommand{\SparkleChapterNumberColor}[2][]{\def\theSparkleChapterNumberColorModel{#1}\def\theSparkleChapterNumberColor{#2}}
\newcommand{\SparkleChapterTitleColor}[2][]{\def\theSparkleChapterTitleColorModel{#1}\def\theSparkleChapterTitleColor{#2}}
\newcommand{\SparkleSectionColor}[2][]{\def\theSparkleSectionColorModel{#1}\def\theSparkleSectionColor{#2}}
\newcommand{\SparkleCaptionColor}[2][]{\def\theSparkleCaptionColorModel{#1}\def\theSparkleCaptionColor{#2}}
\newcommand{\SparkleTOCChapterColor}[2][]{\def\theSparkleTOCChapterColorModel{#1}\def\theSparkleTOCChapterColor{#2}}
% Defaults: black with no model string.
\def\theSparkleRuleColorModel{}          \def\theSparkleRuleColor{black}
\def\theSparkleBoxColorModel{}           \def\theSparkleBoxColor{black}
\def\theSparkleChapterNumberColorModel{} \def\theSparkleChapterNumberColor{black}
\def\theSparkleChapterTitleColorModel{}  \def\theSparkleChapterTitleColor{black}
\def\theSparkleSectionColorModel{}       \def\theSparkleSectionColor{black}
\def\theSparkleCaptionColorModel{}       \def\theSparkleCaptionColor{black}
\def\theSparkleTOCChapterColorModel{}    \def\theSparkleTOCChapterColor{black}

% Internal dispatcher: emits \color[model]{spec} or \color{spec} when no model.
\newcommand{\SparkleApplyColor}[2]{%
  \edef\@sc@model{#1}%
  \ifx\@sc@model\@empty\color{#2}\else\color[\@sc@model]{#2}\fi}

% Internal helper: draw a full-width colored rule.
\newcommand{\SparkleHRule}{{\SparkleApplyColor{\theSparkleRuleColorModel}{\theSparkleRuleColor}\hrule}}

% ============================================================
% EDITING MARKERS
% Visual block markers used during draft review.
% ============================================================
\newcommand{\STOP}{\vspace{2em}\huge\SparkleHRule\SparkleHRule\SparkleHRule\begin{center} $\bigodot$ S T O P $\bigodot$ \end{center}\SparkleHRule\SparkleHRule\SparkleHRule\normalsize\vspace{2em}}
\newcommand{\EDITINGSTART}{\vspace{2em}\SparkleHRule\begin{center}$\Downarrow\ \Downarrow\ \Downarrow$\hspace{3em} E D I T I N G \hspace{2em} S T A R T \hspace{3em}$\Downarrow\ \Downarrow\ \Downarrow$ \end{center}\SparkleHRule\vspace{2em}}
\newcommand{\EDITINGEND}{\vspace{2em}\SparkleHRule\begin{center}$\Uparrow\ \Uparrow\ \Uparrow$\hspace{3em} E D I T I N G \hspace{2em} E N D\hspace{3em}$\Uparrow\ \Uparrow\ \Uparrow$ \end{center}\SparkleHRule\vspace{2em}}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

	\typeout{********************************}
	\typeout{**          SPARKLE           **}
	\typeout{********************************}

	% Load the book class with openright so numbered chapters always start on a recto page.
	\ifoneside
		\LoadClass[9pt,openright,oneside]{book}
		\typeout{* Open manual on the right.}
		\typeout{* 9pt font size.}
		\typeout{* One-sided printing.}
	\else
		\LoadClass[9pt,openright,twoside]{book}
		\typeout{* Open manual on the right.}
		\typeout{* 9pt font size.}
		\typeout{* Two-sided printing.}
	\fi

	% ============================================================
	% PACKAGES (loaded after \LoadClass)
	% ============================================================
	% tocloft must be loaded BEFORE titlesec.  titlesec patches \@starttoc in a
	% way that breaks tocloft's \l@chapter redefinition if tocloft loads second,
	% causing \cftchappagefont (TOC page-number color) to be silently ignored.
	\usepackage{tocloft}     % TOC entry formatting for \SparkleTOCChapterColor hook
	\usepackage{titlesec}    % section heading formatting for color hooks
	\usepackage{fancyhdr}    % custom headers and footers
	\usepackage{datetime}    % \today with long date format; \currenttime on copyright page
	\usepackage{cmbright}    % CM Bright sans-serif body font
	\usepackage[T1]{fontenc} % T1 encoding for correct hyphenation and PDF copying
	\usepackage{avant}       % Avant Garde sans-serif for headings
	\renewcommand*\familydefault{\sfdefault}  % use sans-serif as the document default
	\usepackage[lmargin=1.5in,rmargin=1.5in,tmargin=1in,bmargin=1in]{geometry}
	\usepackage{makeidx}     % back-matter index
	\makeindex

	\newlength{\PageColumnWidth}
	\setlength{\PageColumnWidth}{0.85\columnwidth}
	\addtolength{\PageColumnWidth}{-1em}

	% Logo height variables.  Override with \setlength to adjust sizing.
	\newlength{\SparkleLogoHeight}
	\setlength{\SparkleLogoHeight}{1in}
	\newlength{\SparkleSmallLogoHeight}
	\setlength{\SparkleSmallLogoHeight}{0.75in}
	\newlength{\SparkleSmallLogoStarHeight}
	\setlength{\SparkleSmallLogoStarHeight}{0.5in}
	\newlength{\SparkleCopyrightLogoHeight}
	\setlength{\SparkleCopyrightLogoHeight}{0.5in}

	% If the book class did not define \abstract, provide a minimal version.
	\ifx\abstract\undefined
		\newenvironment{abstract}[1]{\chapter{\thedocumenttitle}}{}
	\else
		\renewenvironment{abstract}{\section{Abstract}}{}
	\fi
	
	% ============================================================
	% LOGO COMMANDS
	% ============================================================
	% Main logo fallback chain: \documentlogo{file} > Logo.pdf > logos/Concordia_Logo.pdf
	\newcommand{\DocumentLogo}[1]{%
		\ifdocumentlogoset
			\includegraphics[#1]{\thedocumentlogo}%
		\else
			\IfFileExists{Logo.pdf}%
				{\includegraphics[#1]{Logo.pdf}}%
				{\includegraphics[#1]{logos/Concordia_Logo.pdf}}%
		\fi}
	% Small logo: \smalldocumentlogo{file} > main logo > logos/Small_Concordia_Logo.pdf
	% #1 = height register (\SparkleSmallLogoHeight or \SparkleSmallLogoStarHeight)
	% \the expands the register to a pt string so graphicx keyval handles it unambiguously.
	\newcommand{\SmallDocumentLogo}[1]{%
		\ifsmalldocumentlogoset
			\includegraphics[height=\the#1]{\thesmalldocumentlogo}%
		\else\ifdocumentlogoset
			\includegraphics[height=\the#1]{\thedocumentlogo}%
		\else
			\includegraphics[height=\the#1]{logos/Small_Concordia_Logo.pdf}%
		\fi\fi}



	% ============================================================
	% TYPOGRAPHY
	% ============================================================
	\setlength{\parskip}{0.75\baselineskip}  % open up space between paragraphs

	\newcommand{\captionfonts}{\scriptsize}  % figures and tables use a smaller caption font
	\makeatletter
	\long\def\@makecaption#1#2{%
  		\vskip\abovecaptionskip
  		\sbox\@tempboxa{{\SparkleApplyColor{\theSparkleCaptionColorModel}{\theSparkleCaptionColor}\captionfonts #1: #2}}%
  		\ifdim \wd\@tempboxa >\hsize
    		{\SparkleApplyColor{\theSparkleCaptionColorModel}{\theSparkleCaptionColor}\captionfonts #1: #2\par}
  		\else
    		\hbox to\hsize{\hfil\box\@tempboxa\hfil}%
  		\fi
  		\vskip\belowcaptionskip}

	% Four levels of numbered headings (chapter, section, subsection, subsubsection),
	% all appearing in the table of contents.
	\setcounter{secnumdepth}{4}
	\setcounter{tocdepth}{4}

	% Sparkle generates the title page via \preamble inside \AtBeginDocument,
	% so the standard \maketitle is suppressed.
	\renewcommand{\maketitle}{}
	\newcommand{\AdjustForPublicationMark}{}  % reserved hook; no-op by default

	% ============================================================
	% FRONT MATTER PAGES
	% ============================================================
	\newcommand{\contactinformation}{\small
			\begin{tabular}{r|p{0.75\textwidth}}
				\textit{Title} & \textbf{\thedocumenttitle}\\
				\textit{Date} & \usdate\@date\longdate\\
				\textit{Author} & \theauthorname\ (\theauthoremail)\\
				\ifx\editor\undefined\else\textit{Editor} & \editor\\\fi
				\ifx\reviewer\undefined\else\textit{Reviewer} & \reviewer\\\fi
				\ifx\thedocumentID\undefined\else\textit{Identification} & \thedocumentID\\\fi
				\textit{Template} & Sparkle Version \SparkleClassVersion\ for \textrm{\LaTeXe}
			\end{tabular}
		}
	\newcommand{\copyrightnotice}{
		\clearpage\pagestyle{empty}
		\begin{center}
			% nomoddate option: suppress the "last modified" timestamp.
			\ifnomoddate\else
				\settimeformat{ampmtime}
				This document was last modified on\\ \today \hspace{0.5ex} at \currenttime.\\
			\fi
			\vfill
			{\SparkleApplyColor{\theSparkleBoxColorModel}{\theSparkleBoxColor}\framebox[\textwidth]{\contactinformation}}\\
			\vfill
			\DocumentLogo{height=\the\SparkleCopyrightLogoHeight}\\\vspace{0.125in}
			\ifnocopyright\else
				\textbf{\copyright \thecopyrightyear. All rights reserved by \theauthorname.} \\
				\noindent This document may not be cited, reproduced, or distributed without explicit written permission from the author.\\
			\fi		
		\end{center}
		\clearpage
		}
	\newcommand{\preamble}{
		\pagestyle{empty}
		\begin{raggedleft}
			\DocumentLogo{height=\the\SparkleLogoHeight}
		\end{raggedleft}
		\vfill
		\begin{raggedleft}
			\SparkleHRule\vspace{1in}\Huge\textbf{\thedocumenttitle}\\\normalsize
			\ifdefined\theauthorname
				\textbf{\theauthorname}\\\vspace{0.25in}
			\fi
			\ifx\thedocumentID\undefined\else\thedocumentID\fi\vspace{1in}\SparkleHRule
		\end{raggedleft}
		\vfill
		\begin{raggedleft}
			\theauthoraddress\\
		\end{raggedleft}
		\copyrightnotice
		}

	% ============================================================
	% HEADERS, FOOTERS & CHAPTER HEADINGS
	% Applied by \basicformatting, which is called inside \AtBeginDocument
	% after the front matter so that chapter pages start clean.
	% ============================================================
	% basicformatting is called once, after the front matter, so that chapter
	% opening pages (which use \thispagestyle{empty}) are not affected by
	% the fancy header before the body begins.
	%
	% Header layout (twoside):
	%   Even (verso) pages  →  page number | chapter title          (left-aligned)
	%   Odd  (recto) pages  →  section title | page number          (right-aligned)
	% Footer layout:
	%   Even pages  →  author name                                   (left-aligned)
	%   Odd  pages  →  document title                                (right-aligned)
	\newcommand{\basicformatting}{
		\pagestyle{fancy}
		\fancyhf{}
		% Even (left) pages: page number then chapter title on the left.
		\fancyhead[LE]{\textbf{\thepage}\hspace{1em}\protect\parbox[t]{0.80\textwidth}{\leftmark}}
		% Odd (right) pages: section title then page number on the right.
		\fancyhead[RO]{\rightmark\hspace{1em}\textbf{\thepage}}
		\fancyfoot[RO]{\textit{\thedocumenttitle}}
		\fancyfoot[LE]{\textit{\theauthorname}}
		\renewcommand{\headrulewidth}{1pt}
		\renewcommand{\footrulewidth}{1pt}
		\renewcommand{\headrule}{{\SparkleApplyColor{\theSparkleRuleColorModel}{\theSparkleRuleColor}\hrule width\headwidth height\headrulewidth}}
		\renewcommand{\footrule}{{\SparkleApplyColor{\theSparkleRuleColorModel}{\theSparkleRuleColor}\hrule width\headwidth height\footrulewidth}}
		\renewcommand{\chaptermark}[1]{\markboth{\protect\parbox[t]{0.80\textwidth}{\MakeUppercase{##1}\vspace{3pt}}}{}}
		% Numbered chapter heading: rule / chapter label + logo / title / rule
		\renewcommand{\@makechapterhead}[1]{%
			\vspace*{10\p@}%
				{\parindent \z@ \raggedright \normalfont
				\SparkleHRule                                 % horizontal line
				\vspace{5pt}%                                 % add vertical space
				\ifnum \c@secnumdepth >\m@ne
	     			{\SparkleApplyColor{\theSparkleChapterNumberColorModel}{\theSparkleChapterNumberColor}\huge\scshape \@chapapp\space \thechapter} \hfill\SmallDocumentLogo{\SparkleSmallLogoHeight}% Chapter number
	      			\par\nobreak
	      			\vskip 20\p@
				\fi
				\interlinepenalty\@M
				{\SparkleApplyColor{\theSparkleChapterTitleColorModel}{\theSparkleChapterTitleColor}\Huge \scshape \textbf{##1}}\par               % chapter title
				\vspace{2ex}%                                 % add vertical space
				\SparkleHRule                                 % horizontal rule
				\nobreak
				\vskip 40\p@
				\thispagestyle{empty}
				}
			\ifdoublespace
				\doublespacing
			\fi			
			}
		% Starred chapter heading (\chapter*): logo only, no chapter number or TOC entry.
		\renewcommand{\@makeschapterhead}[1]{%
			\vspace*{10\p@}%
				{\parindent \z@ \raggedright \normalfont
				\vspace{5pt}%                                 % add vertical space
				\ifnum \c@secnumdepth >\m@ne
	     			\huge\scshape\hfill\SmallDocumentLogo{\SparkleSmallLogoStarHeight}% logo (no chapter number)
	      			\par\nobreak
	      			\vskip 20\p@
				\fi
				\interlinepenalty\@M
				{\SparkleApplyColor{\theSparkleChapterTitleColorModel}{\theSparkleChapterTitleColor}\Huge \scshape \textbf{##1}}\par               % chapter title
				% No closing rule for starred chapters (unnumbered front/back matter).
				\nobreak
				\vskip 40\p@
				\thispagestyle{empty}
				}
			\ifdoublespace
				\doublespacing
			\fi
			}
		}
	\makeatother

	% Apply section heading colors via titlesec.  Each format replicates the
	% book class defaults for size/style but wraps the title in \color so that
	% \SparkleSectionColor takes effect without other visual changes.
	\titleformat{\section}
		{\SparkleApplyColor{\theSparkleSectionColorModel}{\theSparkleSectionColor}\normalfont\Large\bfseries}
		{\thesection}{1em}{}
	\titleformat{\subsection}
		{\SparkleApplyColor{\theSparkleSectionColorModel}{\theSparkleSectionColor}\normalfont\large\bfseries}
		{\thesubsection}{1em}{}
	\titleformat{\subsubsection}
		{\SparkleApplyColor{\theSparkleSectionColorModel}{\theSparkleSectionColor}\normalfont\normalsize\bfseries}
		{\thesubsubsection}{1em}{}

	% Apply TOC chapter entry color via tocloft.
	\renewcommand{\cftchapfont}{\SparkleApplyColor{\theSparkleTOCChapterColorModel}{\theSparkleTOCChapterColor}\bfseries}
	\renewcommand{\cftchappagefont}{\SparkleApplyColor{\theSparkleTOCChapterColorModel}{\theSparkleTOCChapterColor}\bfseries}

	% Bias LaTeX's float placement so figures stay near their text rather than
	% collecting on a dedicated float page.
	\renewcommand{\topfraction}{0.85}
	\renewcommand{\textfraction}{0.1}
	\renewcommand{\floatpagefraction}{0.75}

	% ============================================================
	% MARGIN ANNOTATIONS
	% Place an icon and a short note in the outer margin.
	% Icon files live in the icons/ subdirectory.
	% ============================================================
	\marginparwidth 1in
	\marginparsep 0.125in
	\newcommand{\WarningMessage}[1]{\marginpar{
		\begin{center}
			\includegraphics[width=0.75\marginparwidth]{icons/Warning_Logo.pdf}
		\end{center}\vspace{-2ex}\SparkleHRule\vspace{1ex}\tiny#1\vspace{1ex}\SparkleHRule}}
	\newcommand{\StopMessage}[1]{\marginpar{
		\begin{center}
			\includegraphics[width=0.7\marginparwidth]{icons/Stop_Logo.pdf}
		\end{center}\vspace{-1ex}\SparkleHRule\vspace{1ex}\tiny#1\vspace{1ex}\SparkleHRule}}
	\newcommand{\InformationMessage}[1]{\marginpar{
		\begin{center}
			\includegraphics[width=0.7\marginparwidth]{icons/Information_Logo.pdf}
		\end{center}\vspace{-1ex}\SparkleHRule\vspace{1ex}\tiny#1\vspace{1ex}\SparkleHRule}}

	% ============================================================
	% DOCUMENT LIFECYCLE HOOKS
	% ============================================================
	\AtBeginDocument{
		\ifpdf
			\pdfinfo{
   				/Author (\theauthorname)
   				/Title  (\thedocumenttitle\ifx\thedocumentID\undefined\else\ (\thedocumentID)\fi)
				/Creator (Sparkle Document Class v\SparkleClassVersion\ for XeLaTeX)
   				/Producer (Dr. John F. N. Salik Eng.)
   				/CreationDate (D:\pdfdate)
				}
		\fi
		% Sequence: roman-numbered front matter, title page, copyright page,
		% headers/chapter styles, table of contents, then arabic-numbered body.
		\frontmatter\preamble\basicformatting{\singlespacing\tableofcontents}\mainmatter
		}

	% Back matter: switch to unnumbered pages, then emit the index that was
	% built by makeindex from all \index{} calls in the body.
	\AtEndDocument{%
		\newpage
		\backmatter
		\printindex}

% ============================================================
% UNIT MACROS
% Shorthand commands for common scientific and engineering units.
% Add new entries here following the same \ensuremath pattern.
% ============================================================
\newcommand{\g}{\ensuremath{\textrm{\,g}\:}}
\newcommand{\mg}{\ensuremath{\textrm{\,mg}\:}}
\newcommand{\mL}{\ensuremath{\textrm{\,mL}\:}}
\newcommand{\gmL}{\ensuremath{\,^\textrm{g}/_\textrm{mL}\:}}
\newcommand{\gmol}{\ensuremath{\,^\textrm{g}/_\textrm{mol}\:}}
\newcommand{\M}{\ensuremath{\textrm{\,M}\:}}
\newcommand{\mol}{\ensuremath{\textrm{\,mol}\:}}
\newcommand{\mmol}{\ensuremath{\textrm{\,mmol}\:}}
\newcommand{\C}{\ensuremath{\,^\circ\textrm{C}\:}}
\newcommand{\m}{\ensuremath{\,\textrm{m}\:}}
\newcommand{\mm}{\ensuremath{\,\textrm{mm}\:}}
\newcommand{\nm}{\ensuremath{\,\textrm{nm}\:}}
\newcommand{\cm}{\ensuremath{\,\textrm{cm}\:}}
\newcommand{\mmHg}{\ensuremath{\,\textrm{mmHg}\:}}
\newcommand{\degrees}{\ensuremath{\,^\circ\:}}
\newcommand{\inch}{\ensuremath{\,\textrm{in}}}
\newcommand{\inchpersecond}{\ensuremath{\,\frac{\textrm{in}}{\textrm{s}}}}
\newcommand{\ft}{\ensuremath{\,\textrm{ft}}}

