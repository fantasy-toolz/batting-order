# batting-order
## Batting Orders, drawn from MLB data

### Summary

This repository collects the batting order of each team for each game by automatically analysing the MLB statcast data. Each team has a .csv file in the `data/[year]/` directory, which is update each morning of the regular season with the previous day's games (run by `scrape-player-batting-order.py`).

We have historical data from the 2021 season onwards available. If you want an earlier season, please contact us.

We also have postseason lineups for 2023 and 2024 available in `data/Postseason/[year]/` for each team.

### Analysis Tools (in `analysis`)

There are also analysis scripts that are periodically run to create aggregated content for the [Fantasy Toolz webpage](https://fantasy-toolz.github.io).

1. `aggregate-data`: consolidate all scraped data into an easy-to-digest .csv
2. `summarise-year`: create summary statistics for each player from the full logs


### Predictions (in `predictions`)

We have also predicted, through a mixture of automated and hand-made lineups, the number of plate appearances for each player, for the 2023 and 2024 season. **2025 coming soon!**