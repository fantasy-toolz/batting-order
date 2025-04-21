

import numpy as np
import pandas as pd
from io import StringIO
import requests
import unicodedata


year = '2023'
# this is 2023 specific
yeardates = [str(pd.to_datetime(day, unit='D', origin=str(year))).split()[0] for day in range(88,365)]


year = '2024'
yeardates = [str(pd.to_datetime(day, unit='D', origin=str(year))).split()[0] for day in range(77,365)]
alldates = yeardates[0:np.where(np.array(yeardates)==str(pd.to_datetime("today").date()))[0][0]]

teams = ['LAA', 'HOU', 'OAK', 'TOR', 'ATL', 'MIL', 'STL','CHC', 'AZ', 'LAD', 'SF', 'CLE', 'SEA', 'MIA','NYM', 'WSH', 'BAL', 'SD', 'PHI', 'PIT', 'TEX','TB', 'BOS', 'CIN', 'COL', 'KC', 'DET', 'MIN','CWS', 'NYY']



def load_orderdict(teams):
    OrderDictList = dict()
    for team in teams:
        OrderDictList[team] = dict()
        G = np.genfromtxt('data/2023/{}.csv'.format(team),skip_header=1,delimiter=',',dtype='S20')
        ngames = len(G[:,0])
        for g in range(0,ngames):
            #print(G[g])
            OrderDictList[team][G[g][0].decode()] = [G[g][p].decode() for p in range(1,10)]
    return OrderDictList


OrderDictList = load_orderdict(teams)


import numpy as np

def read_fixed_width_file(filename, colspecs, dtype):
    # Define a custom converter to strip spaces
    def strip_spaces(val):
        return val.strip()
    # Generate a delimiter array based on colspecs
    delimiter = [(start, start + width) for start, width in zip(
        np.cumsum([0] + colspecs[:-1]), colspecs)]  
    # Read the data using genfromtxt
    data = np.genfromtxt(filename, dtype=dtype, delimiter=delimiter, converters={i: strip_spaces for i in range(len(colspecs))})
    return data

# Define the column specifications (widths)
colspecs = [21,4]

# Define the data types for each column
dtype = [('name', 'U21'), ('order', 'U4')]

# Read the fixed-width file
data = read_fixed_width_file('data/Aggregate/mean-batting-2024.csv', colspecs, dtype)


TM = pd.read_csv('data/2023/TeamGuessesOpeningDay.csv')

TM = pd.read_csv('data/2023/TeamGuessesPreseason.csv')


def reverse_player(plr):
    nnames = plr.split(' ')
    if len(nnames)==2:
        return nnames[1]+', '+nnames[0]
    else:
        return nnames[1]+' '+nnames[2]+', '+nnames[0]


f = open('data/2023/2023PredictionSummary.csv','w')
print('team,exact,withinone',file=f)

for team in teams:
    #print(team)
    TM1 = TM.loc[TM['Team']==team]
    gameorder = [reverse_player(TM1['Lineup{}'.format(i)].values[0]) for i in range(1,10)]
    #print('PREDICTED LINEUP: ',gameorder)
    totaloverlap = 0
    within1 = 0
    for lineup in OrderDictList[team].keys():
        overlap = 0
        #within1 = 0
        for spot in range(0,len(OrderDictList[team][lineup])):
            if OrderDictList[team][lineup][spot]==gameorder[spot]:
                overlap +=1
                totaloverlap +=1
            if spot==0:
                if (OrderDictList[team][lineup][spot]==gameorder[spot+1]):
                    within1+=1
            elif spot==len(OrderDictList[team][lineup])-1:
                if (OrderDictList[team][lineup][spot]==gameorder[spot-1]):
                    within1+=1
            else:
                if (OrderDictList[team][lineup][spot]==gameorder[spot-1])|(OrderDictList[team][lineup][spot]==gameorder[spot+1]):
                    within1+=1
        #print(overlap,overlap+within1)
        #print(lineup)
        if gameorder==lineup:
            print('MATCH!')
    print('{0:3s},{1:4.2f},{2:4.2f}'.format(team,(totaloverlap)/len(OrderDictList[team]),(totaloverlap+within1)/len(OrderDictList[team])),file=f)

f.close()

# here, we'd like to analyse similarity metrics
