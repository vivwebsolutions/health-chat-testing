# AGENTS.md: health-chat-testing

A **public** repository: everything here is published. Never add API keys, private data, client data or
abstracts of papers.

- **Questions** are a copy of `data/question-bank/` in vivwebsolutions/HealthRAG (issue #158). Change them there
  and copy them over; don't edit `questions/` by hand.
- **Taxonomy**: edit `scripts/comparison_taxonomy.py`, then run it. Never edit `comparison/*.json` or `*.csv`.
  It is catalogued in Health-Culture-Foundation/hcf-taxonomies.
- **Chats**: a profile cell is filled only from the maker's own page, with the date. Empty means not checked.
- **Ratings**: a row in `chats/ratings.csv` only from a run that follows `docs/how-to-test.md` and is published
  (question set, answers, grades). Never rate a chat from memory or impression.
- **Conflicts**: Viv makes SmartSearch and Claude drafted this kit. Say so wherever their results appear.
- The `chat` field group on hcfhub.org resources (vivwebsolutions/health-culture.org,
  `case-studies/resources/health-chat-testing.json`) mirrors `chats/health-chats.csv`. Change both.
- Branches: `claude/<topic>`, PR into `main`. Sign issue and PR text with:
  `> 🤖 *Written by Claude (Claude Code) on Kalman's behalf*`
