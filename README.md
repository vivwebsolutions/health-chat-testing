# Testing health AI chats

Millions of people now ask chatbots about their health. This is an open hub for testing how well they answer,
**like a Hugging Face leaderboard for health chats**: real questions to ask, a list of what to measure, scripts
anyone can run, and a public leaderboard where anyone can report results, marked self-reported until verified.

It covers **closed chats** (ChatGPT, Claude, Gemini...), **open-weight and open-source models** (Llama, Mistral,
Qwen, Gemma, OLMo) and **open medical models** (MedGemma, Meditron, BioMistral, OpenBioLLM). Openness is part of
every profile.

| Folder | What's in it |
|---|---|
| [`questions/`](questions/) | **1,744 real health questions** people sent to the U.S. National Library of Medicine, in their own words, tagged by topic and by the kind of answer wanted. 397 have a reference answer. |
| [`comparison/`](comparison/) | **What to measure**: a taxonomy of 58 terms. `rated/*` is what a test scores (accuracy, safety, readability, sources, fairness, privacy...). `profile/*` is the facts every chat profile carries (maker, audience, price...). `method/*` is how a study tested. |
| [`docs/how-to-test.md`](docs/how-to-test.md) | **The method**, in four steps: pick real questions, ask them in fresh sessions, grade them, and report every failure with its question. |
| [`questions/hard-cases.json`](questions/hard-cases.json) | **32 hard cases** (AI-written, marked so): emergencies, crises, false premises, dosing, out-of-date advice, sources, Spanish. Each has a checklist of what a safe answer must do. |
| [`chats/`](chats/) | **19 chats and models to compare**: 10 products and 9 open models, each with its kind and openness, and `providers.json` (how to reach each one's API). |
| [`LEADERBOARD.md`](LEADERBOARD.md) | **The results**, generated from `runs/`. **No chat has been rated yet.** |
| [`docs/leaderboard.md`](docs/leaderboard.md) | **The path for a run**: ask (`scripts/run.py`), grade (`scripts/grade.py`), score (`scripts/aggregate.py`), submit a pull request, get verified. How Hugging Face does it, and what we borrow. |
| [`research/`](research/) | **What published research says**: PubMed has 16,703 papers on evaluating LLM and chatbot answers in health. A reading list of 150, starting with the reporting guidelines (CHART, TRIPOD-LLM, METRICS), and what studies rarely measure. |

It's listed in the Resources tab of the [HCF Case Studies Library](https://hcfhub.org), where every chat has
the same profile fields, so chats can be compared side by side.

## Why real questions

Most published tests use exam questions or questions experts wrote. Real people misspell drug names, ask three
things at once, describe their own case and expect a dose. Only about one study in five uses questions from the
public (`research/`). The questions here are exactly what people wrote, with who wrote them recorded on every
one.

## Next steps

- [x] **The path for a run**: runner, grader, aggregator, CI checks, issue forms (`docs/leaderboard.md`)
- [x] **A hard-cases set** (32, AI-written; a person should review it)
- [ ] **First rating runs**, by us or anyone: 100 sampled questions plus the hard cases, graded by an AI judge and
      checked by a clinician on a sample. Needs API keys or a local model runtime.
- [ ] **Fill the chat profiles** from each maker's own pages, with dates (`chats/health-chats.csv`), and confirm
      the model ids in `chats/providers.json`.
- [ ] **Check that links in answers are real** and say what the answer claims (`rated/quality/sources`).
- [ ] **A clinician to check** the AI-drafted definitions in `comparison/` and the reference answers.
- [ ] **Read the reading list properly**: the tags in `research/` come from keywords, not reading.
- [ ] **More real questions**: health department FAQs and other public, licensed sources.

Contributions are welcome: a run you made, a chat to add, a paper we missed. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Conflicts of interest

Viv Web Solutions runs this repository and makes **SmartSearch**, one of the chats
listed. **Claude** (Anthropic), another listed chat, drafted much of this kit. Both are tested the same way as
the rest, and their results should be graded by someone independent. See `chats/README.md`.

## Licence

Questions: CC BY 4.0, from NLM datasets (credit in `questions/README.md`). Everything else: CC BY 4.0. Scripts:
MIT. See `LICENSE.md`.
