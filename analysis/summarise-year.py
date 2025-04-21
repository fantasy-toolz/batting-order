
# code to create a summary of batting positions for a given player by year

import numpy as np
import pandas as pd
from io import StringIO
import unicodedata

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


timetag = ''
year = '2025'
#outdir = 'Preseason/'
#outdir = 'Postseason/'
outdir = ''

# default
start_date = '2025-01-01'
end_date = '2025-12-31'

timelimit=True

if timelimit:
    timetag = '-limitedtime'
    start_date = '2025-04-07'
    end_date = '2025-4-21'


teams = ['LAA', 'HOU', 'OAK', 'TOR', 'ATL', 'MIL', 'STL','CHC', 'AZ', 'LAD', 'SF', 'CLE', 'SEA', 'MIA','NYM', 'WSH', 'BAL', 'SD', 'PHI', 'PIT', 'TEX','TB', 'BOS', 'CIN', 'COL', 'KC', 'DET', 'MIN','CWS', 'NYY']

# if 2025+... Athletics is ATH
teams = ['LAA', 'HOU', 'ATH', 'TOR', 'ATL', 'MIL', 'STL','CHC', 'AZ', 'LAD', 'SF', 'CLE', 'SEA', 'MIA','NYM', 'WSH', 'BAL', 'SD', 'PHI', 'PIT', 'TEX','TB', 'BOS', 'CIN', 'COL', 'KC', 'DET', 'MIN','CWS', 'NYY']



# create a dictionary
PositionTotal = dict()
TeamTotal = dict()
PlrTeam = dict()

for team in teams:
    D = pd.read_csv('data/{}{}/{}.csv'.format(outdir,year,team))
    D['date'] = D['date'].str.replace('a', '').str.replace('b', '') # remove doubleheader tags for analysis
    D['date'] = pd.to_datetime(D['date'])

    D = D[(D['date'] >= start_date) & (D['date'] <= end_date)] # Filter rows based on the date range

    print('team: ',team,' games played: ',len(D['date']))
    TeamTotal[team] = len(D['date'])

    ngames = len(D['date'])
    for n in range(0,ngames):
        for i in range(0,10):
            if i==0:
                # this is the date, so skip ahead
                pass
            else:
                
                try:
                    PositionTotal[D['lineup{}'.format(i)].values[n].lstrip()][i-1] += 1
                except:
                    PositionTotal[D['lineup{}'.format(i)].values[n].lstrip()] = np.zeros(9)
                    PositionTotal[D['lineup{}'.format(i)].values[n].lstrip()][i-1] += 1
                    PlrTeam[D['lineup{}'.format(i)].values[n].lstrip()] = team
                


#print(PositionTotal)

# now make some summary stats
plrs = np.array(list(PositionTotal.keys()))
nplrs = len(plrs)
print("Players who have started a game this year:",nplrs)
f = open('data/{}/Aggregate/Summaries/'.format(outdir)+year+'player-batting-order{}.csv'.format(timetag),'w')
print('player,team,b1,b2,b3,b4,b5,b6,b7,b8,b9',file=f)

g = open('data/{}Aggregate/Summaries/'.format(outdir)+year+'mean-player-batting-order{}.csv'.format(timetag),'w') 
print('player,avg,ngames,teamgames,team',file=g)
for iplr,plr in enumerate(plrs):
    avgspot = np.nansum(np.arange(1,10,1)*PositionTotal[plr]/np.nansum(PositionTotal[plr]))
    ngames = np.nansum(PositionTotal[plr])
    print('{0},{1:4.2f},{2:3.0f},{3:3.0f},{4}'.format(plr,avgspot,ngames,TeamTotal[PlrTeam[plr]],PlrTeam[plr]),file=g)
    #print('{0},"{1}",{2},{3},{4},{5},{6},{7},{8},{9},{10},{11}'.format(iplr,rearrange_name(plr),PlrTeam[plr],PositionTotal[plr][0],PositionTotal[plr][1],PositionTotal[plr][2],PositionTotal[plr][3],PositionTotal[plr][4],PositionTotal[plr][5],PositionTotal[plr][6],PositionTotal[plr][7],PositionTotal[plr][8]),file=f)
    print('{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11}'.format(iplr,plr,PlrTeam[plr],PositionTotal[plr][0],PositionTotal[plr][1],PositionTotal[plr][2],PositionTotal[plr][3],PositionTotal[plr][4],PositionTotal[plr][5],PositionTotal[plr][6],PositionTotal[plr][7],PositionTotal[plr][8]),file=f)

f.close()
g.close()
