# Predicting Baseball Game Participation Using Bayesian Likelihoods

## Introduction

In baseball, each player has the potential to play in up to 162 games in a season. Using Bayesian statistics, we can predict the total number of games a player is likely to play based on the number of games they have participated in so far. This document explores the use of Bayesian likelihoods for this purpose.

## Bayesian Framework

Bayesian inference allows us to update our predictions about a player's total game participation as more data becomes available. We start with a prior belief about their participation and update this belief with the likelihood based on observed data.

### Prior Distribution

First, define a prior distribution reflecting our initial beliefs. A common choice is the **Beta distribution**, which is flexible and bounded between 0 and 1. For game participation, however, we might start with a **uniform distribution** between 0 and 162 as a non-informative prior.

### Likelihood Function

As the season progresses, we observe the number of games (`G`) the player has participated in out of the possible games to date (`T`). The likelihood function models the probability of observing this data given a hypothesized total number (`N`) of games for the player:

\[ P(G \mid N, T) = \text{Binomial}(G \mid N, T) \]

This is based on the assumption that each game is an independent event with its own probability.

### Posterior Distribution

The posterior distribution is updated as:

\[ P(N \mid G, T) \propto P(G \mid N, T) \times P(N) \]

This combines our prior belief with the likelihood of the observed data.

## Implementation

Here’s how you can implement this model in Python:

```python
import numpy as np
from scipy.stats import beta, binom
import matplotlib.pyplot as plt

# Prior parameters
alpha_prior, beta_prior = 1, 1  # Uniform prior

# Function to update posterior
def update_posterior(games_played, total_games, alpha=alpha_prior, beta=beta_prior):
    likelihood = binom.pmf(games_played, total_games, np.linspace(0, 1, 200))
    posterior = beta.pdf(np.linspace(0, 1, 200), alpha, beta) * likelihood
    posterior /= np.sum(posterior)
    return posterior

# Example update
G, T = 80, 100  # Games played out of possible games
posterior = update_posterior(G, T)

plt.plot(np.linspace(0, 1, 200), posterior)
plt.title('Posterior Distribution of Game Participation Rate')
plt.xlabel('Participation Rate')
plt.ylabel('Probability Density')
plt.show()
