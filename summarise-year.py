
# code to create a summary of batting positions for a given player by year

import numpy as np
import pandas as pd
from io import StringIO
import unicodedata

year = '2023'

teams = ['LAA', 'HOU', 'OAK', 'TOR', 'ATL', 'MIL', 'STL','CHC', 'AZ', 'LAD', 'SF', 'CLE', 'SEA', 'MIA','NYM', 'WSH', 'BAL', 'SD', 'PHI', 'PIT', 'TEX','TB', 'BOS', 'CIN', 'COL', 'KC', 'DET', 'MIN','CWS', 'NYY']


# create a dictionary
PositionTotal = dict()
TeamTotal = dict()

for team in teams:
    D = np.genfromtxt('data/{}/{}.csv'.format(year,team),delimiter=',',dtype='S20',skip_header=1)
    print('team: ',team,' games played: ',len(D[:,0]))
    #print('date,lineup1,lineup2,lineup3,lineup4,lineup5,lineup6,lineup7,lineup8,lineup9,',file=f)
    ngames = len(D[:,0])
    for n in range(1,ngames):
        for i in range(0,10):
            if i==0:
                # this is the date, so skip ahead
                pass
            else:
                TeamTotal[D[n][i].decode().lstrip()] = team
                try:
                    PositionTotal[D[n][i].decode().lstrip()][i-1] += 1
                except:
                    PositionTotal[D[n][i].decode().lstrip()] = np.zeros(9)
                    PositionTotal[D[n][i].decode().lstrip()][i-1] += 1


#print(PositionTotal)

# now make some summary stats
plrs = np.array(list(PositionTotal.keys()))
nplrs = len(plrs)
print(nplrs)
f = open('data/Aggregate/player-batting-order-'+year+'.csv','w')
print(',player,team,b1,b2,b3,b4,b5,b6,b7,b8,b9',file=f)
for iplr,plr in enumerate(plrs):
    avgspot = np.nansum(np.arange(1,10,1)*PositionTotal[plr]/np.nansum(PositionTotal[plr]))
    print('{0:20s} {1:4.2f}'.format(plr,avgspot))
    print('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11}'.format(iplr,plr,TeamTotal[plr],PositionTotal[plr][0],PositionTotal[plr][1],PositionTotal[plr][2],PositionTotal[plr][3],PositionTotal[plr][4],PositionTotal[plr][5],PositionTotal[plr][6],PositionTotal[plr][7],PositionTotal[plr][8]),file=f)

f.close()

years = ['2020','2021','2022','2023']
# bring in batting order data
for year in years:
    #print(year)
    df = pd.read_csv('data/Aggregate/player-batting-order-'+year+'.csv')

    keyvals = ['b1','b2','b3','b4','b5','b6','b7','b8','b9']
    for k in keyvals:
        for x in df[k].values:
            try:
                #print(strip_accents(x))
                df[k][df[k]==x] = strip_accents(x)
            except:
                pass

    df['year'] = year
    if year == years[0]:
        AllPlayerBO = df
    else:
        AllPlayerBO = pd.concat([AllPlayerBO,df])


print(AllPlayerBO)