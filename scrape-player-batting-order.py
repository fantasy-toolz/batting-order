"""
scrape-player-batting-order
  a script to create a DataFrame with all the information we want:
  -team
  -game rosters
  -number of starts at each batting order for each player

  this routine is expensive: we heartily recommend that you use the already-processed csv files in data/!

"""

import numpy as np
import pandas as pd


def create_game_summary_df(year,teams,verbose=2):

    # make blank dictionaries as workspaces
    OrderDict     = dict()
    OrderDictList = dict()

    for team in teams:

        # report progress
        if verbose>0: print(team)

        # generate extra dictionary space
        if team not in OrderDict.keys():
            OrderDict[team] = dict()
            OrderDictList[team] = []

        # typical day ranges
        for day in range(90,285):

            # convert day number to string for savant searching
            dayval = pd.to_datetime(day-1, unit='D', origin=str(year))
            date = str(dayval).split()[0]

            # report progress
            if verbose>1: print(date,end='')

            try:
                # the workhorse: use pandas to retrieve a csv of the game data from MLB's statcast data repository
                # working string (30 Jan 2022)...not guaranteed to be infallible
                link = 'https://baseballsavant.mlb.com/statcast_search/csv?all=true&hfPT=&hfAB=&hfGT=R%7C&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfPull=&hfC=&hfSea='+str(year)+'%7C&hfSit=&player_type=batter&hfOuts=&opponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt='+date+'&game_date_lt='+date+'&hfInfield=&team='+team+'&position=&hfOutfield=&hfRO=&home_road=&hfFlag=&hfBBT=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=pitches&player_event_sort=api_p_release_speed&sort_order=desc&min_pas=0&type=details&'
                DF = pd.read_csv(link, low_memory=False)


                # check for doubleheaders
                gamenum = np.unique(DF['game_pk'])
                if len(gamenum)>1:

                    # loop through doubleheader games
                    for g in range(0,len(gamenum)):

                        # make a blank roster
                        gameorder = []

                        # count the number of at bats
                        totalabs = np.nanmax(DF['at_bat_number'][DF['game_pk']==gamenum[g]])

                        # report
                        if verbose>1: print('...double game!',end='')

                        # start the batting order counter
                        order = 0

                        # loop through at bats
                        for num in range(0,totalabs):

                            # who is up to bat?
                            plr = DF['player_name'][(DF['at_bat_number']==num) & (DF['game_pk']==gamenum[g])]
                            try:
                                # check if the at bat ended in an outcome
                                eve = DF['events'][(DF['at_bat_number']==num)]

                                # if not a valid outcome (e.g. caught stealing), skip this at bat
                                if len(eve)==np.sum(eve.isna()):
                                    continue

                                # if the player has not been logged before, create a log:
                                if np.unique(plr)[0] not in OrderDict[team].keys():
                                    OrderDict[team][np.unique(plr)[0]] = np.zeros(9)

                                # if roster is not complete, add player to roster
                                if order<9:
                                    # count the start for the player
                                    OrderDict[team][np.unique(plr)[0]][order] += 1

                                    # add the player to the game roster
                                    gameorder.append(np.unique(plr)[0])

                                # advance the batting order position
                                order +=1

                                # if the roster is full, move on to the next game
                                if order==9:
                                    break
                            except:
                                pass

                        # add the roster to the team's game list
                        OrderDictList[team].append(gameorder)

                    if verbose>1: print()

                # if NOT a double header
                else:

                    # count total number of at bats
                    totalabs = np.nanmax(DF['at_bat_number'])

                    # report
                    if verbose>1: print('...game!')

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

                            # if the player has not been logged before, create a blank array for batting order
                            if np.unique(plr)[0] not in OrderDict[team].keys():
                                OrderDict[team][np.unique(plr)[0]] = np.zeros(9)

                            # advance through early at bats
                            if order<9:

                                # tally the start for the player
                                OrderDict[team][np.unique(plr)[0]][order] += 1

                                # add the player to the daily roster
                                gameorder.append(np.unique(plr)[0])

                            # if we logged the batting order, advance one roster position
                            order +=1

                            # break the loop if we have the full roster already
                            if order==9:
                                break#order=1
                        except:
                            pass

                    # add the roster to the team's list
                    OrderDictList[team].append(gameorder)
            except:
                if verbose>1: print()

    # restructure outputs in to DataFrames

    # how many players did we log?
    tgames = 0
    for team in OrderDictList.keys():
        tgames += len(OrderDictList[team])

    # log all rosters
    AllGameDF = pd.DataFrame(columns=['team','gamenum','b1','b2','b3','b4','b5','b6','b7','b8','b9'],index=[i for i in range(0,tgames)])

    gnum = 0
    for team in OrderDictList.keys():
        for gamenum in range(0,len(OrderDictList[team])):
            AllGameDF.loc[gnum] = pd.Series({'gamenum':gamenum+1,\
                                               'team':team,\
                                               'b1':OrderDictList[team][gamenum][0],\
                                               'b2':OrderDictList[team][gamenum][1],\
                                               'b3':OrderDictList[team][gamenum][2],\
                                               'b4':OrderDictList[team][gamenum][3],\
                                               'b5':OrderDictList[team][gamenum][4],\
                                               'b6':OrderDictList[team][gamenum][5],\
                                               'b7':OrderDictList[team][gamenum][6],\
                                               'b8':OrderDictList[team][gamenum][7],\
                                               'b9':OrderDictList[team][gamenum][8]})
            gnum+=1


    # how many players did we log?
    tplayers = 0
    for team in OrderDict.keys():
        tplayers += len(list(OrderDict[team].keys()))

    # make the DataFrame to hold each player
    AllPlayerDF = pd.DataFrame(columns=['player','team','b1','b2','b3','b4','b5','b6','b7','b8','b9'],index=[i for i in range(0,tplayers)])

    pnum = 0
    for team in OrderDict.keys():
        for player in OrderDict[team].keys():
            AllPlayerDF.loc[pnum] = pd.Series({'player':player,\
                                               'team':team,\
                                               'b1':OrderDict[team][player][0],\
                                               'b2':OrderDict[team][player][1],\
                                               'b3':OrderDict[team][player][2],\
                                               'b4':OrderDict[team][player][3],\
                                               'b5':OrderDict[team][player][4],\
                                               'b6':OrderDict[team][player][5],\
                                               'b7':OrderDict[team][player][6],\
                                               'b8':OrderDict[team][player][7],\
                                               'b9':OrderDict[team][player][8]})
            pnum+=1


    return AllGameDF,AllPlayerDF




# define a list of all MLB team shorthands
teams = ['LAA', 'HOU', 'OAK', 'TOR', 'ATL', 'MIL', 'STL','CHC', 'ARI', 'LAD', 'SF', 'CLE', 'SEA', 'MIA','NYM', 'WSH', 'BAL', 'SD', 'PHI', 'PIT', 'TEX','TB', 'BOS', 'CIN', 'COL', 'KC', 'DET', 'MIN','CWS', 'NYY']

# select a year to scrape
year = '2014'

AllGameDF,AllPlayerDF = create_game_summary_df(year,teams,verbose=2)
AllGameDF.to_csv('data/team-batting-order-'+year+'.csv')
AllPlayerDF.to_csv('data/player-batting-order-'+year+'.csv')


# for some sample applications, see accompanying files
