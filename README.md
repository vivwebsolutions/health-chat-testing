# Testing health AI chats

Millions of people now ask chatbots about their health. This repository is a free, open kit for testing how well
those chats answer. It holds real questions to ask them, a list of what to measure, a method anyone can follow,
and a shared place for results, so tests by different people can be compared.

| Folder | What's in it |
|---|---|
| [`questions/`](questions/) | **1,744 real health questions** people sent to the U.S. National Library of Medicine, in their own words, tagged by topic and by the kind of answer wanted. 397 have a reference answer. |
| [`comparison/`](comparison/) | **What to measure**: a taxonomy of 56 terms. `rated/*` is what a test scores (accuracy, safety, readability, sources, fairness, privacy...). `profile/*` is the facts every chat profile carries (maker, audience, price...). `method/*` is how a study tested. |
| [`docs/how-to-test.md`](docs/how-to-test.md) | **The method**, in four steps: pick real questions, ask them in fresh sessions, grade them, and report every failure with its question. |
| [`chats/`](chats/) | **The chats to compare** (ChatGPT, Claude, Gemini, Copilot, Meta AI, Perplexity, Grok, DeepSeek, OpenEvidence, SmartSearch) and `ratings.csv` for results. **No chat has been rated yet.** |
| [`research/`](research/) | **What published research says**: PubMed has 16,703 papers on evaluating LLM and chatbot answers in health. A reading list of 150, starting with the reporting guidelines (CHART, TRIPOD-LLM, METRICS), and what studies rarely measure. |

It's listed in the Resources tab of the [HCF Case Studies Library](https://hcfhub.org), where every chat has
the same profile fields, so chats can be compared side by side.

## Why real questions

Most published tests use exam questions or questions experts wrote. Real people misspell drug names, ask three
things at once, describe their own case and expect a dose. Only about one study in five uses questions from the
public (`research/`). The questions here are exactly what people wrote, with who wrote them recorded on every
one.

## Next steps

- [ ] **First rating run**: 100 sampled questions plus the hard cases (emergencies, false premises, dosing,
      Spanish), across all ten chats, graded by an AI judge and checked by a clinician on a sample.
- [ ] **Fill the chat profiles** from each maker's own pages, with dates (`chats/health-chats.csv`).
- [ ] **A runner script** that asks a chat the questions through its API and saves the answers, for the chats
      that have one.
- [ ] **A hard-cases set**: emergencies and crises, false premises, dosing for a named person, the same
      questions in Spanish. These test `rated/safety/*`, which random samples rarely reach.
- [ ] **A clinician to check** the AI-drafted definitions in `comparison/` and the reference answers.
- [ ] **Read the reading list properly**: the tags in `research/` come from keywords, not reading.
- [ ] **More real questions**: health department FAQs and other public, licensed sources.

Contributions are welcome. Open an issue with a test you ran, a chat to add, or a paper we missed.

## Conflicts of interest

[Viv Web Solutions](https://vivwebsolutions.com) runs this repository and makes **SmartSearch**, one of the chats
listed. **Claude** (Anthropic), another listed chat, drafted much of this kit. Both are tested the same way as
the rest, and their results should be graded by someone independent. See `chats/README.md`.

## Licence

Questions: CC BY 4.0, from NLM datasets (credit in `questions/README.md`). Everything else: CC BY 4.0. Scripts:
MIT. See `LICENSE.md`.
