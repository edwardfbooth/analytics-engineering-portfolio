# analytics-engineering-portfolio

Portfolio repository documenting a self-directed transition from BI/Analytics Tech Lead into Analytics Engineering, built in public one commit at a time rather than written up after the fact.

## Background

4 years as a BI/Analytics Tech Lead in retail: Python, SQL, Power BI, Excel, intermediate data modeling. This repository tracks the technical foundation build required to move into an Analytics Engineering role internationally.

Path evaluation and scoring methodology live outside this repo; this README covers execution only.

## Roadmap

~4 hours/week, ~190 hours over 12 months.

| Phase | Topic | Status | Repo |
|---|---|---|---|
| 0 | Git + Linux/CLI fundamentals | In progress | this repo |
| 1 | Python for data (scripting, pandas, pytest) | Not started | this repo |
| 2 | SQL optimization + advanced data modeling | Not started | this repo |
| 3 | dbt + cloud data warehouse (Snowflake or BigQuery) | Not started | pipeline repo (link added on completion) |
| 4 | APIs and ingestion patterns | Not started | pipeline repo |
| 5 | Orchestration fundamentals (Airflow or Dagster) | Not started | pipeline repo |
| 6 | Docker + CI/CD (GitHub Actions) | Not started | pipeline repo |
| 7 | Cloud fundamentals certification | Not started | n/a (certification, no repo) |
| 8 | Portfolio consolidation | Not started | this repo (README + links) |
| Elective | LLM/RAG project (month 9-10) | Not started | separate repo (link added on completion) |

**Repo policy:** Phases 0-2 are foundational exercises and stay here. Starting Phase 3, the dbt project is substantial enough to stand alone, so it spins into its own repo and gets extended in place through Phases 4-6 (ingestion, orchestration, containerization), becoming the flagship artifact. The elective LLM/RAG project is a distinct story, not an extension of the pipeline, so it gets its own repo rather than folding into either. This repo stays the hub: roadmap, status, and links to both once they exist.

## Structure

    scripts/           Placeholder for Phase 1 Python scripts
    .gitignore         Python and OS artifacts excluded from tracking
    .gitattributes     Enforces LF line endings repo-wide
    README.md          This file

This repo covers Phases 0-2 and the final capstone. From Phase 3 onward, work lands in separate repos per the policy above, linked here as each one goes live.

## Setup

Clone via SSH:

    git clone git@github.com:edwardfbooth/analytics-engineering-portfolio.git

No dependencies yet. Python environment setup lands alongside the first scripts in Phase 1.

## Usage

Currently a learning log covering Phase 0 (Git and Linux fundamentals). Commit history and pull requests are the evidence of work here, not a runnable tool yet. That changes in Phase 1, when working Python scripts land in `/scripts`.