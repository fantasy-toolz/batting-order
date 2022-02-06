"""
scrape-team-games
  a script to create a DataFrame with all the information we want:
  -team
  -game number
  -date
  -opposing pitcher handedness
  -plate appearances by batting order slot
  -whether the game is a doubleheader or not

  this routine is expensive: we heartily recommend that you use the already-processed csv files in data/!

"""

import numpy as np
import pandas as pd


def create_year_summary_df(year,teams,verbose=2):

    # create a DF to hold all the data we are interested in
    AllGameDF = pd.DataFrame(columns=['team','gamenum','opponent','date','opposinghandedness','pa1','pa2','pa3','pa4','pa5','pa6','pa7','pa8','pa9','dblheader'],index=[i for i in range(0,162*len(teams))])

    # initialise a row index counter
    offset = 0

    # loop through all teams
    for team in teams:

        # print progress
        if verbose>0: print(team)

        # initialise team counter for game number
        gnum = 0

        # loop over dates for a typical baseball season. if there are very early games in a year, may need to extend.
        for day in range(91,285):

            # convert day number to string for savant searching
            dayval = pd.to_datetime(day-1, unit='D', origin=str(year))
            date = str(dayval).split()[0]

            # report progress
            if verbose>1: print(date,end='')

            # the workhorse: use pandas to retrieve a csv of the game data from MLB's statcast data repository
            # working string (30 Jan 2022)...not guaranteed to be infallible
            link = 'https://baseballsavant.mlb.com/statcast_search/csv?all=true&hfPT=&hfAB=&hfGT=R%7C&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfPull=&hfC=&hfSea='+str(year)+'%7C&hfSit=&player_type=batter&hfOuts=&opponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt='+date+'&game_date_lt='+date+'&hfInfield=&team='+team+'&position=&hfOutfield=&hfRO=&home_road=&hfFlag=&hfBBT=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=pitches&player_event_sort=api_p_release_speed&sort_order=desc&min_pas=0&type=details&'
            DF = pd.read_csv(link, low_memory=False)


            try:
                # do we have a valid DF?
                totalabs = np.nanmax(DF['at_bat_number'])

                # check for doubleheaders
                gamenum = np.unique(DF['game_pk'])
                if len(gamenum)>1:
                    for g in range(0,len(gamenum)):

                        if verbose>1: print('...double game!',end='')

                        # advance the team game counter by 1
                        gnum += 1

                        # zero out batting order numbers
                        game_ba = np.zeros(9)

                        # count the total number of at-bats
                        totalabs = len(np.unique(DF['at_bat_number'][DF['game_pk']==gamenum[g]]))

                        # loop through all at-bats in the game to determine the batting order count
                        for i in range(0,totalabs):
                            slot = int(i%9)
                            game_ba[slot] += 1

                        # figure out the opposing team
                        if DF['away_team'].values[0]==team:
                            wteam = DF['home_team'].values[0]
                        else:
                            wteam = DF['away_team'].values[0]

                        # populate the DF
                        AllGameDF.loc[offset+gnum-1] = pd.Series({'team':team,\
                                  'gamenum':gnum,\
                                  'opponent':wteam,\
                                  'date':date,\
                                  'opposinghandedness':DF['p_throws'][DF['at_bat_number']==np.nanmin(DF['at_bat_number'])].values[0],\
                                  'pa1':game_ba[0],\
                                  'pa2':game_ba[1],\
                                  'pa3':game_ba[2],\
                                  'pa4':game_ba[3],\
                                  'pa5':game_ba[4],\
                                  'pa6':game_ba[5],\
                                  'pa7':game_ba[6],\
                                  'pa8':game_ba[7],\
                                  'pa9':game_ba[8],\
                                  'dblheader':'true'\
                                  })

                    if verbose>1: print('')

                # single game days
                else:
                    # advance the team game counter by 1
                    gnum += 1

                    if verbose>1: print('...game!')

                    # zero out batting order numbers
                    game_ba = np.zeros(9)

                    # count the total number of at-bats
                    totalabs = len(np.unique(DF['at_bat_number']))

                    # loop through all at-bats in the game to determine the batting order count
                    for i in range(0,totalabs):
                        slot = int(i%9)
                        game_ba[slot] += 1


                    # figure out the opposing team
                    if DF['away_team'].values[0]==team:
                        wteam = DF['home_team'].values[0]
                    else:
                        wteam = DF['away_team'].values[0]

                    # populate the DF for this game
                    AllGameDF.loc[offset+gnum-1] = pd.Series({'team':team,\
                                  'gamenum':gnum,\
                                  'opponent':wteam,\
                                  'date':date,\
                                  'opposinghandedness':DF['p_throws'][DF['at_bat_number']==np.nanmin(DF['at_bat_number'])].values[0],\
                                  'pa1':game_ba[0],\
                                  'pa2':game_ba[1],\
                                  'pa3':game_ba[2],\
                                  'pa4':game_ba[3],\
                                  'pa5':game_ba[4],\
                                  'pa6':game_ba[5],\
                                  'pa7':game_ba[6],\
                                  'pa8':game_ba[7],\
                                  'pa9':game_ba[8],\
                                  'dblheader':'false'\
                                  })

            except: # no DF: skip to next game
                if verbose>1: print('')

        # keep track of total number of games
        offset += gnum

    return AllGameDF



# define a list of all MLB team shorthands
teams = ['LAA', 'HOU', 'OAK', 'TOR', 'ATL', 'MIL', 'STL','CHC', 'ARI', 'LAD', 'SF', 'CLE', 'SEA', 'MIA','NYM', 'WSH', 'BAL', 'SD', 'PHI', 'PIT', 'TEX','TB', 'BOS', 'CIN', 'COL', 'KC', 'DET', 'MIN','CWS', 'NYY']

# select a year to scrape
year = '2014'

AllGameDF = create_year_summary_df(year,teams,verbose=2)
AllGameDF.to_csv('data/games'+year+'.csv')


# for some sample applications, see accompanying files
