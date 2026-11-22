# Contributing

Anyone can test a health chat with this kit and add the results. See [docs/leaderboard.md](docs/leaderboard.md)
for the whole path.

- **Run the tests yourself:** `scripts/run.py`, then `scripts/grade.py`, then `scripts/aggregate.py`. Open a
  pull request with your `runs/<date>-<chat>-<you>/` folder and the regenerated leaderboard files. CI checks it.
  Your run shows as *self-reported* until a maintainer verifies it.
- **Ask for a chat to be tested:** open a "Request a rating" issue.
- **Add a chat or model:** add a row to `chats/health-chats.csv`, filling only what the maker's own pages say,
  and add how to reach it to `chats/providers.json`.
- **Add questions:** real questions need a source and a licence that allows reuse. AI-written questions go in
  the hard cases, marked `ai-drafted`.
- **Question a result:** open an issue naming the run and the question. Every answer and grade is in the run
  folder.

Say who you are and any conflict of interest in every run and pull request. Never commit an API key.
