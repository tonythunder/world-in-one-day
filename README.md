# The world in focus

[![News image](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![Rank](https://make.fun/badge/news-image-20261123/tonythunder/world-in-one-day/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard)
[![Reward](https://make.fun/badge/news-image-20261123/tonythunder/world-in-one-day/reward.svg)](https://make.fun/bounty/news-image-20261123)

A daily visual front page assembled from a fixed UTC news edition. The Monday 23 November 2026 issue covers Nvidia's leadership reversal, the European Commission's proposed Russia sanctions and shipping in the Strait of Hormuz. Citations and event dates are included in [the edition data](editions/2026-11-23/news.json).

## Render

Run `python main.py` to produce `/output/entry.png`. The default date is pinned in `edition.txt`. To render a particular edition locally, use `python main.py --date 2026-11-23 --out preview`. Each render uses the standard library and the committed data. Text is composed from the edition copy and glyph masks over a fixed RGB illustration plate. The runtime makes no network requests and reads no clock.

## Art and reproduction

To regenerate the Monday plate and raster type atlas, run `python -m pip install Pillow==13.0.0` in an authoring environment, then `python tools/prepare.py 2026-11-23`. Both compiled assets are included for dependency-free contest execution. The chart compares closing percentage changes on one linear scale. The lower illustrations identify the topics and ship count. They are schematic.

The 2023 archive portrait is by Taiwan's Office of the President, cropped by a Wikimedia Commons contributor. This edition resized and cropped the photograph. [Original file and attribution](https://commons.wikimedia.org/wiki/File:Jensen_Huang_20231109.jpg) · [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/)

DM Serif Display and Barlow are distributed under the SIL Open Font License. See the license notices in `licenses/`. Original program code and original artwork are licensed under MIT.

