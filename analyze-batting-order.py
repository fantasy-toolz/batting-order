

import numpy as np
import pandas as pd
from io import StringIO
import requests
import unicodedata


year = '2023'
# this is 2023 specific
yeardates = [str(pd.to_datetime(day, unit='D', origin=str(year))).split()[0] for day in range(88,365)]
alldates = yeardates[0:np.where(np.array(yeardates)==str(pd.to_datetime("today").date()))[0][0]]

teams = ['LAA', 'HOU', 'OAK', 'TOR', 'ATL', 'MIL', 'STL','CHC', 'AZ', 'LAD', 'SF', 'CLE', 'SEA', 'MIA','NYM', 'WSH', 'BAL', 'SD', 'PHI', 'PIT', 'TEX','TB', 'BOS', 'CIN', 'COL', 'KC', 'DET', 'MIN','CWS', 'NYY']



def load_orderdict(teams):
    OrderDictList = dict()
    for team in teams:
        OrderDictList[team] = dict()
        G = np.genfromtxt('data/2023/{}.csv'.format(team),skip_header=1,delimiter=';',dtype='S20')
        ngames = len(G[:,0])
        for g in range(0,ngames):
            #print(G[g])
            OrderDictList[team][G[g][0].decode()] = [G[g][p].decode() for p in range(1,10)]
    return OrderDictList


OrderDictList = load_orderdict(teams)


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
