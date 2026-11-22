# How to test a health chat

A short method anyone can follow, so results from different people can be compared. The terms in brackets are
from the comparison taxonomy (`comparison/health-chat-comparison.json`).

## 1. Pick the questions

- **Start with real questions** [`method/questions-real`]. `questions/health-consumer-questions.json` has 1,744
  questions people sent to the U.S. National Library of Medicine, in their own words, typos included. Each has a
  topic (`tags` in `questions/health-question-topics.tags.jsonl`), and 397 have a reference answer.
- **Sample, don't cherry-pick.** Take a fixed random sample (say 100) with a written seed, or a whole topic
  (every `ask/dose` question). Write down which.
- **Add the hard cases on purpose**, as their own set: emergencies and crises, false premises
  ("since vaccines cause autism..."), dosing for a named person, and the same question in Spanish. These
  test `rated/safety/*`, which a random sample rarely hits.

## 2. Ask them

- Use a **fresh session** for each question, with no memory or custom instructions, signed out where the chat
  allows it. Note the date, the plan (free or paid) and the model the chat says it is using.
- Paste the question **exactly as written**.
- To measure consistency [`rated/quality/consistency`], ask each question **three times**, in three sessions.
- Save every answer in full, with any links it gave.

## 3. Grade the answers

- For each answer, score the `rated/*` terms you are testing on a stated scale (for example 1-5, or pass/fail).
- **Who grades:** a clinician for accuracy and harm [`method/expert-rating`]. An AI grader
  [`method/llm-judge`] is fine for a first pass, but check a sample of its grades by hand and report how often
  you agreed.
- **Check the sources** [`rated/quality/sources`]: open every link. Does it exist? Does it say what the answer
  says it says?
- **Readability** [`rated/communication/readability`]: run a readability formula on the answer text and report
  which one.
- Grade without knowing which chat wrote the answer, where you can.

## 4. Report

- Add one row per chat, term and run to `chats/ratings.csv`. Say the question set, how many questions, who
  graded, and the date.
- Report **what failed, with the question**, not just the average. One dangerous answer matters more than a
  good mean score.
- Say who you are and any conflict of interest (see `chats/README.md`).
- If you publish a study, follow a reporting guideline for chatbot health advice studies
  [`method/reporting-guideline`]; see `research/`.

## What this method does not do

It doesn't test a chat on a person's real records, or over a long conversation, or when someone's using it to
decide on treatment. Those need a clinical study, not a question set.
