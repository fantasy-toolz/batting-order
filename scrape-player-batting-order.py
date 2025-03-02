"""
scrape-player-batting-order
  a script to create a DataFrame with all the information we want for each team
"""

import numpy as np
import pandas as pd
from io import StringIO
import requests
import unicodedata

from src import playerhandling
from src import gamehandling

gamemode = 'regularseason'
outdir = ''

year = '2025'
yeardates = [str(pd.to_datetime(day, unit='D', origin=str(year))).split()[0] for day in range(77,300)]
alldates = yeardates

"""
year = '2022'
yeardates = [str(pd.to_datetime(day, unit='D', origin=str(year))).split()[0] for day in range(77,300)]
alldates = yeardates


year = '2023'
# this is 2023 specific
yeardates = [str(pd.to_datetime(day, unit='D', origin=str(year))).split()[0] for day in range(88,365)]
#alldates = yeardates[0:np.where(np.array(yeardates)==str(pd.to_datetime("today").date()))[0][0]]

"""
# this is 2024 season specific
year = '2024'
yeardates = [str(pd.to_datetime(day, unit='D', origin=str(year))).split()[0] for day in range(77,365)]
#todaynum = np.where(np.array(yeardates)==str(pd.to_datetime("today").date()))[0][0]
alldates = yeardates#[0:todaynum]




# if doing postseason, limit dates
year = '2021'
gamemode = 'postseason'
if gamemode=='postseason':
    yeardates = [str(pd.to_datetime(day, unit='D', origin=str(year))).split()[0] for day in range(270,320)]
    alldates = yeardates
    outdir = 'Postseason/'


# if doing preseason, limit dates
year = '2025'
gamemode = 'preseason'
if gamemode=='preseason':
    yeardates = [str(pd.to_datetime(day, unit='D', origin=str(year))).split()[0] for day in range(48,92)]
    alldates = yeardates[0:np.where(np.array(yeardates)==str(pd.to_datetime("today").date()))[0][0]]
    outdir = 'Preseason/'

teams = ['LAA', 'HOU', 'OAK', 'TOR', 'ATL', 'MIL', 'STL','CHC', 'AZ', 'LAD', 'SF', 'CLE', 'SEA', 'MIA','NYM', 'WSH', 'BAL', 'SD', 'PHI', 'PIT', 'TEX','TB', 'BOS', 'CIN', 'COL', 'KC', 'DET', 'MIN','CWS', 'NYY']

# for 2025, need to update to ATH instead of OAK
teams = ['LAA', 'HOU', 'ATH', 'TOR', 'ATL', 'MIL', 'STL','CHC', 'AZ', 'LAD', 'SF', 'CLE', 'SEA', 'MIA','NYM', 'WSH', 'BAL', 'SD', 'PHI', 'PIT', 'TEX','TB', 'BOS', 'CIN', 'COL', 'KC', 'DET', 'MIN','CWS', 'NYY']

# create a file that stamps the last time run
f = open('data/{}{}/lasttouched.txt'.format(outdir,year),'w')
print(pd.to_datetime("today"),file=f)
f.close()


# this could use a safe mode that doesn't overwrite anything

#OrderDictList = dict()
for team in teams:
    newflag = 0
    print(team)
    # check if the team has already been recorded
    try:
        f = pd.read_csv('data/{}{}/{}.csv'.format(outdir,year,team),delimiter=',')
        maxdate = f['date'].values[-1]
        firstdate = np.where(maxdate==np.array(alldates))[0][0]
        alldatesin = alldates[firstdate+1:]
        newflag = 1
        f = open('data/{}{}/{}.csv'.format(outdir,year,team),'a')
    except:
        alldatesin = alldates
        f = open('data/{}{}/{}.csv'.format(outdir,year,team),'w')
    if (newflag==0):
        print('date,lineup1,lineup2,lineup3,lineup4,lineup5,lineup6,lineup7,lineup8,lineup9,',file=f)
    #OrderDictList[team] = dict()
    for date in alldatesin:
        print(date)
        DF = gamehandling.get_team_game(year,date,team,mode=gamemode)
        ngames = gamehandling.num_games(DF)
        if ngames>1: # allow for doubleheaders
            gamenums = np.unique(DF['game_pk'])
            for igame,gamenum in enumerate(gamenums):
                GDF = DF.loc[DF['game_pk']==gamenum]
                gameorder = gamehandling.get_team_order(GDF)
                if igame==0:
                    #OrderDictList[team][date+'a'] = gameorder
                    gamehandling.record_game(date+'a',gameorder,f)
                else:
                    #OrderDictList[team][date+'b'] = gameorder
                    gamehandling.record_game(date+'b',gameorder,f)
        elif ngames==1:
            gameorder = gamehandling.get_team_order(DF)
            #OrderDictList[team][date] = gameorder # add the roster to the team's list
            gamehandling.record_game(date,gameorder,f)
        else:
            pass
    #print(OrderDictList[team])
    f.close()
