# IMHOTEP research pilot v0.1

Independent preparatory research by Eric Smith / Contrivance Company Chicago.
Intended for discussion with Northwestern SPS advisors; not an approved Northwestern study, admission, affiliation, or thesis.

## Research question
How does retrieval method affect accuracy and response time when finding intake and appointment information in simulated medical secretary workflows?

## Scope
Use fictional records only. Never copy patient records, clinic exports, credentials, or real contact information into this directory.
This pilot evaluates information retrieval, not diagnosis, treatment, clinical effectiveness, or health disparities.

## Study design
1. Build 50 fictional cases and an answer key with query ID, case ID, relevant document IDs, task type, and development/test split.
2. Include exact wording, paraphrases, similar records, and missing-information questions.
3. Reserve 10 cases for development and 40 for held-out evaluation. Split by case before tuning; keep all related documents and queries in that case's split.
4. Freeze cases and scoring rules before the final evaluation. Have a second reviewer check relevance labels.
5. Compare a token-overlap keyword baseline with IMHOTEP/XERJ on the same corpus, patient scope, and questions. Record actual returned document IDs; never substitute a second baseline and call it XERJ.
6. Repeat timing runs with fixed hardware and explicit warm/cold-cache conditions. Compare retrieval-only latency separately from indexing or generated-answer time.

## Outcomes
Primary: top-1 accuracy on answerable queries.
Secondary: recall@3 (relevant documents retrieved / all relevant documents), reciprocal rank, median and p95 latency, and wrong-case retrieval frequency.
For missing-information questions, evaluate abstention separately with a prespecified threshold.
Report paired differences on identical queries, with uncertainty clustered by case. A 50-case pilot is exploratory, not a powered clinical study.
Generated-answer factuality requires a separate claim-level rubric and reviewer; retrieval scores alone do not measure hallucinations.

## Repository map
- research/README.md: protocol and instructions
- research/baseline.py: dependency-free keyword smoke demo
- research/results/: locally generated outputs (not study findings)
- Future: data/synthetic/, evaluation adapters, Colab analysis notebook, tests, and frozen results

## Run the starter
From the repository root:
```bash
python research/baseline.py
```
This runs three fictional documents and two hand-authored queries through a token-overlap baseline. It prints top-1 accuracy and ranked document IDs.
It is a smoke demo, not the 50-case dataset, a XERJ comparison, or evidence of clinical benefit.

## Six-week milestones
- Week 1: review protocol and define tasks with a prospective mentor.
- Week 2: author synthetic cases and independently check answer keys.
- Week 3: freeze development/test split and implement the XERJ adapter.
- Week 4: run the paired benchmark and repeated latency measurements.
- Week 5: analyze errors, uncertainty, and limitations in Colab.
- Week 6: write a short report and prepare an advising presentation.

## Reproducibility checklist
For every study run record: repository commit, dataset SHA-256, split, Python/dependency versions, retrieval configuration, random seed, hardware, run timestamp, raw rankings, and timing definition.
Do not claim Northwestern endorsement, real-world patient benefit, or demographic fairness from fictional examples.
Before recruiting people or using nonpublic health records, consult the supervising institution about ethics review and data access requirements.

## Mathematical foundations
- Sets and ratios: precision and recall.
- Linear algebra: vector representations and cosine similarity.
- Probability and statistics: paired comparisons and confidence intervals.
- Experimental design: holdout cases, leakage prevention, and controlled comparisons.

## First action after merging
Read this protocol, then manually author five development cases and their relevance labels before expanding to 50.

