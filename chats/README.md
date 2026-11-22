# Health chats to compare

`health-chats.csv` is the list of chats, one row each, with the **profile** fields from the comparison taxonomy
(`profile/*` in `../comparison/health-chat-comparison.json`). An empty cell means **not checked yet**, never "no".
Fill a cell only from the maker's own page, and put the date in `price_checked` (or a note) when you do.

`kind` is `product` (an app people use) or `model` (a model on its own); `openness` is `closed`, `open-weights` or
`open-source`. `providers.json` says how to reach each one's API; model ids marked `toConfirm` must be checked
before a run.

`ratings.csv` holds scores, one row per chat × rated term × run. It is **generated** by `scripts/aggregate.py`
from `runs/`; never edit it by hand. **It is empty: no chat has been rated yet.** See
[`../docs/leaderboard.md`](../docs/leaderboard.md).

## Conflicts of interest

- **SmartSearch** is made by Viv Web Solutions, which runs this repository.
- **Claude** (Anthropic) drafted the question tagging, the taxonomy and these files.

Both are tested the same way as every other chat, and their results should be graded by someone independent.
