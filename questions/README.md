# Questions

**1,744 real health questions** people sent to the U.S. National Library of Medicine (NLM), in their own words.
Built in [vivwebsolutions/HealthRAG#158](https://github.com/vivwebsolutions/HealthRAG/issues/158); this is a copy
of `data/question-bank/` there, at HealthRAG commit `3df36e7`.

| Pack | Questions | Source | Licence |
|---|---:|---|---|
| `consumer-health` | 104 | [TREC 2017 LiveQA medical test set](https://github.com/abachaa/LiveQA_MedicalTask_TREC2017), with reference answers | CC BY 4.0 |
| `consumer-health` | 989 | [MeQSum](https://github.com/abachaa/MeQSum) (ACL 2019) | CC BY 4.0 |
| `medications` | 651 | [MedicationQA](https://github.com/abachaa/Medication_QA_MedInfo2019) (MEDINFO 2019) | CC BY 4.0 |

Credit for all three: Asma Ben Abacha, Dina Demner-Fushman and colleagues at NLM. NLM de-identified the messages
(`[NAME]`, `[CONTACT]`, `[LOCATION]`).

- Every question has `provenance` (who wrote the wording: `kind: "live"` for all of these, none AI-written).
- `expect.source` is the reference answer's URL. `expect.answer` holds the text only when it comes from a
  public-domain U.S. federal page; otherwise only the URL is kept (tag `answer-at-source`).
- **Topics:** `health-questions.vocab.json` (83 terms in 4 facets: what kind of answer, health area, kind of
  medicine, health and human services). The tags are in `health-question-topics.tags.jsonl`. Each tag names the
  keyword rule that made it; every rule was checked by an AI judge in Viv Taxonomy Tools (HealthRAG#158).
- `health-questions.provenance.json`: where every topic came from, its definition (AI-drafted), and its MeSH and
  Open Eligibility mappings. Open Eligibility is linked by id only (its labels are CC BY-SA).
