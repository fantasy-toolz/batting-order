"""
scrape-player-batting-order
  a script to create a DataFrame with all the information we want for each team
"""

import numpy as np
import pandas as pd
from io import StringIO
import requests
import unicodedata
from typing import TextIO

from src import playerhandling
from src import gamehandling

gamemode: gamehandling.GameMode = 'regularseason'
outdir: str = ''

year: str = '2025'
yeardates: list[str] = [str(pd.to_datetime(day, unit='D', origin=str(year))).split()[0] for day in range(77,300)]
alldates: list[str] = yeardates

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
year = '2026'
yeardates = [str(pd.to_datetime(day, unit='D', origin=str(year))).split()[0] for day in range(82,365)]
todaynum: int = np.where(np.array(yeardates)==str(pd.to_datetime("today").date()))[0][0]
alldates = yeardates[0:todaynum]


"""
yeardates = [str(pd.to_datetime(day, unit='D', origin=str(year))).split()[0] for day in range(85,365)]
todaynum = np.where(np.array(yeardates)==str(pd.to_datetime("today").date()))[0][0]
alldates = yeardates[0:todaynum]


# if doing postseason, limit dates
gamemode = 'postseason'
if gamemode=='postseason':
    yeardates = [str(pd.to_datetime(day, unit='D', origin=str(year))).split()[0] for day in range(270,320)]
    todaynum = np.where(np.array(yeardates)==str(pd.to_datetime("today").date()))[0][0]
    alldates = yeardates[0:todaynum]
    #alldates = yeardates
    outdir = 'Postseason/'
"""

# if doing preseason, limit dates
#gamemode = 'preseason'
if gamemode=='preseason':
    yeardates = [str(pd.to_datetime(day, unit='D', origin=str(year))).split()[0] for day in range(49,92)]
    alldates = yeardates[0:np.where(np.array(yeardates)==str(pd.to_datetime("today").date()))[0][0]]
    outdir = 'Preseason/'

teams: list[str] = ['LAA', 'HOU', 'OAK', 'TOR', 'ATL', 'MIL', 'STL','CHC', 'AZ', 'LAD', 'SF', 'CLE', 'SEA', 'MIA','NYM', 'WSH', 'BAL', 'SD', 'PHI', 'PIT', 'TEX','TB', 'BOS', 'CIN', 'COL', 'KC', 'DET', 'MIN','CWS', 'NYY']

# for 2025+, need to update to ATH instead of OAK
teams = ['LAA', 'HOU', 'ATH', 'TOR', 'ATL', 'MIL', 'STL','CHC', 'AZ', 'LAD', 'SF', 'CLE', 'SEA', 'MIA','NYM', 'WSH', 'BAL', 'SD', 'PHI', 'PIT', 'TEX','TB', 'BOS', 'CIN', 'COL', 'KC', 'DET', 'MIN','CWS', 'NYY']

# hack for the postseason - only teams that made it
#teams = ['TOR','LAD','MIL',  'SEA']

# create a file that stamps the last time run
last_touched_file: TextIO = open('data/{}{}/lasttouched.txt'.format(outdir,year),'w')
print(pd.to_datetime("today"),file=last_touched_file)
last_touched_file.close()


# this could use a safe mode that doesn't overwrite anything

#OrderDictList = dict()
for team in teams:
    newflag: int = 0
    print(team)
    # check if the team has already been recorded
    try:
        existing_lineups: pd.DataFrame = pd.read_csv('data/{}{}/{}.csv'.format(outdir,year,team),delimiter=',')
        maxdate: str = existing_lineups['date'].values[-1].strip('a').strip('b') # safe for doubleheaders
        firstdate: int = np.where(maxdate==np.array(alldates))[0][0]
        alldatesin: list[str] = alldates[firstdate+1:]
        newflag = 1
        f: TextIO = open('data/{}{}/{}.csv'.format(outdir,year,team),'a')
    except:
        alldatesin = alldates
        f = open('data/{}{}/{}.csv'.format(outdir,year,team),'w')
    if (newflag==0):
        print('date,lineup1,lineup2,lineup3,lineup4,lineup5,lineup6,lineup7,lineup8,lineup9,',file=f)
    #OrderDictList[team] = dict()
    for date in alldatesin:
        print(date)
        DF: pd.DataFrame | None = gamehandling.get_team_game(year,date,team,mode=gamemode)
        ngames: int = gamehandling.num_games(DF)
        if ngames>1: # allow for doubleheaders
            gamenums: np.ndarray = np.unique(DF['game_pk'])
            for igame,gamenum in enumerate(gamenums):
                GDF: pd.DataFrame = DF.loc[DF['game_pk']==gamenum]
                gameorder: list[str] = gamehandling.get_team_order(GDF)
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
