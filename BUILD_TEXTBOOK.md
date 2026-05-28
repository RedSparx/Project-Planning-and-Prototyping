# BUILD MANIFEST — *Proposal, Planning & Prototyping* (Textbook)

This file is the **single source of truth** for building this textbook with Claude Code.
It is a build manifest, not the book. Claude Code reads it, builds **one chapter at a
time**, updates the build-state table after each chapter, and stops for review between
chapters.

> **Audience of the book:** technicians in training who can already solder, design and
> assemble PCBs, do mechanical CAD, 3D-print parts, program embedded systems, and who
> have completed AI, IoT, and robotics coursework. Write to them as capable junior
> engineers, not novices.

---

## 1. OPERATING PROCEDURE (read this first, every session)

Claude Code MUST follow this loop:

1. **Open this file and read the Build-State Table (§2).** Identify the first chapter
   whose status is `TODO`. That is the *only* chapter you build this run.
2. **Read the Global Authoring Spec (§5), Figure Standards (§6), and Math Conventions
   (§7).** These govern every chapter.
3. **Read the Running-Example State (§11).** Use it so the worked example is continuous
   across chapters. If the chapter advances the example, you will update §11 at the end.
4. **Build the chapter** per its brief in §10:
   - Create the chapter folder and its `images/` subfolder if absent.
   - Write all figures first (see §6), including the **200 dpi readability verification**.
   - Write `chapter.tex`.
5. **Update the Build-State Table (§2):** set the chapter status to `DONE`, fill in the
   figure count and a one-line note.
6. **Update the Running-Example State (§11)** if the chapter advanced it.
7. **STOP.** Do not start the next chapter. Report what was built and wait for review.

> Build chapters strictly in numerical order. Never build ahead. Never build two in one
> run unless explicitly told to.

---

## 2. BUILD-STATE TABLE  *(Claude Code edits this after each chapter)*

| Ch | Folder | Title | Status | Figures | Notes |
|----|--------|-------|--------|---------|-------|
| 1  | `chapters/01-overview`        | Overview: Prototypes, Products & the Business of Engineering | TODO | 0/4 | |
| 2  | `chapters/02-workflow`        | The Prototyping Mindset & the Workflow | TODO | 0/3 | |
| 3  | `chapters/03-prototype-vs-product` | Prototype vs. Product & Selective Prototyping | TODO | 0/2 | |
| 4  | `chapters/04-specifications`  | Specifications & Risk Prioritization | TODO | 0/3 | |
| 5  | `chapters/05-architecture`    | System Architecture & Interface Definition | TODO | 0/3 | |
| 6  | `chapters/06-ai`              | AI in Prototyping: Capability & Risk | TODO | 0/2 | |
| 7  | `chapters/07-iot-robotics`    | IoT, Robotics & Safety as a Design Obligation | TODO | 0/3 | |
| 8  | `chapters/08-planning`        | Planning & Schedule Management | TODO | 0/3 | |
| 9  | `chapters/09-bom-procurement` | Bill of Materials & Procurement | TODO | 0/3 | |
| 10 | `chapters/10-economics`       | Low-Volume Production Economics | TODO | 0/3 | |
| 11 | `chapters/11-validation`      | Validation & Test Procedure Design | TODO | 0/3 | |
| 12 | `chapters/12-documentation`   | Documentation Discipline & Portfolio Assembly | TODO | 0/3 | |
| 13 | `chapters/13-cost-bridge`     | Cost Analysis & the Bridge to Project II | TODO | 0/3 | |

Status values: `TODO` → `DONE`. (Use `BLOCKED` + a note if something prevents progress.)

---

## 3. TOOLCHAIN & PREREQUISITES

- **Typesetter:** pdfLaTeX. Compile with `pdflatex` only (never xelatex/lualatex).
- **Document class:** `Sparkle` (the user's own class). **Obtain `Sparkle.cls` and
  `default_logo.pdf` from the user's GitHub repository** and copy both into the project
  root. If the repo URL is not yet known, ask the user for it before assembling
  `main.tex`; chapters and figures can be built without it.
- **Figures:** Python + `matplotlib` (and `graphviz` for node/flow diagrams). Grayscale
  only — see §6.
- **Image inclusion across folders:** use the `import` package so each chapter's
  `\includegraphics{images/...}` resolves relative to that chapter's own folder.

---

## 4. DIRECTORY STRUCTURE (target)

```
textbook/
├── main.tex                     ← top-level assembler (Sparkle)
├── Sparkle.cls                  ← from user's GitHub repo
├── default_logo.pdf             ← from user's GitHub repo
├── BUILD_TEXTBOOK.md            ← this file
├── references.bib               ← optional; only if citations are used
└── chapters/
    ├── 01-overview/
    │   ├── chapter.tex
    │   └── images/
    │       ├── fig_01_pipeline.pdf
    │       ├── fig_01_pipeline.png      ← 200 dpi proof, for verification only
    │       └── ...
    ├── 02-workflow/
    │   ├── chapter.tex
    │   └── images/
    └── ...
```

- Every chapter is a self-contained folder with a `chapter.tex` and an `images/`
  subfolder.
- For each figure, keep **both** the vector `*.pdf` (used by LaTeX) and the `*.png`
  (200 dpi proof used only for the readability check; harmless if left in the folder).

---

## 5. GLOBAL AUTHORING SPECIFICATION

- **Voice:** professional, direct, second person ("you decide," "you document"). A
  working engineer explaining the trade to a capable junior. Institutional scaffolding
  (course codes, competencies, grading) **never appears on the page** — it is implicit.
- **Length:** 3,000–5,000 words of body per chapter.
- **Every chapter contains, in order:**
  1. Opening hook tying the chapter to its place in the workflow.
  2. Numbered **learning objectives** (measurable verbs).
  3. Body sections per the brief.
  4. At least one **worked example** with explicit arithmetic (show the numbers).
  5. **In Practice** callout(s) — short real scenarios.
  6. **Common Pitfalls** — misconceptions to dismantle.
  7. **End-of-chapter artifact** the reader produces (feeds their portfolio).
  8. **Summary** + one-paragraph transition to the next chapter.
- **LaTeX conventions:**
  - `\chapter{}`, `\section{}`, `\subsection{}` (Sparkle styles them).
  - Display equations in `equation`/`align`; inline math with `$...$`.
  - Bold the **first** use of each defined term.
  - Reference the seven-stage workflow by stage number consistently.
  - Reference every figure in the text **before** it appears: `Figure~\ref{fig:...}`.
  - Callouts: use a simple `\paragraph{In Practice.}` / `\paragraph{Common Pitfalls.}`
    lead-in (do not rely on undefined custom environments).
- **Continuity:** the running example (a connected robotic subsystem — see §11) threads
  through every chapter, gaining a business spine in Ch.1 and a technical spine from
  Ch.2 onward.

---

## 6. FIGURE STANDARDS + 200 DPI VERIFICATION  *(mandatory for every figure)*

All figures are **publication-quality black-and-white**. No color.

**Generation rules**
- Grayscale only: black lines/text on white; fills via gray levels (`0.0`–`1.0`) and/or
  hatching (`/`, `\\`, `x`, `.`, `+`). Never use color as the only differentiator.
- Font: sans-serif, **≥ 9 pt** effective size at final print width. Assume figures print
  at ~0.85 textwidth (~13 cm). Avoid tiny tick labels.
- Line weights ≥ 1.0 pt; markers large enough to read.
- Label every axis with units. Subtle grid only (`alpha=0.3`) where it aids reading.
- Save the LaTeX asset as **vector PDF**: `images/fig_NN_name.pdf`.

**The 200 dpi readability check (do not skip)**
For every figure, also export a raster proof and inspect it:
1. Save `images/fig_NN_name.png` at **200 dpi**.
2. **Open/view the PNG** and check for: overlapping labels, clipped text, lines too thin
   to read, insufficient gray contrast, illegible legends, crowded nodes.
3. If any issue is found, fix the figure script and regenerate **both** files. Repeat
   until the 200 dpi proof is clean.
4. Only then reference the PDF in `chapter.tex`.

**Reusable grayscale matplotlib preamble**
```python
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 11,
    "axes.edgecolor": "black", "axes.linewidth": 1.0,
    "axes.grid": True, "grid.alpha": 0.3, "grid.linewidth": 0.5,
    "lines.linewidth": 1.6, "savefig.bbox": "tight",
    "image.cmap": "gray",
})
GRAYS = ["0.0", "0.35", "0.6", "0.8"]   # black → light gray series
HATCH = ["", "///", "\\\\\\", "xxx", "...", "+++"]

def save(fig, stem):
    fig.savefig(f"{stem}.pdf")              # vector for LaTeX
    fig.savefig(f"{stem}.png", dpi=200)     # 200 dpi proof to verify
```

**Embedding (inside a chapter, with the `import` package active)**
```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.85\textwidth]{images/fig_NN_name.pdf}
  \caption{Complete sentence describing the figure and its takeaway.}
  \label{fig:ch-name}
\end{figure}
```

---

## 7. MATHEMATICAL NOTATION CONVENTIONS

- Currency in CAD unless a problem states otherwise.
- Define every symbol at first use. Carry units through all arithmetic.
- Recurring symbols across the book:
  - $p$ = unit selling price; $c_{\text{var}}$ = per-unit variable cost;
    $C_{\text{fixed}}$ = fixed/NRE cost; $N$ = production volume.
  - $C_{\text{unit}}(N) = \dfrac{C_{\text{fixed}}}{N} + c_{\text{var}}$  (introduced Ch.10).
  - Margin $m = p - c_{\text{var}}$; break-even volume $N_{\text{be}} = \dfrac{C_{\text{fixed}}}{p - c_{\text{var}}}$.
  - Risk $R = P_{\text{failure}}\times C_{\text{consequence}}$ (Ch.4).

---

## 8. ASSEMBLY — `main.tex` (build only after Sparkle.cls is in the root)

```latex
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% main.tex — assembles the textbook with the Sparkle document class.
% Compile: pdflatex → (bibtex if refs) → makeindex → pdflatex → pdflatex
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\documentclass[twoside]{Sparkle}

%--- Sparkle metadata (confirm values with the user) ------------------------
\reporttitle{Proposal, Planning \& Prototyping}
\authorname{AUTHOR NAME, Credential}
\authoremail{email@institution.ca}
\authoraddress{%
  \textbf{Computer Engineering Technology}\\
  Vanier College\\
  Montr\'eal, Qu\'ebec}
\documentID{247-519-VA}
\copyrightyear{2026}

%--- packages ----------------------------------------------------------------
\usepackage{amsmath,amssymb}
\usepackage{booktabs}
\usepackage{graphicx}
\usepackage{import}                 % lets each chapter use images/ relative to its folder
\usepackage[hidelinks]{hyperref}

\begin{document}

% One \import line per chapter, in order. \import sets the path context so that
% \includegraphics{images/...} inside each chapter resolves to that chapter's folder.
\import{chapters/01-overview/}{chapter.tex}
\import{chapters/02-workflow/}{chapter.tex}
\import{chapters/03-prototype-vs-product/}{chapter.tex}
\import{chapters/04-specifications/}{chapter.tex}
\import{chapters/05-architecture/}{chapter.tex}
\import{chapters/06-ai/}{chapter.tex}
\import{chapters/07-iot-robotics/}{chapter.tex}
\import{chapters/08-planning/}{chapter.tex}
\import{chapters/09-bom-procurement/}{chapter.tex}
\import{chapters/10-economics/}{chapter.tex}
\import{chapters/11-validation/}{chapter.tex}
\import{chapters/12-documentation/}{chapter.tex}
\import{chapters/13-cost-bridge/}{chapter.tex}

% \import{}{chapter_references.tex}   % only if citations are used

\end{document}
```

> Note: Sparkle fires front matter, TOC, `\mainmatter`, back matter, and the index
> automatically at `\begin{document}` / `\end{document}`. Do not call them manually.
> Each `chapter.tex` begins directly with `\chapter{...}`.

---

## 9. COMPILE SEQUENCE

Run in the project root (where `main.tex` and `Sparkle.cls` live):

```bash
pdflatex  main.tex
# bibtex  main           # only if references.bib is used
makeindex main.idx       # only if \index{} terms are used
pdflatex  main.tex
pdflatex  main.tex
```

A clean compile produces no `! Fatal error`. Overfull-hbox and font-substitution
warnings are acceptable.

---

## 10. CHAPTER BRIEFS

Each brief lists: purpose, learning objectives, sections, **required equations**,
**required figures** (each needing the §6 200 dpi check), worked example, pitfalls,
end-of-chapter artifact, and transition. Word/voice rules from §5 apply to all.

---

### Chapter 1 — Overview: Prototypes, Products & the Business of Engineering
**Folder:** `chapters/01-overview` · **Figures:** 4

**Purpose.** Establish *why* prototyping matters before the *how*, and give the reader
the map of the whole 12-week journey: the theory track, the practice (lab) track, and
how they interlock. This chapter satisfies the requirement for a course-overview of both
theory and practice.

**Learning objectives.** (1) State what a prototype is for and what you will produce.
(2) Describe how a proven prototype becomes a product, and the link to Project II.
(3) Explain your role as a technician working with engineers. (4) Explain why industry
work is justified by the value it creates. (5) Identify the business models that turn a
prototype into revenue.

**Sections.**
- 1.1 What you will build (proof-of-concept prototype + the record of how you got there).
- 1.2 The course map: the theory track and the practice track over 12 weeks, and how
  each week's theory lands just as the lab needs it. Introduce the seven-stage workflow
  at overview level (full treatment in Ch.2).
- 1.3 From prototype to product — the gap (manufacturability, reliability, cost at
  volume, certification, supportability) and what carries into Project II.
- 1.4 Working with engineers — what you own (build, test, document, procure,
  troubleshoot) vs. what engineers own (requirements, accountability, sign-off).
- 1.5 Engineering businesses by size — small/startup, medium, large; same prototype,
  different handling.
- 1.6 Science for profit — cost, time, and volume as engineering constraints; a negative
  economic result is a valuable result.
- 1.7 How a prototype becomes revenue — product sale, B2B vs B2C, hardware-as-a-service
  (IoT), licensing, build-to-order, specialty low-volume vs commodity high-volume.

**Required equations.**
- Unit margin: $m = p - c_{\text{var}}$.
- Gross margin fraction: $\text{GM} = \dfrac{p - c_{\text{var}}}{p}$.
- Forward reference to $C_{\text{unit}}(N)=C_{\text{fixed}}/N + c_{\text{var}}$ (Ch.10),
  used qualitatively here.

**Required figures (4).**
- `fig_01_pipeline` — horizontal flow: Concept → Project I (prototype) → Project II
  (product) → market; annotate what carries across each arrow.
- `fig_02_course_map` — two parallel tracks (Theory, Practice/Lab) across weeks 1–12,
  with the seven workflow stages marked on the practice track; show the three milestones.
- `fig_03_firm_spectrum` — small → medium → large firm axis vs. process formality /
  documentation weight (grayscale gradient bars).
- `fig_04_business_models` — tree/branch diagram from "validated prototype" to the
  revenue models in 1.7.

**Worked example.** For the running example, state the likely business model, what that
model requires the prototype to prove, and compute an illustrative margin: given a target
price and an estimated variable cost, compute $m$ and GM%.

**Common pitfalls.** Technically impressive ≠ good prototype; "it works" ≠ "business case
proven"; underrating the technician's hands-on judgment; reading an economic dead-end as
failure.

**End-of-chapter artifact.** A one-page **project context brief**: the project, its
business model, the firm context, and the single business question the prototype must
help answer. Sits at the front of the portfolio.

**Transition.** Into Ch.2 — the prototyping mindset and the seven-stage workflow.

---

### Chapter 2 — The Prototyping Mindset & the Workflow
**Folder:** `chapters/02-workflow` · **Figures:** 3

**Purpose.** Teach the seven-stage Prototype Development Cycle as the reasoning scaffold
for the whole book, and the discipline that a prototype answers a question.

**Learning objectives.** (1) Walk through all seven stages and the iteration loop.
(2) Define a prototype by the question it answers. (3) Choose fidelity deliberately.

**Sections.** 2.1 Prototype = answer to a question / reducer of risk. 2.2 The seven
stages (one subsection each): Specification & Risk → Scoping & Planning → Architecture →
Subsystem Design → Build & Integration → Validate & Measure → Compile & Economics.
2.3 The controlled iteration loop (Design↔Validate). 2.4 Prototype types
(proof-of-concept, breadboard, functional, looks-like/works-like, pre-production).
2.5 Fidelity matched to the question; the documentation layer named.

**Required equations.** Effort/fidelity intuition: present a simple monotonic relation
(e.g. relative effort rising steeply with fidelity level $f$) to justify "don't over-
build." Keep it illustrative, with explicit example numbers in the worked example.

**Required figures (3).**
- `fig_01_workflow` — the seven-stage spine with the Design↔Validate iteration loop
  (the book's signature diagram; reused conceptually later).
- `fig_02_fidelity_ladder` — fidelity rungs (low→high) against relative effort/cost.
- `fig_03_value` — intrinsic value (knowledge) vs extrinsic value (artifact/confidence).

**Worked example.** Given two prototype options at different fidelities that answer the
same question, compare relative effort and argue for the lower-fidelity choice.

**Common pitfalls.** "Prototype = mini-product"; "higher fidelity is always better."

**End-of-chapter artifact.** A statement of the central question the reader's prototype
must answer + the planned fidelity, with justification.

**Transition.** Into Stage 1 — prototype vs. product and selective prototyping.

---

### Chapter 3 — Prototype vs. Product & Selective Prototyping
**Folder:** `chapters/03-prototype-vs-product` · **Figures:** 2

**Purpose.** Build the judgment of what to prototype and what to specify-and-trust.

**Learning objectives.** (1) Contrast prototype vs product across goals and standards.
(2) Separate intrinsic from extrinsic value in practice. (3) Decide which subsystems
warrant a prototype.

**Sections.** 3.1 Goals (learning vs reliability) and standards (test-ready vs
manufacturable/certifiable/supportable). 3.2 Selective prototyping: prototype only
high-risk / high-uncertainty / novel elements. 3.3 The cost of changing a design later
(why early, cheap iteration matters). 3.4 Known/off-the-shelf subsystems: specify and
trust.

**Required equations.** Cost-of-change escalation (the 1–10–100 heuristic):
$C_{\text{change}}(s) \approx C_0 \cdot 10^{\,s}$ where $s$ indexes the project stage
(concept, design, build, production). Use it to justify front-loaded de-risking.

**Required figures (2).**
- `fig_01_cost_of_change` — cost-of-change vs stage on a **log** y-axis (grayscale step
  or bar plot) showing the order-of-magnitude rise.
- `fig_02_selective_decision` — decision flow: subsystem → (novel/uncertain/high-
  consequence?) → prototype vs specify-and-trust.

**Worked example.** Take the running example's subsystems; classify each; compute the
relative cost of fixing a flaw if caught at design vs at production using the heuristic.

**Common pitfalls.** Prototyping the easy/known parts to feel productive; unplanned
"tinkering" mistaken for iteration.

**End-of-chapter artifact.** Subsystem classification table (prototype vs specify-and-
trust) with one-line justifications.

**Transition.** Into formal specifications and risk ranking.

---

### Chapter 4 — Specifications & Risk Prioritization
**Folder:** `chapters/04-specifications` · **Figures:** 3 · *(Milestone 1: proposal)*

**Purpose.** Turn an idea into a measurable specification and a defensible risk ranking.

**Learning objectives.** (1) Write measurable, testable requirements. (2) Separate
requirements (what) from design (how). (3) Build and defend a risk-priority ranking.

**Sections.** 4.1 Anatomy of a specification: functional requirements, performance
targets, constraints, interfaces, acceptance criteria. 4.2 Requirements vs design.
4.3 Risk-driven prioritization. 4.4 FMEA-style ranking. 4.5 The critical path of
unknowns.

**Required equations.**
- Risk: $R = P_{\text{failure}} \times C_{\text{consequence}}$.
- FMEA risk priority number: $\text{RPN} = S \cdot O \cdot D$ (severity, occurrence,
  detection), with a worked ranking table.

**Required figures (3).**
- `fig_01_risk_matrix` — probability × consequence grid, grayscale shaded by risk band.
- `fig_02_req_vs_design` — side-by-side: a requirement statement vs a design statement.
- `fig_03_critical_unknowns` — the assumptions that, if wrong, sink the project.

**Worked example.** Convert a vague feature wish into a measurable requirement
(e.g. "fast" → "process 10 kS/s within 5 ms latency"); compute RPN for three subsystems
and rank them.

**Common pitfalls.** Unmeasurable criteria; embedding the solution inside the requirement.

**End-of-chapter artifact.** Specification + risk register + scoping rationale (the
proposal core / Milestone 1).

**Transition.** Into system architecture.

---

### Chapter 5 — System Architecture & Interface Definition
**Folder:** `chapters/05-architecture` · **Figures:** 3

**Purpose.** Decompose the prototype and define interfaces *before* building, because
integration fails at boundaries.

**Learning objectives.** (1) Decompose into subsystems. (2) Specify interface contracts
(electrical, mechanical, data, timing). (3) Allocate budgets across an interface.

**Sections.** 5.1 Decomposition. 5.2 Interfaces as contracts. 5.3 Budgets: timing,
power, error. 5.4 Why integration fails at boundaries.

**Required equations.**
- Timing budget: $T_{\text{total}} = \sum_i t_i \le T_{\text{budget}}$.
- Power budget: $P_{\text{total}} = \sum_i P_i$.
- Error combination (independent terms, RSS):
  $e_{\text{total}} = \sqrt{\sum_i e_i^{\,2}}$.

**Required figures (3).**
- `fig_01_block_diagram` — running-example system block diagram (graphviz, grayscale).
- `fig_02_interface_budget` — a budget allocated across an interface (stacked grayscale
  bar vs the budget limit line).
- `fig_03_boundary_failure` — two blocks that each work alone but mismatch at the
  interface (e.g. voltage level / data rate).

**Worked example.** Allocate a 5 ms latency budget across three pipeline stages; verify
$\sum t_i \le T_{\text{budget}}$; combine three independent measurement errors via RSS.

**Common pitfalls.** Diving into a favorite subsystem before interfaces are fixed;
"we'll figure the interface out later."

**End-of-chapter artifact.** System block diagram + interface table with budgets.

**Transition.** Into design decisions, starting with AI tooling.

---

### Chapter 6 — AI in Prototyping: Capability & Risk
**Folder:** `chapters/06-ai` · **Figures:** 2

**Purpose.** Use AI as an accelerator while keeping the engineer accountable for
correctness.

**Learning objectives.** (1) Identify where AI helps. (2) Verify every AI output against
first principles. (3) Document AI use for reproducibility.

**Sections.** 6.1 Where AI helps (scaffolding, boilerplate, debugging, design-space
exploration, documentation). 6.2 Accelerator, not autonomous designer. 6.3 Hallucination
and human-in-the-loop verification. 6.4 The black-box problem (validate via simulation /
bench test). 6.5 IP and data-leakage risk. 6.6 Reproducibility and traceability.

**Required equations.** Expected cost of an unverified error:
$\mathbb{E}[C_{\text{err}}] = p_{\text{err}} \cdot C_{\text{consequence}}$ — used to
justify the cost of verification vs the cost of a missed fault.

**Required figures (2).**
- `fig_01_hitl_loop` — human-in-the-loop verification cycle (AI proposes → engineer
  verifies → accept/reject → document).
- `fig_02_trust_matrix` — where AI may be trusted vs where it must not (e.g. boilerplate
  vs safety/timing-critical), grayscale quadrants.

**Worked example.** Given an AI-suggested component value or code snippet with a stated
error probability and a failure consequence cost, compute $\mathbb{E}[C_{\text{err}}]$
and decide the verification effort.

**Common pitfalls.** Trusting plausible output; pasting confidential design data into
public tools; undocumented AI use.

**End-of-chapter artifact.** Decision-log entries recording AI use and its verification.

**Transition.** Into IoT, robotics, and safety as design obligations.

---

### Chapter 7 — IoT, Robotics & Safety as a Design Obligation
**Folder:** `chapters/07-iot-robotics` · **Figures:** 3

**Purpose.** Build security and safety into the design at Stage 4, not after.

**Learning objectives.** (1) Design IoT security in from the start. (2) Size a power /
battery budget for a connected device. (3) Identify and mitigate robotics physical-safety
risks; apply EMC/ESD/PPE thinking at design time.

**Sections.** 7.1 IoT security by design (encryption, authentication, secure protocols).
7.2 Attack surfaces (connectivity, communication, management). 7.3 Privacy/data
obligations. 7.4 Protocol choice (MQTT/CoAP/BLE) as a consequential decision. 7.5 Power
& battery budgeting for connected devices. 7.6 Robotics physical safety: e-stops,
guarding, fail-safe, force/speed limits; human-robot interaction. 7.7 Absorbed safety
practice: EMC, ESD, PPE.

**Required equations.**
- Average current with duty cycle $D$:
  $I_{\text{avg}} = D\,I_{\text{active}} + (1-D)\,I_{\text{sleep}}$.
- Battery life: $t_{\text{life}} = \dfrac{C_{\text{batt}}}{I_{\text{avg}}}$
  ($C_{\text{batt}}$ in mAh, $I$ in mA → hours).
- Mechanical safety factor: $\text{SF} = \dfrac{\text{capacity}}{\text{applied load}}$.

**Required figures (3).**
- `fig_01_attack_surface` — layered IoT architecture with the three attack surfaces
  marked.
- `fig_02_power_budget` — duty-cycled current profile (active/sleep) and resulting
  $I_{\text{avg}}$; annotate battery life.
- `fig_03_robot_safety` — robot workspace with safety zones, guarding, and e-stop in the
  control path.

**Worked example.** A sensor node: $I_{\text{active}}=80$ mA, $I_{\text{sleep}}=0.05$ mA,
$D=2\%$, $C_{\text{batt}}=2000$ mAh. Compute $I_{\text{avg}}$ and $t_{\text{life}}$;
show how lowering $D$ extends life.

**Common pitfalls.** "Add security later"; default credentials; safety treated as a final
inspection; no e-stop on a moving prototype.

**End-of-chapter artifact.** Updated design records capturing security, power, and safety
decisions.

**Transition.** Into planning and schedule management for the build.

---

### Chapter 8 — Planning & Schedule Management
**Folder:** `chapters/08-planning` · **Figures:** 3

**Purpose.** Build a realistic, maintained schedule with a critical path and procurement
lead times.

**Learning objectives.** (1) Build a WBS and a critical-path schedule. (2) Compute slack
and identify the critical path. (3) Estimate durations under uncertainty (PERT) and treat
lead time as a scheduled risk.

**Sections.** 8.1 Work breakdown structure. 8.2 Dependencies and the critical path.
8.3 Gantt scheduling. 8.4 Three-point (PERT) estimation. 8.5 Lead time as a planning
risk. 8.6 Maintaining the risk register.

**Required equations.**
- CPM: earliest/latest start & finish; $\text{slack} = \text{LS} - \text{ES} =
  \text{LF} - \text{EF}$; critical path = activities with zero slack.
- PERT expected duration: $t_e = \dfrac{a + 4m + b}{6}$, with
  $\sigma = \dfrac{b-a}{6}$.

**Required figures (3).**
- `fig_01_gantt` — Gantt of the running example (grayscale bars, milestones as markers).
- `fig_02_cpm_network` — activity-on-node network with the critical path bolded.
- `fig_03_pert` — three-point estimate (a, m, b) and the resulting $t_e$.

**Worked example.** A small network of 5–6 activities: compute ES/EF/LS/LF, slack, and
the critical path; compute $t_e$ and $\sigma$ for one activity from $a,m,b$.

**Common pitfalls.** A Gantt made once and never updated; ignoring component lead time.

**End-of-chapter artifact.** Gantt chart + updated risk register.

**Transition.** Into the bill of materials and procurement the schedule depends on.

---

### Chapter 9 — Bill of Materials & Procurement
**Folder:** `chapters/09-bom-procurement` · **Figures:** 3

**Purpose.** Produce a complete, costed BOM and run the full procurement document chain.

**Learning objectives.** (1) Build a multi-level, costed BOM with designators and
alternates. (2) Derive a purchase list and compare quotes. (3) Operate PO → receipt /
invoice → reconciliation.

**Sections.** 9.1 BOM as a design document (part number, qty, spec, unit cost,
designator, alternates; multi-level). 9.2 Purchase list derived from BOM (stock, shared
resources). 9.3 Quotes (price, availability, lead time). 9.4 Purchase order. 9.5 Receipt
vs invoice. 9.6 Reconciliation; the as-built BOM (forward reference to Ch.12).

**Required equations.**
- Line extended cost: $\text{ext}_i = q_i \cdot u_i$.
- BOM total: $C_{\text{BOM}} = \sum_i q_i u_i$.
- With attrition/overage factor $\alpha$ (spares/failures):
  $q_i^{\text{order}} = \lceil (1+\alpha)\, q_i \rceil$.

**Required figures (3).**
- `fig_01_doc_chain` — BOM → purchase list → quote → PO → receipt/invoice →
  reconciliation (flow).
- `fig_02_bom_tree` — multi-level BOM (assembly → subassembly → component).
- `fig_03_rollup` — cost rollup visualization (stacked grayscale contribution by
  subsystem).

**Worked example.** A 6–8 line BOM: compute extended costs, apply a 10% overage to
consumables, total $C_{\text{BOM}}$; compare two supplier quotes differing in price and
lead time.

**Common pitfalls.** BOM as an afterthought list; no alternates for long-lead parts;
wrong footprint from a missing designator.

**End-of-chapter artifact.** Costed BOM + purchase list + procurement records.

**Transition.** Into the economics those costs imply at volume.

---

### Chapter 10 — Low-Volume Production Economics
**Folder:** `chapters/10-economics` · **Figures:** 3 · *(Milestone 2: design review)*

**Purpose.** Explain why per-unit cost falls with volume and how design locks in cost.

**Learning objectives.** (1) Use the unit-cost model. (2) Find the break-even volume
between two methods. (3) Connect design choices to production cost (DFM/DFA).

**Sections.** 10.1 Why low-volume/bridge production exists. 10.2 Fixed vs variable cost.
10.3 The unit-cost curve. 10.4 Break-even between two processes. 10.5 DFM/DFA and the
design-locks-cost principle. 10.6 Failure economics (validate early and cheaply).

**Required equations.**
- $C_{\text{unit}}(N) = \dfrac{C_{\text{fixed}}}{N} + c_{\text{var}}$.
- Method break-even: solve
  $\dfrac{C_{f1}}{N^\ast} + c_{v1} = \dfrac{C_{f2}}{N^\ast} + c_{v2}$ for $N^\ast$.
- Design-locks-cost heuristic: ~70–80% of final manufacturing cost is committed during
  design.

**Required figures (3).**
- `fig_01_unit_cost_curve` — $C_{\text{unit}}$ vs $N$ (hyperbola → asymptote at
  $c_{\text{var}}$).
- `fig_02_breakeven` — two methods (e.g. 3D-print vs injection-mold) crossing at
  $N^\ast$.
- `fig_03_cost_committed` — cost committed vs cost incurred across project phases (two
  grayscale curves).

**Worked example.** $C_{\text{fixed}}=\$8000$, $c_{\text{var}}=\$12$: tabulate
$C_{\text{unit}}$ at $N=1,50,500$; then find $N^\ast$ between 3D printing
($C_f=0,\ c_v=\$40$) and molding ($C_f=\$8000,\ c_v=\$6$).

**Common pitfalls.** Assuming prototype unit cost equals production unit cost.

**End-of-chapter artifact.** Preliminary cost analysis (feeds Ch.13).

**Transition.** Into validating what was built.

---

### Chapter 11 — Validation & Test Procedure Design
**Folder:** `chapters/11-validation` · **Figures:** 3

**Purpose.** Test against criteria defined in advance; collect and interpret performance
data; decide iterations on evidence.

**Learning objectives.** (1) Write test procedures before testing. (2) Tie acceptance
criteria to the specification. (3) Quantify whether results meet spec, including basic
variation.

**Sections.** 11.1 Procedures written in advance. 11.2 Acceptance criteria traced to
spec. 11.3 Functional demonstration vs quantitative data. 11.4 Measurement, tolerance,
and margin. 11.5 Basic statistics for pass/fail with variation. 11.6 The documented
iteration decision.

**Required equations.**
- Sample mean $\bar{x} = \frac{1}{n}\sum x_i$; sample std
  $s = \sqrt{\frac{1}{n-1}\sum (x_i-\bar{x})^2}$.
- Margin to a limit: $z = \dfrac{\text{USL} - \bar{x}}{s}$.
- Capability: $C_p = \dfrac{\text{USL}-\text{LSL}}{6\sigma}$ (introduce, interpret simply).

**Required figures (3).**
- `fig_01_test_flow` — test procedure flow (setup → measure → record → pass/fail →
  iterate).
- `fig_02_tolerance_band` — measured values against a tolerance band with margins.
- `fig_03_distribution_limits` — a distribution with LSL/USL and $\bar{x}\pm N s$.

**Worked example.** Ten measurements: compute $\bar{x}$ and $s$; given a spec limit,
compute $z$ and $C_p$; decide pass/fail and whether to iterate.

**Common pitfalls.** Tests written to confirm success rather than detect failure; testing
after the fact; ignoring variation.

**End-of-chapter artifact.** Test procedure + raw data + iteration decision memo.

**Transition.** Into compiling the evidence into a portfolio.

---

### Chapter 12 — Documentation Discipline & Portfolio Assembly
**Folder:** `chapters/12-documentation` · **Figures:** 3

**Purpose.** Make documentation the by-product of doing the work, and assemble the
portfolio from existing artifacts.

**Learning objectives.** (1) Apply the three documentation principles. (2) Produce an
as-built BOM. (3) Establish traceability requirement → design → test.

**Sections.** 12.1 Three principles (record decisions not outcomes; enable reproduction;
documentation debt compounds). 12.2 Documentation runs parallel to the workflow.
12.3 Compiling, not writing, the portfolio. 12.4 The as-built BOM. 12.5 Traceability.

**Required equations.** Traceability coverage:
$\text{coverage} = \dfrac{\text{requirements with a linked test}}{\text{total requirements}}$,
expressed as a percentage; target 100%.

**Required figures (3).**
- `fig_01_doc_parallel` — documentation layer running parallel to the seven stages
  (timeline with artifact tags per stage).
- `fig_02_traceability` — requirement → design element → test case mapping.
- `fig_03_portfolio_assembly` — stage artifacts feeding into the final portfolio.

**Worked example.** Build a small traceability matrix for the running example; compute
coverage; identify an untested requirement; reconcile a design-BOM line against the
as-built reality.

**Common pitfalls.** Writing the portfolio from memory; as-built BOM never reconciled.

**End-of-chapter artifact.** Draft portfolio + as-built BOM.

**Transition.** Into the closing cost analysis and the handoff to Project II.

---

### Chapter 13 — Cost Analysis & the Bridge to Project II
**Folder:** `chapters/13-cost-bridge` · **Figures:** 3 · *(Milestone 3: final portfolio)*

**Purpose.** Project production cost from the validated prototype and define readiness for
Project II.

**Learning objectives.** (1) Produce a basic production cost projection. (2) Compute
break-even units against a target price. (3) State what the prototype proved and what
Project II must still resolve.

**Sections.** 13.1 Applying the cost model to the finished prototype. 13.2 Prototype cost
vs projected production cost. 13.3 Break-even and margin at the target price. 13.4
Extrinsic value and design readiness. 13.5 Lessons learned. 13.6 The handoff to Project
II (Design, Manufacturing & Production).

**Required equations.**
- $C_{\text{unit}}(N)$ reused for projection.
- Break-even units: $N_{\text{be}} = \dfrac{C_{\text{fixed}}}{p - c_{\text{var}}}$.
- Margin at volume: $m = p - C_{\text{unit}}(N)$; total profit
  $\Pi(N) = N\,(p - c_{\text{var}}) - C_{\text{fixed}}$.

**Required figures (3).**
- `fig_01_cost_projection` — projected $C_{\text{unit}}$ at $N=1,50,500$ for the running
  example (bar or curve).
- `fig_02_proto_vs_prod` — prototype cost vs projected production cost (paired bars).
- `fig_03_readiness_handoff` — what Project I delivers vs what Project II must resolve.

**Worked example.** With the running example's $C_{\text{fixed}}$, $c_{\text{var}}$, and
a target $p$: compute $N_{\text{be}}$, margin at $N=500$, and $\Pi(500)$; write a
two-sentence readiness statement.

**Common pitfalls.** Conflating "it works" with "ready to produce"; treating a negative
economic finding as failure.

**End-of-chapter artifact.** Final portfolio submission (Milestone 3) with the production
cost projection and readiness statement.

**Transition.** Forward to Project II — the prototype becomes a product.

---

## 11. RUNNING-EXAMPLE STATE  *(Claude Code updates this as chapters advance it)*

> A single example threads through the whole book so arithmetic and diagrams stay
> concrete and continuous. Update the fields below as each chapter develops them.

**Example product:** a **connected (IoT) robotic sorting subsystem** — a small
sensor-guided actuator that classifies and diverts items on a bench conveyor, reports
status over a network, and is intended as a module within a larger automation product.
It exercises every reader skill area: PCB + embedded firmware + mechanical/3D-printed
parts + an AI inference step + IoT connectivity + a moving (robotic) element requiring
safety design.

| Field | Current value | Set/updated in |
|---|---|---|
| Business model | *(set in Ch.1)* | Ch.1 |
| Firm context | *(set in Ch.1)* | Ch.1 |
| Central question the prototype answers | *(set in Ch.2)* | Ch.2 |
| Chosen fidelity | *(set in Ch.2)* | Ch.2 |
| Subsystem classification (prototype vs trust) | *(set in Ch.3)* | Ch.3 |
| Specification + risk ranking | *(set in Ch.4)* | Ch.4 |
| Architecture + interface budgets | *(set in Ch.5)* | Ch.5 |
| Power/battery numbers | *(set in Ch.7)* | Ch.7 |
| Schedule (key activities, critical path) | *(set in Ch.8)* | Ch.8 |
| BOM totals ($C_{\text{fixed}}$, $c_{\text{var}}$) | *(set in Ch.9–10)* | Ch.9–10 |
| Target price $p$ | *(set in Ch.10/13)* | Ch.10/13 |
| Validation results | *(set in Ch.11)* | Ch.11 |

Keep numbers internally consistent: the $C_{\text{fixed}}$, $c_{\text{var}}$, and $p$
chosen for the economics chapters must match those reused in Chapter 13.

---

## 12. DEFINITION OF DONE (per chapter)

- [ ] Chapter folder + `images/` created.
- [ ] All required figures generated as **vector PDF**, each with a **200 dpi PNG proof
      that was viewed and verified readable** (labels, contrast, no clipping).
- [ ] `chapter.tex` written to the §5 structure, with all required equations and worked
      example showing explicit arithmetic.
- [ ] Every figure referenced in text before it appears; captions are full sentences.
- [ ] Build-State Table (§2) updated to `DONE` with figure count + note.
- [ ] Running-Example State (§11) updated if advanced.
- [ ] Stopped for review; next chapter NOT started.
