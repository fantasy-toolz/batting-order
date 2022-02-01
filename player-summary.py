"""
player-summary
  an example script that will look at results for an individual player


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
mpl.rcParams['xtick.minor.visible'] = False
mpl.rcParams['ytick.minor.visible'] = False

def rearrange_name(player_name):
    """toggles names between last,first and first last """
    if ',' in player_name:
        return player_name.split(',')[1]+' '+player_name.split(',')[0]
    else:
        name_length = len(player_name.split(' '))
        if name_length==2:
            return player_name.split(' ')[1]+', '+player_name.split(' ')[0]
        if name_length==3:
            return player_name.split(' ')[1]+' '+player_name.split(' ')[2]+', '+player_name.split(' ')[0]

def make_player_order_matrix(player_name,years):


    nyears = len(years)
    order_matrix = np.zeros([nyears,9])

    for iyear,year in enumerate(years):
        AllPlayerDF = pd.read_csv('data/player-batting-order-'+year+'.csv')
        PlayerDF = AllPlayerDF[AllPlayerDF['player']==rearrange_name(player)]
        order_matrix[iyear] = np.array([PlayerDF['b1'].values[0],
                                        PlayerDF['b2'].values[0],
                                        PlayerDF['b3'].values[0],
                                        PlayerDF['b4'].values[0],
                                        PlayerDF['b5'].values[0],
                                        PlayerDF['b6'].values[0],
                                        PlayerDF['b7'].values[0],
                                        PlayerDF['b8'].values[0],
                                        PlayerDF['b9'].values[0]])
    return order_matrix

# define a list of all MLB team shorthands
teams = ['LAA', 'HOU', 'OAK', 'TOR', 'ATL', 'MIL', 'STL','CHC', 'ARI', 'LAD', 'SF', 'CLE', 'SEA', 'MIA','NYM', 'WSH', 'BAL', 'SD', 'PHI', 'PIT', 'TEX','TB', 'BOS', 'CIN', 'COL', 'KC', 'DET', 'MIN','CWS', 'NYY']

player = 'Trout, Mike'
player = 'Jackie Bradley Jr.'
player = 'Mike Trout'

year = '2021'
AllPlayerDF = pd.read_csv('data/player-batting-order-'+year+'.csv')
# can start by considering all 2021 players...where did they bat in previous years? How similar are they?

#print(AllPlayerDF.columns)
#Index(['Unnamed: 0', 'player', 'team', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6','b7', 'b8', 'b9'],

PlayerDF = AllPlayerDF[AllPlayerDF['player']==rearrange_name(player)]
#print(PlayerDF)
#print(PlayerDF['b1'].values[0])

order_matrix = make_player_order_matrix(player,['2016','2017','2018','2019','2020','2021'])
print(order_matrix)

plt.figure(figsize=(4,3))

plt.imshow(order_matrix,origin='lower',cmap=cm.Greys,aspect='auto')
plt.xlabel('batting order')
plt.ylabel('years')
plt.xticks([0,1,2,3,4,5,6,7,8],labels=[1,2,3,4,5,6,7,8,9])
#plt.xticklabels()
plt.yticks([0,1,2,3,4,5],labels=['2016','2017','2018','2019','2020','2021'])
#plt.yticklabels()
plt.tight_layout()
plt.savefig('figures/order_test.png')
