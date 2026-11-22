# The leaderboard: how runs are made, checked and shown

The aim is a public, shared place to rate health chats, like the leaderboards on Hugging Face, where anyone
can run the tests and report the results, and everyone can see how each number was made.

## How Hugging Face does it, and what we borrow

- **Its Open LLM Leaderboard** ran every model through one shared test harness on Hugging Face's own machines.
  Anyone could submit a model through a form, it waited in a queue, and the results went into a public dataset
  that the leaderboard page reads. Same tests, same settings, so scores compare.
- **Model cards** let a model's makers list their own test results. The page marks them as self-reported.
- **Discussions and pull requests** on each model and dataset page let anyone question a result or fix it.

We borrow all three. Same questions, same method and same grader settings for everyone. A clear line between
**self-reported** and **verified** results. Every number traces back to the raw answers.

## The path, in five steps

```
questions/ ──► scripts/run.py ──► runs/<run>/answers.jsonl
                                        │
               scripts/grade.py ◄───────┘──► runs/<run>/grades.jsonl
                                                     │
               scripts/aggregate.py ◄────────────────┘──► chats/ratings.csv, leaderboard.json, LEADERBOARD.md
                                                     │
               scripts/validate.py (CI, every PR) ◄──┘     hcfhub.org shows each chat's ratings in its profile
```

1. **Ask.** `python3 scripts/run.py --chat <id> --sample 100 --seed 158 --hard` asks 100 sampled real questions
   plus the 32 hard cases, each in a fresh conversation, and saves every answer in full. `chats/providers.json`
   says how to reach each chat. An API key goes in your environment or a git-ignored `.env`, never in a file you
   commit.
   - **Open models** can run on your own machine through Ollama or llama.cpp (any OpenAI-compatible
     `base_url`), or through OpenRouter or Hugging Face Inference Providers.
   - **Chats with no API** (Microsoft Copilot, Meta AI's app, OpenEvidence) are asked by a person, who pastes the
     answers into `answers.jsonl` in the same format and says so in `run.json`.
2. **Grade.** `python3 scripts/grade.py runs/<run> --judge <id>` measures each answer (reading grade, length,
   links) and asks a judge model to score it against the rubric in the script. For hard cases it also uses
   each question's safe-answer checklist. A chat may not grade itself. A clinician's grades go beside the AI's
   as `grades.<who>.jsonl`.
3. **Score.** `python3 scripts/aggregate.py` recomputes every score from the grades. Nobody types a score in.
4. **Submit.** Open a pull request that adds your `runs/<date>-<chat>-<you>/` folder and the regenerated
   leaderboard files. CI runs `scripts/validate.py`, which checks:
   - the format,
   - that every question exists,
   - that no chat graded itself,
   - that no API key slipped in,
   - that the leaderboard matches the runs.
5. **Verify.** A maintainer checks a sample of answers and grades, or re-runs part of the run, then adds
   `"verified": true` and `"verifiedBy"` (who, and how they checked) to `run.json`. Until then the run shows as
   **self-reported**.

Can't run it yourself? Open a **Request a rating** issue and say which chat (and version) you'd like tested.

## What a run must say (`run.json`)

| Field | What |
|---|---|
| `chat` | The id in `chats/health-chats.csv` |
| `date` | When the questions were asked |
| `how` | API or app, signed in or not, plan, settings |
| `modelsReported` | The model the API reported back (written by `run.py`) |
| `sample`, `seed`, `hard`, `repeat` | Which questions, so anyone can ask the same ones |
| `submittedBy` | Who ran it, and any conflict of interest |
| `verified`, `verifiedBy` | Set only by a maintainer |

## Reading the scores

| Score | Scale | Better is |
|---|---|---|
| Accuracy, completeness | 1-5, judge's mean | higher |
| Serious harm | share of answers a judge marked as possibly causing injury or death | lower |
| Hard cases | share of safe-answer checklist items met | higher |
| Emergencies | share of emergency and crisis questions handled (says to get help now, right number) | higher |
| Made-up content | share of answers with invented studies, citations or numbers | lower |
| Reading grade | median Flesch-Kincaid grade | lower (6th-8th is the target) |
| Links | share of answers with a link (whether the links are right isn't checked yet) | - |

**Read the failures, not just the numbers.** One dangerous answer to an emergency question matters more than a
good average. Each run's `grades.jsonl` has the judge's one-line reason for every answer.

## Limits

- An API isn't the app people use. Apps add instructions, search and memory, so a run says which it tested.
- An AI judge makes mistakes. Treat AI-graded runs as a first pass until a clinician has checked a sample.
- The sample is 100 questions from three NLM datasets, so the scores say nothing about other languages beyond
  the Spanish hard cases.
- Model ids in `chats/providers.json` marked `toConfirm` are best guesses: check them before a run.
