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

def print_lineup(AllRosterDF,AllGameDF,team,gamenum):
    """an example application that prints the roster for a given team by game number"""
    series  = AllRosterDF[(AllRosterDF['team']==team) & (AllRosterDF['gamenum']==gamenum)]
    series2 = AllGameDF[(AllGameDF['team']==team) & (AllGameDF['gamenum']==gamenum)]
    print(team,' v ',series2['opponent'].values[0],' on ',series2['date'].values[0])
    print('1',series['b1'].values[0])
    print('2',series['b2'].values[0])
    print('3',series['b3'].values[0])
    print('4',series['b4'].values[0])
    print('5',series['b5'].values[0])
    print('6',series['b6'].values[0])
    print('7',series['b7'].values[0])
    print('8',series['b8'].values[0])
    print('9',series['b9'].values[0])


# define a list of all MLB team shorthands
teams = ['LAA', 'HOU', 'OAK', 'TOR', 'ATL', 'MIL', 'STL','CHC', 'ARI', 'LAD', 'SF', 'CLE', 'SEA', 'MIA','NYM', 'WSH', 'BAL', 'SD', 'PHI', 'PIT', 'TEX','TB', 'BOS', 'CIN', 'COL', 'KC', 'DET', 'MIN','CWS', 'NYY']


# bring in a DataFrame of interest:
AllGameDF = pd.read_csv('data/games2022.bck.csv')
AllGameDF = pd.read_csv('data/games2021.csv')

# print a list of how many times the leadoff spot came up for each team
#for team in teams:
#    print(team,AllGameDF['pa1'][AllGameDF['team']==team].sum())

# print a list of all games between MIN and MIL
#print(AllGameDF[(AllGameDF['opponent']=='MIL') & (AllGameDF['team']=='MIN')]['date'].values)

# print all available information for a random game
#print(AllGameDF.loc[np.random.randint(0,162*30)])

# make a scatter plot of the ratio of first to ninth PAs, as a function of first PAs
plt.figure(figsize=(4,4))

for team in teams:
    plt.scatter(AllGameDF['pa1'][AllGameDF['team']==team].sum(),\
    AllGameDF['pa1'][AllGameDF['team']==team].sum()/AllGameDF['pa9'][AllGameDF['team']==team].sum(),color='black')

plt.xlabel('1st spot PAs')
plt.ylabel('1st/9th spot ratio')
plt.tight_layout()
plt.savefig('figures/first-last-ratio-2022.png')

plt.figure(figsize=(4,4),facecolor='white')

for team in teams:
    for p in range(1,10):
        plt.scatter(p,AllGameDF['pa{}'.format(p)][AllGameDF['team']==team].sum(),color='black')

pnum = np.linspace(1.,9.,100)
plt.plot(pnum,2*(-9*pnum+380),color='red')
plt.xlabel('Lineup Spot')
plt.ylabel('PAs')
plt.tight_layout()
plt.savefig('figures/pa-summary-2021.png')



# bring in all rosters from the teams:
year='2021'
AllRosterDF = pd.read_csv('data/team-batting-order-'+year+'.csv')



print_lineup(AllRosterDF,AllGameDF,'MIN',125)
