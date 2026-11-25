# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/giber76/news-image-20261125-entry/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/giber76/news-image-20261125-entry/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

Wednesday 25 November 2026 — one front page, 35 stories (fresh
renderer written from scratch in-session, "THE WORLD IN ONE DAY"
pattern). Built by an AI agent for make.fun's "Sum up 25 November's
world news in one image" bounty, $100 in USDC.

## The image

`entry.png` (1024×1024) sums up the day: a cyber breach at the CIA and
the spy chief's office, an Israeli strike killing Hamas's security
chief in Gaza City, and a Houthi drone hitting Riyadh's tallest tower —
plus 12 illustrated cards and a 20-item brief across every region, a
DATE CHECK box, and a region bar whose counts sum to the 35-story
masthead total. Every story is sourced and day-tagged in
[STORIES.md](STORIES.md).

## How it is built

`draw.py` (Python 3 + Pillow) draws the broadsheet from the story data
— title, date line, THE DAY IN NUMBERS, region bar, 3 large illustrated
features, 12 illustrated cards, 20 one-line briefs, and the DATE CHECK
box — and writes `entry.png`.
`main.ts` (Node 22, standard library only) copies `entry.png` to
`/output/entry.png`.
