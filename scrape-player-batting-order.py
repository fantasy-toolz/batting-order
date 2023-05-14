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
from io import StringIO
import requests
import unicodedata



year = '2023'
date = '2023-04-07'
team = 'MIN'


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


yeardates = [str(pd.to_datetime(day, unit='D', origin=str(year))).split()[0] for day in range(88,365)]
alldates = yeardates[0:np.where(np.array(yeardates)==str(pd.to_datetime("today").date()))[0][0]]

teams = ['LAA', 'HOU', 'OAK', 'TOR', 'ATL', 'MIL', 'STL','CHC', 'AZ', 'LAD', 'SF', 'CLE', 'SEA', 'MIA','NYM', 'WSH', 'BAL', 'SD', 'PHI', 'PIT', 'TEX','TB', 'BOS', 'CIN', 'COL', 'KC', 'DET', 'MIN','CWS', 'NYY']

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



def record_game(datestring,gameorder,f):
    print(datestring,end=';',file=f)
    for plr in gameorder:
        print(strip_accents(plr),end=';',file=f)
    print('',file=f)

#OrderDictList = dict()
for team in teams:
    newflag = 0
    print(team)
    # check if the team has already been recorded
    try:
        f = pd.read_csv('data/2023/{}.csv'.format(team),delimiter=';')
        maxdate = f['date'].values[-1]
        firstdate = np.where(maxdate==np.array(alldates))[0][0]
        alldatesin = alldates[firstdate+1:]
        newflag = 1
        f = open('data/2023/{}.csv'.format(team),'a')
    except:
        alldatesin = alldates
        f = open('data/2023/{}.csv'.format(team),'w')
    if (newflag==0):
        print('date;lineup1;lineup2;lineup3;lineup4;lineup5;lineup6;lineup7;lineup8;lineup9;',file=f)
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



def load_orderdict(teams):
    OrderDictList = dict()
    for team in teams:
        OrderDictList[team] = dict()
        G = np.genfromtxt('batting-order/data/2023/{}.csv'.format(team),skip_header=1,delimiter=';',dtype='S20')
        ngames = len(G[:,0])
        for g in range(0,ngames):
            #print(G[g])
            OrderDictList[team][G[g][0].decode()] = [G[g][p].decode() for p in range(1,10)]
    return OrderDictList


OrderDictList = load_orderdict(teams)


TM = pd.read_csv('/Users/mpetersen/Downloads/TeamGuessesOpeningDay.csv')

TM = pd.read_csv('/Users/mpetersen/Downloads/TeamGuessesPreseason.csv')


def reverse_player(plr):
    nnames = plr.split(' ')
    if len(nnames)==2:
        return nnames[1]+', '+nnames[0]
    else:
        return nnames[1]+' '+nnames[2]+', '+nnames[0]


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
        print(overlap,overlap+within1)
        #print(lineup)
        if gameorder==lineup:
            print('MATCH!')
    print('{0:3s} MEAN: {1:4.2f}, (p/m1 {2:4.2f})'.format(team,(totaloverlap)/len(OrderDictList[team]),(totaloverlap+within1)/len(OrderDictList[team])))



def create_game_summary_df(year,teams,InputDates=dict(),verbose=2):

    # make blank dictionaries as workspaces
    OrderDict     = dict()
    OrderDictList = dict()
    ValidDates    = dict()

    for team in teams:

        # report progress
        if verbose>0: print(team)

        # generate extra dictionary space
        if team not in OrderDict.keys():
            OrderDict[team] = dict()
            OrderDictList[team] = []

        # typical day ranges
        #for day in range(90,285):
        #for day in range(94,145):
        #for day in range(94,100):
        for day in range(96,280):


            # convert day number to string for savant searching
            dayval = pd.to_datetime(day-1, unit='D', origin=str(year))
            date = str(dayval).split()[0]

            # no need to go past today's date
            if date == str(pd.to_datetime("today").date()):
                break

            if date in InputDates['date'].values:
                continue

            if date not in ValidDates.keys():
                ValidDates[date] = 0


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

                        # add the games played to the list for the day
                        ValidDates[date] += 1

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

                    # add the games played to the list for the day
                    ValidDates[date] += 1

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

    ndates = len(list(ValidDates.keys()))
    OutputDates = pd.DataFrame(columns=['date','ngames'],index=[i for i in range(0,ndates)])
    dnum = 0
    for d in ValidDates.keys():
        OutputDates.loc[dnum] = pd.Series({'date':d,'ngames':ValidDates[d]})
        dnum+=1

    return OrderDict,OrderDictList,OutputDates

def reorganise_orderdictlist(OrderDict,OrderDictList):
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

def merge_csvs(InputDates,InputGameDF,InputPlayerDF,ValidDates,AllGameDF,AllPlayerDF):

    # dates are easy, just apend
    ndates1 = InputDates['date'].size
    ndates2 = ValidDates['date'].size
    OutputDates = pd.DataFrame(columns=['date','ngames'],index=[i for i in range(0,ndates1+ndates2)])
    dnum = 0
    for i in range(0,ndates1):
        OutputDates.loc[dnum] = pd.Series({'date':InputDates['date'].values[i],'ngames':InputDates['ngames'].values[i]})
        dnum+=1
    for i in range(0,ndates2):
        OutputDates.loc[dnum] = pd.Series({'date':ValidDates['date'].values[i],'ngames':ValidDates['ngames'].values[i]})
        dnum+=1

    # game DF is straightforward too, also append


# define a list of all MLB team shorthands
teams = ['LAA', 'HOU', 'OAK', 'TOR', 'ATL', 'MIL', 'STL','CHC', 'ARI', 'LAD', 'SF', 'CLE', 'SEA', 'MIA','NYM', 'WSH', 'BAL', 'SD', 'PHI', 'PIT', 'TEX','TB', 'BOS', 'CIN', 'COL', 'KC', 'DET', 'MIN','CWS', 'NYY']

# select a year to scrape
year = '2023'

try:
    InputDates    = pd.read_csv('data/days-batting-order'+year+'.csv')
    InputGameDF   = pd.read_csv('data/team-batting-order-'+year+'.csv')
    InputPlayerDF = pd.read_csv('data/player-batting-order-'+year+'.csv')
    print(InputDates['date'].values)
except:
    InputDates = pd.DataFrame(columns=['date'],index=[0])
    InputDates.loc[0] = pd.Series({'date':'nan'})

print(InputDates['date'].size)

OrderDict,OrderDictList,ValidDates = create_game_summary_df(year,teams,InputDates=InputDates,verbose=2)
AllGameDF,AllPlayerDF = reorganise_orderdictlist(OrderDict,OrderDictList)

# now merge the inputs

AllGameDF.to_csv('data/team-batting-order-'+year+'.csv')
AllPlayerDF.to_csv('data/player-batting-order-'+year+'.csv')
ValidDates.to_csv('data/days-batting-order'+year+'.csv')


# for some sample applications, see accompanying files
