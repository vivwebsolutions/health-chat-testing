# Research on testing health AI chats

What published research says about evaluating chatbots that answer health questions, from PubMed on
**2026-11-21**.

## How big the field is

PubMed holds **16,703** papers that pair an LLM or chatbot with accuracy, quality, evaluation or readability, and
health. Narrower counts, with the exact queries, are in `counts.json`:

| Topic | Papers |
|---|---:|
| Safety or harm | 3,064 |
| Bias or equity | 2,926 |
| Misinformation or hallucination | 1,832 |
| Readability | 1,780 |
| Reporting guideline terms | 1,352 |
| Non-English | 1,304 |
| Systematic reviews | 1,236 |
| Mental health or crisis | 1,080 |
| DISCERN, PEMAT or Global Quality Score | 755 |
| OpenEvidence | 125 |
| An LLM grading another LLM | 107 |

## The reading list

`papers.json` has **150 papers**: 34 systematic or scoping reviews, 13 frameworks and reporting guidelines, 11
benchmarks and 92 evaluation studies, mostly from 2024-2026. Each has its PMID, DOI, journal, year, specialty, the
comparison terms it measures (`dimensions`, from `../comparison/`) and the instruments it used.

Start with the reporting guidelines and frameworks:

| PMID | Year | Paper |
|---|---|---|
| [40747871](https://pubmed.ncbi.nlm.nih.gov/40747871/) | 2025 | CHART: reporting guideline for chatbot health advice studies |
| [39779929](https://pubmed.ncbi.nlm.nih.gov/39779929/) | 2025 | TRIPOD-LLM reporting guideline |
| [38276872](https://pubmed.ncbi.nlm.nih.gov/38276872/) | 2024 | METRICS checklist for generative AI studies in health care |
| [41742713](https://pubmed.ncbi.nlm.nih.gov/41742713/) | 2026 | REFINE reporting checklist |
| [37957381](https://pubmed.ncbi.nlm.nih.gov/37957381/) | 2023 | Reporting standards for chatbots giving health advice |
| [39903463](https://pubmed.ncbi.nlm.nih.gov/39903463/) | 2025 | Systematic review of chatbot health advice studies |
| [42618044](https://pubmed.ncbi.nlm.nih.gov/42618044/) | 2026 | How reliable human evaluation of LLMs in health care is |
| [41343765](https://pubmed.ncbi.nlm.nih.gov/41343765/) | 2025 | CLEVER: expert review framework |
| [34719011](https://pubmed.ncbi.nlm.nih.gov/34719011/) | 2021 | Evaluation metrics for health chatbots (Delphi) |

## What studies measure, and what they don't

Most studies measure **accuracy** (107 of 150), with **expert graders** (69) and published **instruments** (82),
most often Flesch-Kincaid, DISCERN, Flesch Reading Ease, Likert scales and the Global Quality Score.
**Readability** (57) and **completeness** (56) come next.

Rarely measured, though they matter most for a public chat:

- whether advice is **up to date** (4),
- whether the chat **corrects a false premise** (2),
- whether it **knows when to refer** (6),
- **AI graders** (4),
- **whole conversations** rather than single questions (4).

Only 33 used **real questions** from the public. These gaps are where the question bank in `../questions/` and the
method in `../docs/how-to-test.md` add most. `gaps.md` lists further dimensions found, with example PMIDs.

## How this was made, and its limits

- Every PMID came from NCBI's E-utilities. The scripts are in `scripts/`.
- Papers were picked by relevance and spread across specialties, **not by citation count**.
- The `dimensions` and `instruments` tags were assigned by **keyword matching on titles and abstracts**, not by
  reading each paper, so the counts are approximate.
- The `why` lines are generated from those tags.
- No abstracts are stored here (they're the publishers').
- Some landmark papers were looked up by exact title and not found, so the list is a starting set, not a
  systematic review.
