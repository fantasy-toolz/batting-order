"""
scrape-player-batting-order
  a script to create a DataFrame with all the information we want for each team
"""

import numpy as np
import pandas as pd
from io import StringIO
import requests
import unicodedata


year = '2023'
# this is 2023 specific
yeardates = [str(pd.to_datetime(day, unit='D', origin=str(year))).split()[0] for day in range(88,365)]
#alldates = yeardates[0:np.where(np.array(yeardates)==str(pd.to_datetime("today").date()))[0][0]]

# this is 2024 season specific
year = '2024'
yeardates = [str(pd.to_datetime(day, unit='D', origin=str(year))).split()[0] for day in range(77,365)]

todaynum = np.where(np.array(yeardates)==str(pd.to_datetime("today").date()))[0][0]

alldates = yeardates[0:todaynum]

# check just the past couple of days
#alldates = yeardates[max(0,todaynum-15):todaynum]



teams = ['LAA', 'HOU', 'OAK', 'TOR', 'ATL', 'MIL', 'STL','CHC', 'AZ', 'LAD', 'SF', 'CLE', 'SEA', 'MIA','NYM', 'WSH', 'BAL', 'SD', 'PHI', 'PIT', 'TEX','TB', 'BOS', 'CIN', 'COL', 'KC', 'DET', 'MIN','CWS', 'NYY']

# create a file that stamps the last time run
f = open('data/{}/lasttouched.txt'.format(year),'w')
print(pd.to_datetime("today"),file=f)
f.close()

def get_team_game(year,date,team):
    link = 'https://baseballsavant.mlb.com/statcast_search/csv?all=true&hfPT=&hfAB=&hfGT=R%7C&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfPull=&hfC=&hfSea='+str(year)+'%7C&hfSit=&player_type=batter&hfOuts=&opponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt='+date+'&game_date_lt='+date+'&hfInfield=&team='+team+'&position=&hfOutfield=&hfRO=&home_road=&hfFlag=&hfBBT=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=pitches&player_event_sort=api_p_release_speed&sort_order=desc&min_pas=0&type=details&'
    header = {
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
      "X-Requested-With": "XMLHttpRequest"
    }
    r = requests.get(link, headers=header)
    csvStringIO = StringIO(r.text)
    DF = pd.read_csv(csvStringIO, low_memory=False)
    return DF

def num_games(DF):
    gamenums = np.unique(DF['game_pk'])
    return len(gamenums)

def get_team_order(DF):
    # count total number of at bats
    totalabs = np.nanmax(DF['at_bat_number'])
    # report
    #if verbose>1: print('...game!')
    # start counter for roster order
    order = 0
    # initialise blank roster
    gameorder = []
    # loop through at bats
    for num in range(0,totalabs):
        # what player is up to bat?
        plr = DF['player_name'][DF['at_bat_number']==num]
        # check if the at bat ended in an outcome
        try:
            eve = DF['events'][(DF['at_bat_number']==num)]
            # no outcome, don't count this at bat
            if len(eve)==np.sum(eve.isna()):
                continue
            if order<9:
                # add the player to the daily roster
                gameorder.append(np.unique(plr)[0])
            # if we logged the batting order, advance one roster position
            order +=1
            # break the loop if we have the full roster already
            if order==9:
                break#order=1
        except:
            pass
    return gameorder


def strip_accents(text):
    """
    https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-normalize-in-a-python-unicode-string
    Strip accents from input String.

    :param text: The input string.
    :type text: String.

    :returns: The processed String.
    :rtype: String.
    """
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError): # unicode is a default on python 3
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)


def rearrange_player(plrstring):
    splitup = plrstring.split(',')
    return(splitup[1]+' '+splitup[0])

def record_game(datestring,gameorder,f):
    print(datestring,end=',',file=f)
    for plr in gameorder:
        print(rearrange_player(strip_accents(plr)),end=',',file=f)
    print('',file=f)

#OrderDictList = dict()
for team in teams:
    newflag = 0
    print(team)
    # check if the team has already been recorded
    try:
        f = pd.read_csv('data/{}/{}.csv'.format(year,team),delimiter=',')
        maxdate = f['date'].values[-1]
        firstdate = np.where(maxdate==np.array(alldates))[0][0]
        alldatesin = alldates[firstdate+1:]
        newflag = 1
        f = open('data/{}/{}.csv'.format(year,team),'a')
    except:
        alldatesin = alldates
        f = open('data/{}/{}.csv'.format(year,team),'w')
    if (newflag==0):
        print('date,lineup1,lineup2,lineup3,lineup4,lineup5,lineup6,lineup7,lineup8,lineup9,',file=f)
    #OrderDictList[team] = dict()
    for date in alldatesin:
        print(date)
        DF = get_team_game(year,date,team)
        ngames = num_games(DF)
        if ngames>1: # allow for doubleheaders
            gamenums = np.unique(DF['game_pk'])
            for igame,gamenum in enumerate(gamenums):
                GDF = DF.loc[DF['game_pk']==gamenum]
                gameorder = get_team_order(GDF)
                if igame==0:
                    #OrderDictList[team][date+'a'] = gameorder
                    record_game(date+'a',gameorder,f)
                else:
                    #OrderDictList[team][date+'b'] = gameorder
                    record_game(date+'b',gameorder,f)
        elif ngames==1:
            gameorder = get_team_order(DF)
            #OrderDictList[team][date] = gameorder # add the roster to the team's list
            record_game(date,gameorder,f)
        else:
            pass
    #print(OrderDictList[team])
    f.close()
