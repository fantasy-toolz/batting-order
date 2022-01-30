"""
batting-order-summary
  an example script that will generate summary statistics, and some basic visualisations


"""

import numpy as np
import pandas as pd

# plotting basics
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# override some parameters for a 'house style'
import matplotlib as mpl
mpl.rcParams['xtick.labelsize'] = 10
mpl.rcParams['ytick.labelsize'] = 10
mpl.rcParams['font.weight'] = 'medium'
mpl.rcParams['axes.linewidth'] = 1.5
mpl.rcParams['xtick.major.width'] = 1.5
mpl.rcParams['xtick.minor.width'] = 0.75
mpl.rcParams['ytick.major.width'] = 1.5
mpl.rcParams['ytick.minor.width'] = 0.75
mpl.rcParams['xtick.minor.visible'] = True
mpl.rcParams['ytick.minor.visible'] = True


# define a list of all MLB team shorthands
teams = ['LAA', 'HOU', 'OAK', 'TOR', 'ATL', 'MIL', 'STL','CHC', 'ARI', 'LAD', 'SF', 'CLE', 'SEA', 'MIA','NYM', 'WSH', 'BAL', 'SD', 'PHI', 'PIT', 'TEX','TB', 'BOS', 'CIN', 'COL', 'KC', 'DET', 'MIN','CWS', 'NYY']


# bring in a DataFrame of interest:
AllGameDF = pd.read_csv('data/games2021.csv')

# print a list of how many times the leadoff spot came up for each team
for team in teams:
    print(team,AllGameDF['pa1'][AllGameDF['team']==team].sum())

# print a list of all games between MIN and MIL
print(AllGameDF[(AllGameDF['opponent']=='MIL') & (AllGameDF['team']=='MIN')]['date'].values)

# print all available information for a random game
print(AllGameDF.loc[np.random.randint(0,162*30)])

# make a scatter plot of the ratio of first to ninth PAs, as a function of first PAs
plt.figure(figsize=(4,4))

for team in teams:
    plt.scatter(AllGameDF['pa1'][AllGameDF['team']==team].sum(),\
    AllGameDF['pa1'][AllGameDF['team']==team].sum()/AllGameDF['pa9'][AllGameDF['team']==team].sum(),color='black')

plt.xlabel('1st spot PAs')
plt.ylabel('1st/9th spot ratio')
plt.tight_layout()
plt.savefig('figures/first-last-ratio-2021.png')
