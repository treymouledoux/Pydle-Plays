# My Pydle Plays

My attempts at [Pydle](https://pydle.net), one Python puzzle at a time 🐍

<!-- pydle-progress:start -->
**19 games completed** · **21 attempted**

**9 hard** · **10 easy only** · **2 incomplete** (2 broken)

![Pydle pie chart](assets/pydle-progress.svg)

Archive percentage and unattempted games will appear after the first successful update.

| Game | Best saved score | Result |
| --- | ---: | --- |
| #1 | 116 | Hard |
| #63 | 111 | Hard |
| #67 | 163 | Easy only |
| #68 | 92 | Hard |
| #69 | 170 | Easy only |
| #70 | — | Incomplete (broken) |
| #71 | 103 | Hard |
| #72 | 111 | Hard |
| #73 | 125 | Easy only |
| #76 | 94 | Hard |
| #81 | 106 | Hard |
| #83 | 144 | Easy only |
| #84 | — | Incomplete (broken) |
| #87 | 79 | Hard |
| #88 | 147 | Easy only |
| #226 | 137 | Easy only |
| #229 | 223 | Easy only |
| #230 | 144 | Easy only |
| #231 | 156 | Easy only |
| #232 | 147 | Easy only |
| #233 | 123 | Hard |
<!-- pydle-progress:end -->

All my attempts are in [`games/`](games). Each filename starts with its game number, like `#73 Frog.py`.

Progress updates automatically on every push to the default branch and every day through GitHub Actions. The Action generates `assets/pydle-progress.svg` and commits it with the updated README.

The shortest saved attempt determines each game's result: **Hard** is under 125 characters; **Easy only** is 125–249; **Incomplete** includes scores of 250 or more and broken attempts. Hard also beats easy, but each game occupies just one pie slice. Unattempted archive games get their own slice.

Scores come from the Pydle character counts recorded in comment headers, like `#Final Solution 123 / 250 chars`, paired with the code below them. Empty attempt sections are ignored. Attempts without a recorded score count as incomplete until a score is added. This tracks saved scores; it doesn't run solutions or validate their output against Pydle.

To refresh manually, run **Update Pydle progress** from the Actions tab. If needed, set the repository variable `PYDLE_ARCHIVE_URL` to the archive's URL; otherwise the updater opens the archive from the homepage.

For a local refresh:

```sh
python -m pip install playwright==1.58.0
python -m playwright install chromium
python scripts/update_progress.py
```

If the archive can't be read, the workflow fails and keeps the previous progress display.
