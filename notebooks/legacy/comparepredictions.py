import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dfest = pd.read_csv('data/Aggregate/estimated_batting_stats_2024.csv')
dfcalc = pd.read_csv('data/Aggregate/mean-player-batting-order-2024.csv')


prefac = 162/97.
dfcalc['predictedPA'] = 2*(-9*dfcalc['avg'].values+380)
# rescale by the number of games in previous years for a fair comparison with PAprediction

# now cross-match against the two
merged_df = dfest.merge(dfcalc, how = 'inner', on = ['player'])


# all stats to-date
dfstat = pd.read_csv('/Users/mpetersen/FantasyBaseball/mlb-player-predictions/predictions/AllHitting_2024_2024.csv')

all_merge = merged_df.merge(dfstat, how = 'inner', on = ['player'])


playedfactor = dfstat['G']/98.
diffPA = dfstat['PA'] - (dfcalc['predictedPA'] * (98/162) * (playedfactor))

plt.scatter(dfstat['PA'],diffPA,color='black',s=1.)
plt.xlabel('PAs to date')
plt.ylabel('difference with predicted PAs')


plt.scatter(all_merge['PA'],all_merge['PAprediction']/prefac,color='black',s=1.)
plt.xlabel('PAs to date')
plt.ylabel('(scaled) predicted PAs')

lineup23
avg
bo24 = (all_merge['PA24lineup']/2 - 380)/-9

plt.scatter(all_merge['avg'],bo24,color='black',s=1.)
plt.xlabel('2024 average BO')
plt.ylabel('2024 predicted BO')

plt.scatter(all_merge['avg'],all_merge['lineup23'],color='black',s=1.)
plt.xlabel('2024 average BO')
plt.ylabel('2023 average BO')