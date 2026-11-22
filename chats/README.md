# Health chats to compare

`health-chats.csv` is the list of chats, one row each, with the **profile** fields from the comparison taxonomy
(`profile/*` in `../comparison/health-chat-comparison.json`). An empty cell means **not checked yet**, never "no".
Fill a cell only from the maker's own page, and put the date in `price_checked` (or a note) when you do.

`ratings.csv` holds scores, one row per chat × rated term × run. **It is empty: no chat has been rated yet.** A
score is only added by a run that follows [`../docs/how-to-test.md`](../docs/how-to-test.md), and names the
question set, the number of questions, who or what graded them, and the date.

## Conflicts of interest

- **SmartSearch** is made by Viv Web Solutions, which runs this repository.
- **Claude** (Anthropic) drafted the question tagging, the taxonomy and these files.

Both are tested the same way as every other chat, and their results should be graded by someone independent.
