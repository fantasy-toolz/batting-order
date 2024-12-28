
import numpy as np
import pandas as pd
from io import StringIO
import requests
import unicodedata

from . import playerhandling

def get_team_game(year,date,team,mode='regularseason'):
    if mode=='regularseason':
        modestring = 'R%7C'
    if mode=='postseason':
        modestring = 'PO%7C'
    if mode=='preseason':
        modestring = 'S%7C'

    link = 'https://baseballsavant.mlb.com/statcast_search/csv?all=true&hfPT=&hfAB=&hfGT='+modestring+'&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfPull=&hfC=&hfSea='+str(year)+'%7C&hfSit=&player_type=batter&hfOuts=&opponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt='+date+'&game_date_lt='+date+'&hfInfield=&team='+team+'&position=&hfOutfield=&hfRO=&home_road=&hfFlag=&hfBBT=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=pitches&player_event_sort=api_p_release_speed&sort_order=desc&min_pas=0&type=details&'
    header = {
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
      "X-Requested-With": "XMLHttpRequest"
    }
    r = requests.get(link, headers=header)
    csvStringIO = StringIO(r.text)
    DF = pd.read_csv(csvStringIO, low_memory=False)
    return DF



def get_team_order(DF):
    """
    for a DF that is a specific MLB game scraped from savant, loop through and get the batting order.
    """
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

def num_games(DF):
    gamenums = np.unique(DF['game_pk'])
    return len(gamenums)


def record_game(datestring,gameorder,f):
    print(datestring,end=',',file=f)
    for plr in gameorder:
        print(playerhandling.rearrange_player(playerhandling.strip_accents(plr)),end=',',file=f)
    print('',file=f)
