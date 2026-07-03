# Plate-Appearance Forecasting Model

## Goal

The PA model estimates a player's full-season plate appearances from batting-order observations. It treats PA forecasting as two linked questions:

1. How many lineup starts will the player receive?
2. How many plate appearances does each lineup start create?

The notebook `PA-Prediction-Engine.ipynb` models these separately and combines them with Monte Carlo sampling to produce percentile forecasts rather than a single point estimate.

## Data Inputs

The model uses local repository data:

- `data/Aggregate/Summaries/*mean-player-batting-order.csv`
- `data/Aggregate/Summaries/player-batting-order-YYYY.csv`
- `data/Aggregate/YearlyStats/yearlystats-YYYY.csv`

The batting-order summaries provide:

- `avg_slot`: average batting-order position
- `starts`: lineup starts observed by the scraper
- `teamgames`: team games observed
- `start_share = starts / teamgames`

The yearly stats provide historical full-season `PA` totals.

Important distinction: `starts` are lineup starts, not all games appeared. This model forecasts PA through lineup starts.

## Name And Data Cleaning

Historical files use both `First Last` and `Last, First` player-name formats. The notebook normalizes names by:

- stripping accents
- converting `Last, First` to `First Last`
- removing periods and apostrophes
- case-folding whitespace-normalized names

The model also filters rows that are structurally impossible or likely bad joins:

- `starts <= 0`
- `PA <= 0`
- `starts > teamgames`
- `start_share` outside `[0, 1]`
- extreme `PA / start` values outside the configured range

Rows with `starts > teamgames` are usually same-name collisions in aggregate summaries.

## Component 1: Future Lineup Starts

For a current-season player, the observed role is:

```text
starts_so_far = S
team_games_so_far = T
misses_so_far = T - S
```

The player's lineup-start probability is modeled with a beta posterior:

```text
p_start ~ Beta(alpha_prior + S, beta_prior + T - S)
```

The current notebook uses a weak prior:

```text
alpha_prior = 2
beta_prior = 2
```

For each Monte Carlo draw:

```text
p_start_draw ~ Beta(alpha_post, beta_post)
remaining_starts_draw ~ Binomial(162 - T, p_start_draw)
projected_starts_draw = S + remaining_starts_draw
```

Projected starts are capped at the full-season game count.

## Component 2: PA Per Lineup Start

Historical seasons are used to fit PA per lineup start:

```text
pa_per_start = PA / starts
```

The model is a weighted linear regression with mild curvature and role-size interaction:

```text
pa_per_start = b0
             + b1 * avg_slot
             + b2 * avg_slot^2
             + b3 * start_share
             + b4 * avg_slot * start_share
             + error
```

Rows are weighted by `sqrt(starts)`, so players with more observed lineup starts influence the fit more than tiny samples without allowing everyday players to dominate completely.

Predicted PA/start is clipped to a plausible configured range:

```text
MIN_PA_PER_START = 2.0
MAX_PA_PER_START = 6.5
```

## Combining The Components

For each player, the notebook draws:

1. projected full-season starts from the beta-binomial start model
2. PA/start from the fitted PA/start model plus sampled historical residuals

Then:

```text
projected_PA_draw = projected_starts_draw * pa_per_start_draw
```

The forecast reports percentiles:

- `projected_starts_p10`, `projected_starts_p50`, `projected_starts_p90`
- `projected_pa_p10`, `projected_pa_p50`, `projected_pa_p90`
- `projected_remaining_pa_p50`

This gives an interval forecast that reflects both playing-time uncertainty and PA/start uncertainty.

## Validation

The notebook performs leave-one-season-out validation across the historical training seasons. For each holdout year:

1. train the PA/start model on all other years
2. predict PA/start for the holdout players
3. multiply by the actual holdout-year lineup starts
4. compare predicted PA to actual PA

This validates the PA/start component independently of the future-start model.

Reported validation metrics include:

- MAE
- RMSE
- bias

Validation is also split into player groups such as:

- all eligible players
- players with at least 50 starts
- players with at least 100 starts

## Current Limitations

The model is intentionally simple and transparent. It does not yet include:

- injuries or transaction context
- manual depth-chart priors
- preseason playing-time expectations
- handedness/platoon role information
- team run environment or lineup strength
- changes in role over recent weeks
- player-specific PA tendencies beyond batting-order slot and start share

The beta-binomial role model can overtrust early-season start rates because it only knows observed starts and misses. A player with 20 starts in 20 team games is treated similarly whether he is an established star or a short-term injury replacement.

## Best Next Upgrade

The next major statistical upgrade is to blend priors into the start model:

```text
p_start ~ Beta(prior_from_depth_chart + observed_starts,
               prior_from_depth_chart_misses + observed_misses)
```

Possible prior sources:

- preseason lineup-start projections
- previous-season starts
- rolling recent starts
- injury/IL information
- platoon split information from the platoon notebook

That would let the model distinguish true everyday players from temporary role spikes while preserving the clean Bayesian update structure.
