# BUILD MANIFEST — *Proposal, Planning & Prototyping* (Textbook)
# Version 2.0 — revised structure (17 chapters + course plan)

This file is the **single source of truth** for building this textbook with Claude Code.
Claude Code reads it, builds **one chapter at a time**, updates the build-state table,
and stops for review between chapters.

> **Audience:** technicians in training who can solder, design/assemble PCBs, do
> mechanical CAD, 3D-print parts, program embedded systems, and have completed AI, IoT,
> and robotics coursework. Address them as capable junior engineers, never as novices.

---

## 1. OPERATING PROCEDURE *(read this first, every session)*

1. **Read the Build-State Table (§2).** Find the first chapter marked `REDO` or `TODO`.
   That is the ONLY chapter you build this run. `REDO` takes priority over `TODO`.
2. **Read the Migration Notes (§3)** if the chapter is marked `REDO`.
3. **Read the Global Authoring Spec (§6), Figure Standards (§7), and Math Conventions
   (§8).** These govern every chapter.
4. **Read the Running-Example State (§12).** Keep the example continuous and consistent.
5. **Build the chapter** per its brief in §11:
   - Create or rename the folder and its `images/` subfolder per §3 if needed.
   - Generate all figures first (§7) including the 200 dpi readability check.
   - Write `chapter.tex`.
6. **Update the Build-State Table (§2):** set status to `DONE`, fill figure count + note.
7. **Update the Running-Example State (§12)** if the chapter advanced it.
8. **STOP.** Report what was built. Do not start the next chapter.

> Build in status order: clear all `REDO` chapters first (in numerical order), then
> `TODO` chapters in order. Never build two chapters in one run unless explicitly told.

---

## 2. BUILD-STATE TABLE *(Claude Code edits this after each chapter)*

| Ch | Folder | Title | Status | Figures | Notes |
|----|--------|-------|--------|---------|-------|
| 1  | `chapters/01-overview`              | Overview: Prototypes, Products & the Business of Engineering | REDO | 0/4 | Minor update: add Stage-Gate/Kano forward ref; add IP awareness para |
| 2  | `chapters/02-stagegate-kano`        | Product Development & the Stage-Gate Model | TODO | 0/4 | New chapter; absorbs old Ch.3 content |
| 3  | `chapters/03-workflow`              | The Prototyping Mindset & the Workflow | REDO | 0/3 | Renumbered from old Ch.2; add Stage-Gate framing opener |
| 4  | `chapters/04-specifications`        | Specifications & Risk Prioritization | REDO | 0/3 | Renumbered from old Ch.4; add Stage-Gate phase label opener |
| 5  | `chapters/05-architecture`          | System Architecture & Interface Definition | TODO | 0/3 | |
| 6  | `chapters/06-component-selection`   | Component Selection & Datasheet Literacy | TODO | 0/3 | New chapter |
| 7  | `chapters/07-dfx`                   | Design for X | TODO | 0/3 | New chapter |
| 8  | `chapters/08-ai`                    | AI in Prototyping: Capability & Risk | TODO | 0/2 | Tightened scope vs old Ch.6 |
| 9  | `chapters/09-iot-robotics`          | IoT, Robotics & Safety as a Design Obligation | TODO | 0/3 | |
| 10 | `chapters/10-planning`              | Planning & Schedule Management | TODO | 0/3 | |
| 11 | `chapters/11-bom-procurement`       | Bill of Materials & Procurement | TODO | 0/3 | |
| 12 | `chapters/12-economics`             | Low-Volume Production Economics | TODO | 0/3 | |
| 13 | `chapters/13-version-control`       | Version Control & Design History | TODO | 0/3 | New chapter |
| 14 | `chapters/14-validation`            | Validation & Test Procedure Design | TODO | 0/4 | Failure analysis section added |
| 15 | `chapters/15-ip`                    | Intellectual Property Basics | TODO | 0/2 | New chapter |
| 16 | `chapters/16-documentation`         | Documentation & Portfolio Assembly | TODO | 0/3 | Shortened (~1500 words) |
| 17 | `chapters/17-cost-bridge`           | Cost Analysis & the Bridge to Project II | TODO | 0/3 | |
| CP | `courseplan/`                       | 12-Week Course Plan (standalone document) | TODO | 0/2 | Build after Ch.17 |

Status values: `TODO` `REDO` `DONE` `BLOCKED`

---

## 3. MIGRATION NOTES *(for REDO chapters only)*

Four chapters were built under the old 13-chapter manifest. The following instructions
tell Claude Code exactly what to do with the existing folders before rewriting.

### Chapter 1 (REDO)
- **Old folder:** `chapters/01-overview/` — **keep folder name unchanged**
- **What changes:** Add a forward reference to Stage-Gate and Kano (introduced in Ch.2).
  Add one paragraph in §1.7 (business models) noting that IP ownership is a business
  consideration (forward ref to Ch.15). Update the course-map figure to reflect 17
  chapters and the new Stage-Gate phase annotations. All other content is valid.
- **Action:** Overwrite `chapter.tex` in place. Regenerate only the course-map figure
  (`fig_02_course_map`). Keep the other three figures.

### Chapter 2 — old workflow chapter (REDO, becomes new Chapter 3)
- **Old folder:** `chapters/02-workflow/`
- **New folder:** `chapters/03-workflow/`
- **Action:** Rename the folder. In `chapter.tex`, update the chapter number references
  and add a one-paragraph opener locating this chapter within Stage 2/3 of the
  Cooper Stage-Gate model (i.e., this is the work done inside the gate, not the gate
  decision itself). All figures and content are otherwise valid.

### Chapter 3 — old prototype-vs-product chapter (SUPERSEDED)
- **Old folder:** `chapters/03-prototype-vs-product/`
- **Action:** Delete this folder entirely. Its content is absorbed into new Chapter 2
  (Stage-Gate + Kano). Do not port any files forward.

### Chapter 4 — specifications chapter (REDO, renumbered)
- **Old folder:** `chapters/04-specifications/`
- **New folder:** same — `chapters/04-specifications/` *(folder name unchanged)*
- **Action:** In `chapter.tex`, add a one-paragraph opener stating that this chapter
  operates at Stage 2 of the Stage-Gate model (scoping/feasibility) and that the
  risk register produced here feeds the Gate 2 decision. No figures need regeneration.
  All arithmetic and content are valid.

---

## 4. TOOLCHAIN & PREREQUISITES

- **Typesetter:** pdfLaTeX only (never xelatex or lualatex).
- **Document class:** `Sparkle` from the user's GitHub repository. Copy `Sparkle.cls`
  and `default_logo.pdf` into the project root before building `main.tex`. Chapters
  and figures can be built before `Sparkle.cls` is present.
- **Figures:** Python + `matplotlib`; `graphviz` for flow/node diagrams. Grayscale only.
- **Folder-relative image paths:** use the `import` package so each chapter's
  `\includegraphics{images/...}` resolves relative to its own folder (see §5).

---

## 5. DIRECTORY STRUCTURE

```
textbook/
├── main.tex                        ← Sparkle assembler
├── Sparkle.cls                     ← from user's GitHub repo
├── default_logo.pdf                ← from user's GitHub repo
├── BUILD_TEXTBOOK.md               ← this file
├── references.bib                  ← add entries as needed
├── courseplan/
│   ├── courseplan.tex              ← standalone course-plan document
│   └── images/
└── chapters/
    ├── 01-overview/
    │   ├── chapter.tex
    │   └── images/
    │       ├── fig_01_pipeline.pdf
    │       ├── fig_01_pipeline.png     ← 200 dpi proof
    │       └── ...
    ├── 02-stagegate-kano/
    │   ├── chapter.tex
    │   └── images/
    └── ...  (03 through 17)
```

Each figure appears as both a vector `.pdf` (used by LaTeX) and a `.png` (200 dpi proof
for readability verification only).

---

## 6. GLOBAL AUTHORING SPECIFICATION

- **Voice:** professional, direct, second person. A working engineer explaining the trade
  to a capable junior. No institutional scaffolding (course codes, grades, competencies)
  ever appears on the page.
- **Length:** 3,000–5,000 words body per chapter. Chapter 15 (IP) and Chapter 16
  (Documentation) are exceptions: target ~2,000 words each.
- **Every chapter contains, in order:**
  1. Stage-Gate location opener (one short paragraph stating which Stage-Gate stage/gate
     this chapter's work serves — omit only for Ch.1 and Ch.2 which establish the model).
  2. Numbered **learning objectives** (measurable verbs, 3–5).
  3. Body sections per the brief.
  4. At least one **worked example** with explicit arithmetic (show every step).
  5. **In Practice** callout(s) — short real-world scenarios.
  6. **Common Pitfalls** — misconceptions to dismantle directly.
  7. **End-of-chapter artifact** the reader produces (feeds their portfolio).
  8. **Summary** + one-paragraph transition to the next chapter.
- **LaTeX conventions:**
  - `\chapter{}`, `\section{}`, `\subsection{}` — Sparkle styles automatically.
  - Display equations: `equation` or `align` environments.
  - Bold the **first use** of every defined term. Add to `\index{}`.
  - Reference every figure in text **before** it appears: `Figure~\ref{fig:label}`.
  - Callouts via `\paragraph{In Practice.}` and `\paragraph{Common Pitfalls.}`.
  - Stage-Gate opener via `\paragraph{Where this fits.}` at chapter start.
- **Continuity:** the running example (connected robotic sorting subsystem, §12) threads
  through every chapter. Numbers set in one chapter are reused in all later chapters.

---

## 7. FIGURE STANDARDS + 200 DPI VERIFICATION *(mandatory, no exceptions)*

**All figures are publication-quality black and white. No colour.**

**Generation rules**
- Grayscale fills (`0.0`–`1.0`) and/or hatching (`/`, `\\`, `x`, `.`, `+`).
- Sans-serif font, **≥ 9 pt** at final print width (~13 cm / 0.85 textwidth).
- Line weights ≥ 1.0 pt. Label every axis with units. Grid `alpha=0.3` only where useful.
- Save the LaTeX asset as vector PDF: `images/fig_NN_name.pdf`.

**200 dpi readability check — do not skip**
1. Export `images/fig_NN_name.png` at 200 dpi.
2. **View the PNG.** Check for: overlapping labels, clipped text, lines too thin to read,
   insufficient contrast, illegible legend, crowded nodes.
3. Fix and regenerate both files if any issue found. Repeat until the PNG is clean.
4. Only then embed the PDF in `chapter.tex`.

**Reusable grayscale preamble**
```python
import matplotlib as mpl, matplotlib.pyplot as plt
mpl.rcParams.update({
    "font.family": "sans-serif", "font.size": 11,
    "axes.edgecolor": "black", "axes.linewidth": 1.0,
    "axes.grid": True, "grid.alpha": 0.3, "grid.linewidth": 0.5,
    "lines.linewidth": 1.6, "savefig.bbox": "tight", "image.cmap": "gray",
})
GRAYS = ["0.0", "0.35", "0.55", "0.75"]
HATCH = ["", "///", "\\\\\\", "xxx", "...", "+++"]

def save(fig, stem):
    fig.savefig(f"{stem}.pdf")
    fig.savefig(f"{stem}.png", dpi=200)
```

**LaTeX embedding**
```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.85\textwidth]{images/fig_NN_name.pdf}
  \caption{Complete sentence stating what the figure shows and its key takeaway.}
  \label{fig:chN-name}
\end{figure}
```

---

## 8. MATHEMATICAL NOTATION CONVENTIONS

- Currency in CAD unless stated otherwise.
- Define every symbol at first use; carry units through all arithmetic.
- **Recurring symbols (consistent across all chapters):**
  - $p$ = unit selling price
  - $c_{\text{var}}$ = per-unit variable cost
  - $C_{\text{fixed}}$ = fixed / NRE cost
  - $N$ = production volume
  - $m = p - c_{\text{var}}$ = unit margin
  - $C_{\text{unit}}(N) = C_{\text{fixed}}/N + c_{\text{var}}$ (introduced Ch.12)
  - $N_{\text{be}} = C_{\text{fixed}} / (p - c_{\text{var}})$ (introduced Ch.12)
  - $R = P_{\text{failure}} \times C_{\text{consequence}}$ (introduced Ch.4)

---

## 9. ASSEMBLY — `main.tex`

Build this file only after `Sparkle.cls` is in the project root.

```latex
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% main.tex — Proposal, Planning & Prototyping
% Compile: pdflatex → bibtex → makeindex → pdflatex → pdflatex
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\documentclass[twoside]{Sparkle}

\reporttitle{Proposal, Planning \& Prototyping}
\authorname{AUTHOR NAME, Credential}
\authoremail{email@vanier.ca}
\authoraddress{%
  \textbf{Computer Engineering Technology}\\
  Vanier College\\
  Montr\'eal, Qu\'ebec}
\documentID{247-519-VA}
\copyrightyear{2026}

\usepackage{amsmath,amssymb}
\usepackage{booktabs}
\usepackage{graphicx}
\usepackage{import}
\usepackage[hidelinks]{hyperref}
\usepackage{cite}

\begin{document}

\import{chapters/01-overview/}{chapter.tex}
\import{chapters/02-stagegate-kano/}{chapter.tex}
\import{chapters/03-workflow/}{chapter.tex}
\import{chapters/04-specifications/}{chapter.tex}
\import{chapters/05-architecture/}{chapter.tex}
\import{chapters/06-component-selection/}{chapter.tex}
\import{chapters/07-dfx/}{chapter.tex}
\import{chapters/08-ai/}{chapter.tex}
\import{chapters/09-iot-robotics/}{chapter.tex}
\import{chapters/10-planning/}{chapter.tex}
\import{chapters/11-bom-procurement/}{chapter.tex}
\import{chapters/12-economics/}{chapter.tex}
\import{chapters/13-version-control/}{chapter.tex}
\import{chapters/14-validation/}{chapter.tex}
\import{chapters/15-ip/}{chapter.tex}
\import{chapters/16-documentation/}{chapter.tex}
\import{chapters/17-cost-bridge/}{chapter.tex}

\end{document}
```

---

## 10. COMPILE SEQUENCE

```bash
pdflatex  main.tex
bibtex    main
makeindex main.idx
pdflatex  main.tex
pdflatex  main.tex
```

Course plan compiled separately:
```bash
cd courseplan
pdflatex  courseplan.tex
pdflatex  courseplan.tex
```

---

## 11. CHAPTER BRIEFS

---

### Chapter 1 — Overview: Prototypes, Products & the Business of Engineering
**Folder:** `chapters/01-overview` · **Status:** REDO · **Figures:** 4 (regenerate fig_02 only)

**Changes from previous build:** Add a forward-reference sentence to Stage-Gate/Kano
at the end of §1.3 ("The process by which your prototype earns the right to become a
product is formalised in Chapter 2."). Add one sentence in §1.7 noting IP ownership
as a business-model consideration (forward ref to Ch.15). Regenerate `fig_02_course_map`
to show 17 chapters and Stage-Gate phase bands across the 12-week timeline.

**Purpose.** Establish why prototyping matters commercially and professionally, and give
the reader the map of the full 12-week journey before any technical content begins.

**Learning objectives.** (1) State what this book will teach and what you will produce.
(2) Trace a prototype's path to a product. (3) Describe your role as a technician
alongside engineers. (4) Explain why technical work is justified by the value it creates.
(5) Name the business models that turn a prototype into revenue.

**Sections.**
- 1.1 What you will build.
- 1.2 The course map: theory track and practice track over 12 weeks; the seven-stage
  workflow at overview level; three milestones; Stage-Gate phase bands (forward ref
  to Ch.2 for full treatment).
- 1.3 From prototype to product — the gap and what carries forward.
- 1.4 Working with engineers — what you own vs what engineers own.
- 1.5 Engineering businesses by size: small/startup, medium, large.
- 1.6 Science for profit.
- 1.7 Business models: product sale, B2B/B2C, hardware-as-a-service, licensing,
  build-to-order, low-volume specialty vs commodity; IP ownership as a business
  consideration (forward ref to Ch.15).

**Required equations.**
- Unit margin: $m = p - c_{\text{var}}$.
- Gross margin: $\mathrm{GM} = (p - c_{\text{var}})/p$.

**Required figures (4).**
- `fig_01_pipeline` — Concept → Project I → Project II → market (horizontal flow).
- `fig_02_course_map` — **REGENERATE:** two parallel tracks (Theory / Practice) across
  weeks 1–12; Stage-Gate phase bands; three milestone markers; 17-chapter spine.
- `fig_03_firm_spectrum` — small → large axis vs process formality.
- `fig_04_business_models` — tree from "validated prototype" to revenue models.

**Worked example.** For the running example state the business model, compute
illustrative $m$ and GM% from a target price and estimated variable cost.

**Common pitfalls.** Technically impressive ≠ good prototype; "it works" ≠ "business
case proven"; reading an economic dead-end as failure.

**End-of-chapter artifact.** One-page project context brief: project, business model,
firm context, single business question the prototype must answer.

**Transition.** Into Ch.2 — the formal product development process and how prototyping
earns its place within it.

---

### Chapter 2 — Product Development & the Stage-Gate Model
**Folder:** `chapters/02-stagegate-kano` · **Status:** TODO · **Figures:** 4

**Purpose.** Establish the product development lifecycle and the Cooper Stage-Gate model
as the professional frame for all subsequent work. Introduce Kano analysis as the tool
that determines what a product must do and therefore what the prototype must prove.
Absorbs the selective-prototyping content of the old Chapter 3.

**Learning objectives.** (1) Name the five Stage-Gate stages and what each gate decides.
(2) Locate this course and Project II within the Stage-Gate model. (3) Classify features
using Kano categories. (4) Use Kano satisfaction coefficients to prioritise prototype
scope.

**Sections.**
- 2.1 The product development lifecycle: concept → scoping → development → testing →
  launch → sustain. The full arc a product travels.
- 2.2 The Cooper Stage-Gate model: five stages (Discovery, Scoping, Build Business Case,
  Development, Testing & Validation, Launch), five gates (go/kill/hold/recycle
  decisions). Where this course sits: Stage 2/3, Gate 3. Where Project II sits:
  Stage 3/4, Gate 4. Keep the treatment practical — name it, frame it, apply it.
- 2.3 What a gate decision requires: the Business Case, the resource plan, and the
  validated-prototype evidence that this textbook teaches you to produce.
- 2.4 Kano analysis: the five feature categories (basic/threshold, performance,
  delighter/excitement, indifferent, reverse). Why category determines prototyping
  priority: delighters and uncertain performance features warrant prototyping; threshold
  features do not.
- 2.5 Kano satisfaction and dissatisfaction coefficients: how to quantify feature
  priority from survey data.
- 2.6 From Kano to prototype scope: combining Stage-Gate position with Kano results to
  decide what to build. This is the principled version of selective prototyping.

**Required equations.**
- Kano satisfaction coefficient:
  $\mathrm{CS} = \dfrac{f(\text{functional}) + f(\text{both})}{f(\text{functional}) + f(\text{dysfunctional}) + f(\text{both}) + f(\text{neither})}$
- Kano dissatisfaction coefficient:
  $\mathrm{DS} = -\dfrac{f(\text{dysfunctional}) + f(\text{both})}{f(\text{functional}) + f(\text{dysfunctional}) + f(\text{both}) + f(\text{neither})}$
- A feature with high CS and high |DS| is performance; high CS and low |DS| is
  delighter; low CS and high |DS| is threshold. Show a worked survey table.

**Required figures (4).**
- `fig_01_stagegate` — the five-stage, five-gate funnel (left to right); annotate where
  this course and Project II sit.
- `fig_02_kano_map` — the classic Kano satisfaction vs fulfilment curve, grayscale,
  with the five categories labelled.
- `fig_03_kano_cs_ds` — CS vs |DS| scatter (four quadrants): threshold, performance,
  delighter, indifferent.
- `fig_04_scope_decision` — decision flow: feature → Kano category → prototype or
  specify-and-trust.

**Worked example.** For the running example: a 5-feature Kano survey table with
hypothetical response counts; compute CS and DS for each; plot on the CS/|DS| quadrant;
derive the prototype scope — which features to build, which to specify.

**In Practice.** A team that prototyped a polished enclosure (threshold feature) before
proving the AI inference speed (performance feature) and ran out of time.

**Common pitfalls.** Treating all features as equally important; prototyping known/
threshold features for comfort; skipping Kano and relying on intuition.

**End-of-chapter artifact.** Kano analysis table for the reader's project + initial
prototype scope derived from it.

**Transition.** Into Ch.3 — the seven-stage prototyping workflow that executes within
the Stage-Gate frame.

---

### Chapter 3 — The Prototyping Mindset & the Workflow
**Folder:** `chapters/03-workflow` · **Status:** REDO · **Figures:** 3

**Changes from previous build (was old Ch.2):** Rename folder from `02-workflow` to
`03-workflow`. Add Stage-Gate location opener: "The seven-stage workflow in this chapter
is the work you do inside Stage 2/3 of the Stage-Gate model — between Gate 2 (project
approved) and Gate 3 (proof of concept accepted)." All other content valid; update
chapter number references in cross-references.

**Purpose.** Teach the seven-stage Prototype Development Cycle as the reasoning scaffold
for all subsequent technical chapters.

**Learning objectives.** (1) Walk all seven stages and the iteration loop. (2) Define a
prototype by the question it answers. (3) Choose fidelity deliberately.

**Sections.** 3.1 Prototype = answer to a question or reducer of a risk. 3.2 The seven
stages (one subsection each). 3.3 The controlled iteration loop. 3.4 Prototype types.
3.5 Fidelity matched to the question. 3.6 The documentation layer.

**Required equations.** Illustrative effort vs fidelity; numerical comparison of two
fidelity options in the worked example.

**Required figures (3).**
- `fig_01_workflow` — seven-stage spine with Design↔Validate iteration loop.
- `fig_02_fidelity_ladder` — fidelity rungs vs relative effort/cost.
- `fig_03_value` — intrinsic vs extrinsic value diagram.

**Worked example.** Two prototype options at different fidelities answering the same
question; compare relative effort; argue for the lower-fidelity choice.

**Common pitfalls.** "Prototype = mini-product"; "higher fidelity is always better."

**End-of-chapter artifact.** Statement of the central question the prototype must answer
+ chosen fidelity with justification.

**Transition.** Into Ch.4 — producing the specification and risk register.

---

### Chapter 4 — Specifications & Risk Prioritization
**Folder:** `chapters/04-specifications` · **Status:** REDO · **Figures:** 3

**Changes from previous build:** Folder name unchanged. Add Stage-Gate opener: "This
chapter produces the core deliverable of Stage-Gate Stage 2 (Scoping) — the product
specification and risk register that justify a Go decision at Gate 2." Update chapter
number references. No figures need regeneration.

**Purpose.** Turn an idea into a measurable specification and a defensible risk ranking.

**Learning objectives.** (1) Write measurable, testable requirements. (2) Separate
requirements from design. (3) Build and defend a risk-priority ranking using both
the risk matrix and FMEA RPN.

**Sections.** 4.1 Specification anatomy. 4.2 Requirements vs design. 4.3 Risk-driven
prioritization. 4.4 FMEA and RPN. 4.5 Critical path of unknowns.

**Required equations.**
- $R = P_{\text{failure}} \times C_{\text{consequence}}$.
- $\mathrm{RPN} = S \cdot O \cdot D$.

**Required figures (3).**
- `fig_01_risk_matrix` — probability × consequence grid, grayscale shaded.
- `fig_02_req_vs_design` — requirement vs design statement side-by-side.
- `fig_03_critical_unknowns` — critical path of unknowns diagram.

**Worked example.** Convert a vague wish to a measurable requirement; compute RPN for
three subsystems and rank.

**Common pitfalls.** Unmeasurable criteria; solutions embedded in requirements.

**End-of-chapter artifact.** Specification + risk register + scoping rationale.

**Transition.** Into Ch.5 — decomposing the specification into a system architecture.

---

### Chapter 5 — System Architecture & Interface Definition
**Folder:** `chapters/05-architecture` · **Status:** TODO · **Figures:** 3

**Stage-Gate location.** Stage 2/3 — architectural decisions are the primary technical
work between Gate 2 and Gate 3; a sound architecture is a prerequisite for an honest
Gate 3 business case.

**Purpose.** Decompose the prototype into subsystems and define interfaces before any
building begins. Integration fails at boundaries, not within blocks.

**Learning objectives.** (1) Decompose into subsystems. (2) Specify interface contracts.
(3) Allocate timing, power, and error budgets.

**Sections.** 5.1 Decomposition: electronics, mechanical, firmware, AI/IoT/robotic logic.
5.2 Interfaces as contracts: electrical, mechanical, data, timing. 5.3 Budget allocation.
5.4 Why integration fails at boundaries.

**Required equations.**
- Timing budget: $T_{\text{total}} = \sum_i t_i \le T_{\text{budget}}$.
- Power budget: $P_{\text{total}} = \sum_i P_i$.
- RSS error: $e_{\text{total}} = \sqrt{\sum_i e_i^{\,2}}$.

**Required figures (3).**
- `fig_01_block_diagram` — running-example system block diagram (graphviz).
- `fig_02_interface_budget` — budget allocated across an interface (stacked bar vs limit).
- `fig_03_boundary_failure` — two blocks that work alone but mismatch at the interface.

**Worked example.** Allocate a 5 ms latency budget across three pipeline stages; combine
three measurement errors via RSS.

**Common pitfalls.** Starting a favourite subsystem before interfaces are fixed; informal
"we'll figure it out" interfaces.

**End-of-chapter artifact.** System block diagram + interface table with budgets.

**Transition.** Into Ch.6 — selecting the components that populate this architecture.

---

### Chapter 6 — Component Selection & Datasheet Literacy
**Folder:** `chapters/06-component-selection` · **Status:** TODO · **Figures:** 3

**Stage-Gate location.** Stage 3 (Development) — component selection locks in a large
fraction of unit cost and reliability before a single board is laid out.

**Purpose.** Teach how to choose a component, not just name one. Students know how to
use components; this chapter teaches how to evaluate and select them professionally.

**Learning objectives.** (1) Extract critical parameters from a datasheet. (2) Apply
derating to select components with adequate margin. (3) Evaluate lifecycle status and
supply-chain risk. (4) Develop a second-source strategy.

**Sections.**
- 6.1 Reading a datasheet: absolute maximum ratings, recommended operating conditions,
  electrical characteristics, timing diagrams, application circuits, packaging/footprint.
- 6.2 Derating: never operate at the rated limit; apply derating factors for voltage,
  current, temperature, and power dissipation.
- 6.3 Operating margin: quantifying headroom to a limit.
- 6.4 Component lifecycle status: active, NRND (not recommended for new designs),
  last-time buy, obsolete. Why lifecycle status is a risk register entry.
- 6.5 Second-sourcing strategy: compatible alternates, footprint compatibility,
  parametric equivalence.
- 6.6 Supply chain risk: single-source components, long lead times, allocation periods.
  How to identify and mitigate before the BOM is locked.
- 6.7 MTBF and reliability basics: what the failure rate number on a datasheet means and
  how to use it for simple system reliability estimation.

**Required equations.**
- Derating factor: $D_f = V_{\text{applied}} / V_{\text{rated}}$; design target
  typically $D_f \le 0.8$ for voltage, $D_f \le 0.75$ for capacitors.
- Operating margin: $M = \dfrac{\text{spec limit} - \text{actual value}}{\text{spec limit}} \times 100\%$.
- Series system MTBF:
  $\lambda_{\text{sys}} = \sum_i \lambda_i$, $\quad \mathrm{MTBF}_{\text{sys}} = 1/\lambda_{\text{sys}}$.
- Parallel (redundant) reliability:
  $R_{\text{sys}} = 1 - \prod_i (1 - R_i)$.

**Required figures (3).**
- `fig_01_datasheet_anatomy` — annotated datasheet page excerpt (drawn, not scanned)
  highlighting the four key zones: abs max, recommended operating, characteristics,
  timing.
- `fig_02_derating_curve` — component stress vs derating factor; failure rate vs
  applied/rated ratio showing the knee of the curve.
- `fig_03_lifecycle` — component lifecycle timeline (active → NRND → LTB → obsolete)
  with risk implication annotations.

**Worked example.** A microcontroller running at 3.3 V supply, 85°C ambient: compute
$D_f$ for supply voltage and junction temperature; compute operating margin on a timing
parameter; look up the lifecycle status of a hypothetical component; identify an
alternate; estimate system MTBF for a three-component critical path.

**In Practice.** A prototype built on a component that entered NRND six months after
design freeze; the redesign cost exceeded the original prototype budget.

**Common pitfalls.** Operating at absolute maximum ratings; ignoring lifecycle status;
no second source identified; accepting a component because it "works in the lab" without
checking derating.

**End-of-chapter artifact.** Component selection table (critical components): part
number, $D_f$, margin, lifecycle status, alternate part, supply-chain risk note.

**Transition.** Into Ch.7 — designing the assembly and manufacturing process around the
components you have chosen.

---

### Chapter 7 — Design for X
**Folder:** `chapters/07-dfx` · **Status:** TODO · **Figures:** 3

**Stage-Gate location.** Stage 3 (Development) — DFX decisions made here determine
~70–80% of manufacturing cost and assembly quality before a single prototype is built.

**Purpose.** Teach students to design with the downstream process in mind. DFX is not
a post-design checklist; it is a design-time discipline.

**Learning objectives.** (1) Apply DFM principles to reduce unit cost. (2) Use DFA
metrics to simplify assembly. (3) Design for testability to enable efficient validation.
(4) Consider reliability as a design parameter.

**Sections.**
- 7.1 What DFX means: designing with the downstream in mind. Overview of DFM, DFA,
  DFT, DFR and how they interrelate.
- 7.2 Design for Manufacturability (DFM): standard processes, tolerances, materials,
  surface finishes; avoid exotic geometries; PCB DFM (trace width, via size, panelisation,
  solder mask, silkscreen); 3D-print DFM (wall thickness, overhang, support structure,
  orientation).
- 7.3 Design for Assembly (DFA): minimise part count; use standard fasteners; design
  for one-directional assembly; the Boothroyd-Dewhurst theoretical minimum parts
  criterion.
- 7.4 Design for Test (DFT): test points, JTAG/SWD access, LED indicators, UART
  debug ports, built-in self-test (BIST). Designing observability and controllability
  into the prototype.
- 7.5 Design for Reliability (DFR): derating (link to Ch.6), redundancy, FMEA-driven
  design margin, thermal management.
- 7.6 Practical DFX trade-offs: DFM may conflict with DFA; optimise for the dominant
  cost driver at your production volume.

**Required equations.**
- DFA assembly efficiency (Boothroyd-Dewhurst):
  $\eta_A = \dfrac{N_{\text{min}} \cdot t_{\text{ideal}}}{t_{\text{actual}}}$
  where $N_{\text{min}}$ is the theoretical minimum part count and $t_{\text{ideal}}$
  is the ideal assembly time per part (typically 3 s).
- DFM cost impact (simplified): relative unit cost savings from part-count reduction:
  $\Delta C \approx \Delta N_{\text{parts}} \cdot \bar{c}_{\text{part}} + \Delta N_{\text{ops}} \cdot \bar{c}_{\text{op}}$.
- DFT defect coverage: $\mathrm{DPMO} = \dfrac{D}{N \cdot O} \times 10^6$
  where $D$ = defects observed, $N$ = units, $O$ = opportunities per unit.

**Required figures (3).**
- `fig_01_dfx_overview` — DFM/DFA/DFT/DFR as four overlapping domains feeding into
  the prototype (Venn-style, grayscale).
- `fig_02_dfa_parts` — before/after part-count reduction example with assembly steps.
- `fig_03_dft_testpoints` — schematic fragment showing test points, debug header, and
  BIST output on a PCB.

**Worked example.** A subassembly with 8 parts and 120 s assembly time: compute
$\eta_A$; identify two parts that can be eliminated (fail the Boothroyd-Dewhurst
keep/eliminate test); recompute $\eta_A$; estimate the assembly cost saving per unit
at 500 units using $\bar{c}_{\text{op}} = \$0.10/$s.

**In Practice.** A prototype with no test points: the validation team spent 3 days
probing unmarked pads with a clip lead to find a firmware bug that a UART debug port
would have exposed in 20 minutes.

**Common pitfalls.** Treating DFX as a post-design review; DFM/DFA applied only at
production volumes (they matter at prototype volume too); no test points because "we
can always probe the board."

**End-of-chapter artifact.** DFX review checklist for the reader's prototype design,
with $\eta_A$ computed and three DFT features explicitly designed in.

**Transition.** Into Ch.8 — using AI tools within the design process you have just
disciplined.

---

### Chapter 8 — AI in Prototyping: Capability & Risk
**Folder:** `chapters/08-ai` · **Status:** TODO · **Figures:** 2

**Stage-Gate location.** Stage 3 (Development) — AI tools accelerate design work inside
Stage 3, but their outputs must be verified before they become Gate 3 evidence.

**Purpose.** Use AI as a design accelerator while keeping the engineer accountable for
every output. Scope is strictly AI in the *design and prototyping process* — code
generation, schematic suggestion, design-space exploration, documentation. AI as a
*system component* (inference engines, ML models) is covered in Ch.9.

**Learning objectives.** (1) Identify where AI genuinely helps in prototyping. (2) Verify
every AI output against first principles. (3) Manage IP and reproducibility risk.

**Sections.**
- 8.1 Where AI helps: scaffolding firmware, generating boilerplate, suggesting component
  values, exploring design alternatives, generating documentation drafts.
- 8.2 Accelerator, not autonomous designer: the engineer remains accountable.
- 8.3 Hallucination in engineering context: AI output that is plausible but electrically,
  mechanically, or logically wrong; the human-in-the-loop verification loop.
- 8.4 The black-box problem: validate AI suggestions via simulation, bench test, or
  first-principles analysis — never deploy unverified AI output to safety-relevant
  functions.
- 8.5 IP and data-leakage risk: what happens to proprietary schematics and firmware
  submitted to public AI tools; confidentiality obligations to employers and clients.
- 8.6 Reproducibility and traceability: documenting where AI was used, what it produced,
  and how it was verified — required for a defensible Gate 3 submission.

**Required equations.**
- Expected cost of an unverified error:
  $\mathbb{E}[C_{\text{err}}] = p_{\text{err}} \cdot C_{\text{consequence}}$
  used to justify verification investment.

**Required figures (2).**
- `fig_01_hitl_loop` — human-in-the-loop verification cycle: AI proposes → engineer
  verifies → accept or reject → document.
- `fig_02_trust_matrix` — what AI output can be used directly vs what requires
  independent verification (grayscale quadrant matrix).

**Worked example.** An AI-suggested pull-up resistor value with a stated error
probability and consequence cost; compute $\mathbb{E}[C_{\text{err}}]$; decide whether
the cost of bench verification is justified.

**Common pitfalls.** Trusting plausible output without verification; submitting
confidential design data to public tools; no record of AI involvement in a design.

**End-of-chapter artifact.** AI use log entries: tool used, output produced, verification
method, result.

**Transition.** Into Ch.9 — IoT connectivity, robotics, and the safety and security
design obligations specific to connected and moving systems.

---

### Chapter 9 — IoT, Robotics & Safety as a Design Obligation
**Folder:** `chapters/09-iot-robotics` · **Status:** TODO · **Figures:** 3

**Stage-Gate location.** Stage 3 (Development) — security and safety requirements that
are not designed in here will fail at Gate 4 (Testing & Validation) and are expensive
to retrofit.

**Purpose.** Build security and physical safety into the design at Stage 3. These are
design requirements, not post-build additions.

**Learning objectives.** (1) Design IoT security in from the start. (2) Size a power and
battery budget for a connected device. (3) Specify robotic safety design parameters.

**Sections.**
- 9.1 IoT security by design: encryption, authentication, secure protocols; the cost of
  retrofitting security vs designing it in.
- 9.2 Attack surfaces: connectivity layer, communication layer, management layer.
- 9.3 Privacy and data obligations: what sensor data triggers compliance requirements.
- 9.4 Protocol selection: MQTT, CoAP, BLE — each choice has security, power, and
  interoperability consequences.
- 9.5 Power and battery budgeting: duty-cycle analysis for connected devices.
- 9.6 Robotics physical safety: e-stops, guarding, fail-safe states, force/speed limits,
  human-robot interaction zones.
- 9.7 Absorbed safety practice: EMC and ESD design, PPE requirements in the lab,
  applicable health-and-safety law — designed in at Stage 3.

**Required equations.**
- Average current:
  $I_{\text{avg}} = D\,I_{\text{active}} + (1-D)\,I_{\text{sleep}}$.
- Battery life:
  $t_{\text{life}} = C_{\text{batt}} / I_{\text{avg}}$ (mAh / mA = hours).
- Mechanical safety factor:
  $\mathrm{SF} = \text{capacity} / \text{applied load}$.

**Required figures (3).**
- `fig_01_attack_surface` — layered IoT architecture with the three attack surfaces.
- `fig_02_power_budget` — duty-cycled current profile with $I_{\text{avg}}$ and battery
  life annotation.
- `fig_03_robot_safety` — robot workspace with safety zones, guarding, and e-stop in the
  control path.

**Worked example.** Sensor node: $I_{\text{active}}=80$ mA, $I_{\text{sleep}}=0.05$ mA,
$D=2\%$, $C_{\text{batt}}=2000$ mAh. Compute $I_{\text{avg}}$ and $t_{\text{life}}$;
show how halving $D$ nearly doubles life.

**Common pitfalls.** "Add security later"; default credentials shipped; no e-stop on
a moving prototype; EMC treated as a compliance problem rather than a design problem.

**End-of-chapter artifact.** Updated design records with security, power budget, and
safety design decisions explicitly documented.

**Transition.** Into Ch.10 — managing the schedule and plan for the build.

---

### Chapter 10 — Planning & Schedule Management
**Folder:** `chapters/10-planning` · **Status:** TODO · **Figures:** 3

**Stage-Gate location.** Stage 3 (Development) — the project schedule and risk register
are Gate 3 deliverables; an unrealistic schedule is a gate failure before the prototype
is even built.

**Purpose.** Build and maintain a realistic schedule with a critical path, treating lead
times and procurement as first-class planning risks.

**Learning objectives.** (1) Build a WBS and identify the critical path. (2) Estimate
durations under uncertainty using PERT. (3) Maintain a living risk register.

**Sections.** 10.1 Work breakdown structure. 10.2 Dependencies and critical path.
10.3 Gantt scheduling. 10.4 PERT three-point estimation. 10.5 Lead time as a planning
risk. 10.6 Maintaining the risk register.

**Required equations.**
- CPM slack: $\text{slack} = \mathrm{LS} - \mathrm{ES} = \mathrm{LF} - \mathrm{EF}$.
- Critical path: all activities with zero slack.
- PERT expected duration: $t_e = (a + 4m + b)/6$.
- PERT standard deviation: $\sigma = (b - a)/6$.

**Required figures (3).**
- `fig_01_gantt` — Gantt of the running example (grayscale bars, milestones as markers).
- `fig_02_cpm_network` — activity-on-node network with critical path bolded.
- `fig_03_pert_dist` — three-point estimate (a, m, b) with $t_e$ and $\sigma$ annotated.

**Worked example.** A 6-activity network: compute ES/EF/LS/LF, slack, critical path;
compute $t_e$ and $\sigma$ from $(a,m,b) = (3,5,10)$ days.

**Common pitfalls.** Gantt made once and never updated; component lead times not
scheduled; confusing the critical path with the longest task.

**End-of-chapter artifact.** Gantt chart + updated risk register.

**Transition.** Into Ch.11 — the bill of materials and procurement chain.

---

### Chapter 11 — Bill of Materials & Procurement
**Folder:** `chapters/11-bom-procurement` · **Status:** TODO · **Figures:** 3

**Stage-Gate location.** Stage 3 (Development) — the BOM is a Gate 3 deliverable; an
uncosted or incomplete BOM cannot support the business case.

**Purpose.** Produce a complete, costed, multi-level BOM and operate the full
procurement document chain from BOM to reconciliation.

**Learning objectives.** (1) Build a multi-level costed BOM. (2) Derive a purchase list
and compare quotes. (3) Manage the PO → receipt/invoice → reconciliation chain.

**Sections.** 11.1 BOM as a design document. 11.2 Purchase list from BOM. 11.3 Quotes.
11.4 Purchase orders. 11.5 Receipt vs invoice. 11.6 Reconciliation and as-built BOM.

**Required equations.**
- Extended cost: $\text{ext}_i = q_i \cdot u_i$.
- BOM total: $C_{\text{BOM}} = \sum_i q_i u_i$.
- Order quantity with overage: $q_i^{\text{order}} = \lceil (1+\alpha)\,q_i \rceil$.

**Required figures (3).**
- `fig_01_doc_chain` — BOM → purchase list → quote → PO → receipt/invoice →
  reconciliation flow.
- `fig_02_bom_tree` — multi-level BOM tree.
- `fig_03_cost_rollup` — BOM cost rollup by subsystem (stacked grayscale bars).

**Worked example.** An 8-line BOM: extended costs, 10% overage on consumables,
$C_{\text{BOM}}$ total; compare two supplier quotes on price and lead time.

**Common pitfalls.** BOM as an afterthought; no alternates; wrong footprint from a
missing designator.

**End-of-chapter artifact.** Costed BOM + purchase list + procurement records.

**Transition.** Into Ch.12 — the economics that the BOM cost implies at production
volume.

---

### Chapter 12 — Low-Volume Production Economics
**Folder:** `chapters/12-economics` · **Status:** TODO · **Figures:** 3

**Stage-Gate location.** The cost projection produced here is a primary Gate 3
deliverable — it is the economic half of the go/kill decision.

**Purpose.** Explain why per-unit cost falls with volume, how design decisions lock in
cost, and how to project production economics from a prototype BOM.

**Learning objectives.** (1) Compute and plot the unit-cost curve. (2) Find the break-
even volume between two production processes. (3) Connect design decisions to downstream
manufacturing cost.

**Sections.** 12.1 Why low-volume/bridge production exists. 12.2 Fixed vs variable cost.
12.3 The unit-cost curve. 12.4 Process break-even. 12.5 DFM/DFA and the design-locks-
cost principle (link back to Ch.7). 12.6 Failure economics.

**Required equations.**
- $C_{\text{unit}}(N) = C_{\text{fixed}}/N + c_{\text{var}}$.
- Process break-even: solve
  $C_{f1}/N^\ast + c_{v1} = C_{f2}/N^\ast + c_{v2}$ for $N^\ast =
  (C_{f2}-C_{f1})/(c_{v1}-c_{v2})$.

**Required figures (3).**
- `fig_01_unit_cost_curve` — $C_{\text{unit}}$ vs $N$ (hyperbola → asymptote).
- `fig_02_breakeven` — two processes crossing at $N^\ast$.
- `fig_03_cost_committed` — cost committed vs cost incurred over project phases.

**Worked example.** $C_{\text{fixed}}=\$8{,}000$, $c_{\text{var}}=\$12$: tabulate
$C_{\text{unit}}$ at $N=1,50,500$; find $N^\ast$ between 3D-printing ($C_f=0$,
$c_v=\$40$) and injection moulding ($C_f=\$8{,}000$, $c_v=\$6$).

**Common pitfalls.** Assuming prototype unit cost = production unit cost.

**End-of-chapter artifact.** Preliminary cost analysis with $C_{\text{unit}}$ at three
volumes (feeds Ch.17).

**Transition.** Into Ch.13 — managing design history and version control.

---

### Chapter 13 — Version Control & Design History
**Folder:** `chapters/13-version-control` · **Status:** TODO · **Figures:** 3

**Stage-Gate location.** Stage 3 (Development) and a Gate 3 requirement — a design
without a traceable history cannot be handed off, reproduced, or certified.

**Purpose.** Establish version control and design history as non-negotiable professional
practice. Students know git for software; this chapter extends that discipline to all
design artifacts.

**Learning objectives.** (1) Apply version control to firmware, schematics, and CAD.
(2) Write meaningful commit messages and manage branches. (3) Understand the Design
History File (DHF) concept and its role in product development.

**Sections.**
- 13.1 Why version control matters for hardware: a change to a schematic without a
  record is indistinguishable from an error. The principle that design history is design
  evidence.
- 13.2 Git for firmware: commit discipline, branching strategy (main/develop/feature),
  tagging releases (v0.1-proto, v1.0-gate3), meaningful commit messages.
- 13.3 Version control for design files: EDA tools (schematic/PCB), CAD (Fusion 360
  version history, STEP export as a version artifact), managing binary files in git
  (LFS).
- 13.4 The Design History File (DHF): the DHF is the auditable record of all design
  decisions, changes, approvals, and test results. It is what a regulatory body or a
  new engineer asks for. In this course the portfolio IS the DHF.
- 13.5 Change management: engineering change order (ECO) concept; when an informal
  change is acceptable vs when it requires a formal record.
- 13.6 Practical tooling: git, git-lfs, GitHub/GitLab; KiCad git integration; Fusion
  360 version history; keeping the DHF in the repo.

**Required equations.** No heavy arithmetic; the content is procedural and structural.
Present one illustrative diagram-based example of a version tree with a hotfix branch
and show how the commit log constitutes a recoverable history.

**Required figures (3).**
- `fig_01_git_flow` — branch/merge diagram (main, develop, feature, hotfix) labelled
  with prototype milestones.
- `fig_02_dhf_structure` — DHF as a tree of design records, test records, and approval
  records feeding into the Gate document.
- `fig_03_eco_flow` — engineering change order decision flow: informal fix vs formal ECO.

**Worked example.** A three-week snapshot of the running example's git log: five commits
with meaningful messages, one branch for a subsystem experiment, one tag at the design
review milestone. Show how to reconstruct the design state at any commit.

**In Practice.** A team that made a last-minute resistor value change without recording
it; the prototype passed testing, went to Gate 3, and the reviewer asked why the BOM
differed from the schematic. No one could answer.

**Common pitfalls.** Committing binary blobs without LFS; "WIP" as a commit message;
treating git as a backup tool rather than a history tool; skipping the DHF because
"we'll remember."

**End-of-chapter artifact.** Git repository for the reader's project with a commit log
covering the design period; a DHF index page linking design records to the repo.

**Transition.** Into Ch.14 — validating the design you have just rigorously documented.

---

### Chapter 14 — Validation & Test Procedure Design
**Folder:** `chapters/14-validation` · **Status:** TODO · **Figures:** 4

**Stage-Gate location.** Stage 4 (Testing & Validation) — this chapter IS Stage 4. Test
results produced here are the primary Gate 4 deliverable.

**Purpose.** Test against criteria defined in advance; collect and interpret performance
data; use failure analysis to anticipate what will break before it breaks.

**Learning objectives.** (1) Write test procedures before testing. (2) Tie acceptance
criteria to the specification. (3) Quantify results against spec using basic statistics.
(4) Use fault trees to anticipate failure modes before running a test.

**Sections.**
- 14.1 Procedures written in advance: the test plan structure.
- 14.2 Acceptance criteria traced to specification: traceability matrix.
- 14.3 Functional demonstration vs quantitative performance data.
- 14.4 Measurement, tolerance, and margin.
- 14.5 Basic statistics for pass/fail with variation.
- 14.6 Failure analysis as a design tool: fault tree analysis (FTA) applied proactively
  before testing; common failure modes for electronics (solder joints, ESD, decoupling)
  and 3D-printed/mechanical assemblies (layer delamination, fit/clearance, fatigue);
  using FTA output to write better test procedures and prioritise test effort.
- 14.7 The documented iteration decision: evidence → decision → scoped change.

**Required equations.**
- $\bar{x} = \frac{1}{n}\sum x_i$;
  $s = \sqrt{\frac{1}{n-1}\sum(x_i-\bar{x})^2}$.
- Margin to limit: $z = (\mathrm{USL} - \bar{x})/s$.
- Process capability: $C_p = (\mathrm{USL}-\mathrm{LSL})/(6\sigma)$.
- FTA OR gate: $P(\text{top}) = 1 - \prod_i (1-P_i)$.
- FTA AND gate: $P(\text{top}) = \prod_i P_i$.

**Required figures (4).**
- `fig_01_test_flow` — test procedure flow (setup → measure → record → pass/fail →
  iterate).
- `fig_02_tolerance_band` — measured values against tolerance band with margin $z$.
- `fig_03_distribution` — distribution with LSL/USL and $\bar{x} \pm Ns$.
- `fig_04_fault_tree` — a simple fault tree for the running example (2 levels, mix of
  OR and AND gates) with probabilities propagated to the top event.

**Worked example.** Part A: ten measurements, compute $\bar{x}$, $s$, $z$, $C_p$,
pass/fail decision. Part B: a three-basic-event fault tree; one OR gate, one AND gate;
compute $P(\text{top event})$; identify the highest-priority test from the result.

**Common pitfalls.** Tests written to confirm success; testing after the fact; ignoring
variation; building the fault tree after the failure occurs instead of before.

**End-of-chapter artifact.** Test procedure + raw data table + fault tree for critical
subsystems + iteration decision memo.

**Transition.** Into Ch.15 — protecting what you have just proven.

---

### Chapter 15 — Intellectual Property Basics
**Folder:** `chapters/15-ip` · **Status:** TODO · **Figures:** 2
**Target length:** ~2,000 words (shorter chapter by design).

**Stage-Gate location.** IP is relevant at every gate — at Gate 2 (does our concept
infringe existing patents?), Gate 3 (should we file before disclosing?), and Gate 4
(is our IP strategy part of the business case?).

**Purpose.** Give technicians the professional literacy to understand who owns what they
build, what obligations they have, and when to ask for legal guidance.

**Learning objectives.** (1) Distinguish the main types of IP protection. (2) Understand
IP assignment in an employment context. (3) Recognise when an NDA applies. (4) Know
when to ask a lawyer.

**Sections.**
- 15.1 Why IP matters to technicians: the prototype you build may be the most valuable
  thing your employer owns. Understanding IP is not optional professional knowledge.
- 15.2 Types of IP protection:
  - *Patents* (utility, design): what they protect, how long, public disclosure trade-off.
  - *Trade secrets*: protection through confidentiality rather than registration;
    indefinite if maintained.
  - *Copyright*: automatic; applies to firmware, documentation, and design files.
  - *Trademarks*: names and marks; less relevant at the prototype stage.
- 15.3 IP ownership in employment: in most jurisdictions, IP created during employment
  in the scope of your job belongs to the employer. Understand your employment contract.
- 15.4 NDAs: non-disclosure agreements before showing a prototype to a supplier,
  customer, or investor. What they cover and what they don't.
- 15.5 IP assignment agreements: when you do contract work or build a prototype for a
  client, the contract determines ownership. Know before you build.
- 15.6 The prior-art check: a basic patent search before committing to a design direction
  is standard professional practice. Tools and approach.
- 15.7 When to ask a lawyer: recognise the boundary between professional literacy and
  legal advice. The purpose of this chapter is the former.

**Required equations.** None. The content is conceptual and procedural.

**Required figures (2).**
- `fig_01_ip_types` — comparison table/matrix of IP types: protection mechanism,
  duration, registration required, disclosure trade-off.
- `fig_02_ip_timeline` — when each IP consideration arises across the Stage-Gate
  model (concept → Gate 2 → Gate 3 → launch).

**Worked example.** The running-example product: identify what could be protected by
patent, what is best protected as a trade secret, what is automatically copyrighted, and
what the team should do before showing the prototype at a trade show.

**Common pitfalls.** Publicly disclosing a concept before filing a provisional patent;
assuming employer-provided tools mean employer-owns-nothing; skipping the NDA because
the supplier "seems trustworthy."

**End-of-chapter artifact.** An IP checklist for the reader's project: potential
protectable elements, ownership assignment, NDA requirement, prior-art search status.

**Transition.** Into Ch.16 — compiling the evidence into a portfolio that can support
a Gate 3/4 submission.

---

### Chapter 16 — Documentation & Portfolio Assembly
**Folder:** `chapters/16-documentation` · **Status:** TODO · **Figures:** 3
**Target length:** ~1,500–2,000 words (intentionally short — documentation practice is
already woven through every preceding chapter).

**Stage-Gate location.** Gate 3/4 submission — the portfolio IS the gate deliverable.
This chapter teaches assembly, not documentation (which has already happened).

**Purpose.** Compile existing artifacts into a coherent, traceable portfolio. Introduce
the as-built BOM and traceability coverage as the two quantitative completeness checks.

**Learning objectives.** (1) Assemble a portfolio from existing stage artifacts.
(2) Produce and reconcile an as-built BOM. (3) Compute and close traceability coverage.

**Sections.**
- 16.1 The three documentation principles (brief restatement): record decisions not
  outcomes; enable reproduction; documentation debt compounds.
- 16.2 Compiling, not writing: the portfolio is assembled from artifacts produced at
  each stage. If a section must be written from memory, the process broke down earlier.
- 16.3 Portfolio structure: map each section to its source artifact.
- 16.4 The as-built BOM: reconcile against the design BOM; every deviation is a
  documented decision.
- 16.5 Traceability coverage: count requirements with a linked test; close gaps before
  submission.

**Required equations.**
- $\mathrm{coverage} = \dfrac{\text{requirements with linked test}}{\text{total requirements}} \times 100\%$; target 100%.

**Required figures (3).**
- `fig_01_doc_parallel` — documentation layer parallel to the seven stages with artifact
  tags per stage.
- `fig_02_traceability` — requirement → design element → test case matrix.
- `fig_03_portfolio_map` — portfolio sections mapped to their source stage artifacts.

**Worked example.** Compute traceability coverage for the running example; identify one
untested requirement; show the as-built BOM reconciliation for two line items that
changed.

**Common pitfalls.** Writing the portfolio from memory; as-built BOM never reconciled;
100% coverage assumed without checking.

**End-of-chapter artifact.** Draft portfolio + as-built BOM + traceability matrix with
coverage percentage.

**Transition.** Into Ch.17 — the closing cost analysis and the case for Gate 3.

---

### Chapter 17 — Cost Analysis & the Bridge to Project II
**Folder:** `chapters/17-cost-bridge` · **Status:** TODO · **Figures:** 3
**Milestone 3: Final Portfolio & Gate 3 submission.**

**Stage-Gate location.** Gate 3 (Go to Development / Go to Project II) — this chapter
produces the economic component of the Gate 3 deliverable.

**Purpose.** Project production economics from the validated prototype; state what was
proven and what remains; frame readiness for Project II (Stage-Gate Stage 3/4).

**Learning objectives.** (1) Project unit cost at three volumes from the prototype BOM.
(2) Compute break-even and margin at a target price. (3) Articulate Gate 3 readiness.

**Sections.** 17.1 Applying the cost model to the finished prototype. 17.2 Prototype
cost vs projected production cost. 17.3 Break-even and margin. 17.4 Extrinsic value
and Gate 3 readiness. 17.5 Lessons learned. 17.6 The handoff to Project II.

**Required equations.**
- $C_{\text{unit}}(N)$ reused.
- $N_{\text{be}} = C_{\text{fixed}} / (p - c_{\text{var}})$.
- Total profit: $\Pi(N) = N(p - c_{\text{var}}) - C_{\text{fixed}}$.

**Required figures (3).**
- `fig_01_cost_projection` — $C_{\text{unit}}$ at $N=1,50,500$ for the running example.
- `fig_02_proto_vs_prod` — prototype cost vs projected production cost (paired bars).
- `fig_03_gate3_readiness` — what Project I delivers vs what Project II must resolve.

**Worked example.** Full projection with the running example's numbers; compute
$N_{\text{be}}$, margin at $N=500$, $\Pi(500)$; write a two-sentence Gate 3 readiness
statement.

**Common pitfalls.** "It works" = "ready to produce"; negative economic finding = failure.

**End-of-chapter artifact.** Final portfolio with production cost projection, Gate 3
readiness statement, and lessons learned.

**Transition.** Forward to Project II — the prototype becomes a product.

---

### Course Plan — 12-Week Course Plan Document
**Folder:** `courseplan/` · **Status:** TODO · **Build after Ch.17**

**Purpose.** A standalone Sparkle document — separate from the textbook — that maps
the 12-week course to Stage-Gate phases, theory topics, lab activities, milestones, and
assessment weights. Used by the instructor as the authoritative course plan.

**Document structure (generate as `courseplan/courseplan.tex`).**
- Title page via Sparkle metadata.
- §1 Course overview: one paragraph situating the course within the Stage-Gate model
  (Stage 2/3, Gate 3 outcome).
- §2 Twelve-week theory and practice map: a full-page table with columns:
  Week | Stage-Gate Phase | Theory Topic (chapter ref) | Lab Activity | Artifact Due.
- §3 Three milestones with descriptions and assessment weights:
  - Milestone 1 (Week 3/4): Proposal + Kano analysis + risk register — 15%
  - Milestone 2 (Week 9/10): Design review + alpha prototype + DFX review — 20%
  - Milestone 3 (Week 12): Final portfolio + Gate 3 submission — 65%
- §4 Assessment criteria summary (one paragraph per milestone).
- §5 SPLI note: minimum 10% of any written/oral work assessed on professional English.

**Required figures (2).**
- `fig_01_stagegate_course` — Stage-Gate funnel with the 12-week course shaded inside
  Stage 2/3; Gate 2 at the left edge, Gate 3 at the right.
- `fig_02_milestone_timeline` — Gantt-style timeline across 12 weeks with theory track,
  lab track, and three milestones marked.

**Week-by-week map (use to populate §2 table).**

| Week | Stage-Gate Phase | Theory (Chapter) | Lab | Artifact |
|------|-----------------|------------------|-----|----------|
| 1 | Stage 2 — Scoping | Ch.1 Overview; Ch.2 Stage-Gate/Kano | Project brief issued; Kano survey | Project context brief |
| 2 | Stage 2 | Ch.3 Workflow; Ch.4 Specifications | Risk matrix workshop | Kano analysis + scope |
| 3 | Stage 2 | Ch.4 Specifications cont. | Proposal writing lab | |
| 4 | Gate 2 / Stage 3 start | Ch.5 Architecture | Architecture workshop | **Milestone 1** |
| 5 | Stage 3 — Development | Ch.6 Component selection | Component selection lab; BOM start | Component selection table |
| 6 | Stage 3 | Ch.7 Design for X | DFX review workshop | DFX checklist |
| 7 | Stage 3 | Ch.8 AI; Ch.9 IoT/Robotics/Safety | Design lab — subsystem design | AI use log; safety records |
| 8 | Stage 3 | Ch.10 Planning; Ch.11 BOM | Procurement lab; Gantt | BOM + Gantt |
| 9 | Stage 3 | Ch.12 Economics | Cost analysis lab | |
| 10 | Gate 3 approach | Ch.13 Version Control | Build lab; git repo setup | **Milestone 2** |
| 11 | Stage 4 — Testing | Ch.14 Validation | Test procedure lab; fault tree | Test procedure + FTA |
| 12 | Gate 3 | Ch.15 IP; Ch.16 Documentation; Ch.17 Cost | Portfolio assembly; Gate 3 prep | **Milestone 3** |

**Compile separately** using:
```bash
cd courseplan
pdflatex courseplan.tex
pdflatex courseplan.tex
```

---

## 12. RUNNING-EXAMPLE STATE *(Claude Code updates this as chapters advance it)*

**Product:** A **connected (IoT) robotic sorting subsystem** — a sensor-guided actuator
that classifies and diverts items on a bench conveyor, reports status over a network,
and is designed as a module within a larger automation product. Exercises all reader
skill areas: PCB + embedded firmware + mechanical/3D-printed parts + AI inference +
IoT connectivity + moving robotic element requiring safety design.

| Field | Value | Set in |
|-------|-------|--------|
| Business model | *(set in Ch.1)* | Ch.1 |
| Firm context | *(set in Ch.1)* | Ch.1 |
| Kano feature classification | *(set in Ch.2)* | Ch.2 |
| Prototype scope (from Kano) | *(set in Ch.2)* | Ch.2 |
| Central question the prototype answers | *(set in Ch.3)* | Ch.3 |
| Chosen fidelity | *(set in Ch.3)* | Ch.3 |
| Specification + RPN ranking | *(set in Ch.4)* | Ch.4 |
| Architecture + interface budgets | *(set in Ch.5)* | Ch.5 |
| Critical component selection (derating, lifecycle) | *(set in Ch.6)* | Ch.6 |
| DFX checklist + $\eta_A$ | *(set in Ch.7)* | Ch.7 |
| Power/battery numbers | *(set in Ch.9)* | Ch.9 |
| Schedule — key activities, critical path | *(set in Ch.10)* | Ch.10 |
| BOM totals and $C_{\text{fixed}}$, $c_{\text{var}}$ | *(set in Ch.11–12)* | Ch.11–12 |
| Target price $p$ | *(set in Ch.12)* | Ch.12 |
| Validation results + FTA top-event probability | *(set in Ch.14)* | Ch.14 |
| IP checklist | *(set in Ch.15)* | Ch.15 |

**Consistency rule:** $C_{\text{fixed}}$, $c_{\text{var}}$, and $p$ set in Ch.11–12
must be reused unchanged in Ch.17. Lock these values in Ch.11 and record them here.

---

## 13. DEFINITION OF DONE (per chapter)

- [ ] Folder + `images/` created (or renamed per §3 for REDO chapters).
- [ ] All required figures: vector PDF + 200 dpi PNG proof viewed and verified clean.
- [ ] `chapter.tex`: Stage-Gate opener, objectives, all sections, all equations with
      worked arithmetic, In Practice callout(s), Common Pitfalls, artifact, summary,
      transition.
- [ ] Every figure referenced in text before it appears; captions are full sentences.
- [ ] `\index{}` on every bold-first-use term.
- [ ] Build-State Table (§2) updated to `DONE`.
- [ ] Running-Example State (§12) updated if advanced.
- [ ] Stopped for review; next chapter NOT started.
