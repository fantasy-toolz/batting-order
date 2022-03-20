"""
predict-batting-order.py
  take a stab at what the batting order for a team would be, given the personnel.


RED SOX
player,position
"Bogaerts, Xander",SS
"Vázquez, Christian",C
"Story, Trevor",2B
"Dalbec, Bobby",1B
"Devers, Rafael",3B
"Martinez, J.D.",RF
"Bradley Jr., Jackie",CF
"Verdugo, Alex",LF
"Hernández, Enrique",OF

TWINS
player,position
"Correa, Carlos",SS
"Buxton, Byron",OF
"Kepler, Max",OF
"Sanó, Miguel",1B
"Urshela, Gio",3B
"Sánchez, Gary",DH
"Jeffers, Ryan",C
"Polanco, Jorge",2B
"Larnach, Trevor",OF
"Kirilloff, Alex",OF

CARDINALS
player,position
"Molina, Yadier",C
"Goldschmidt, Paul",1B
"Edman, Tommy",2B
"Arenado, Nolan",3B
"Sosa, Edmundo",SS
"DeJong, Paul",SS
"O'Neill, Tyler",OF
"Bader, Harrison",OF
"Carlson, Dylan",OF
"Yepez, Juan",DH

BLUE JAYS
player,position
"Kirk, Alejandro",C
"Guerrero Jr., Vladimir",1B
"Biggio, Cavan",2B
"Espinal, Santiago",3B
"Bichette, Bo",SS
"Gurriel Jr., Lourdes",OF
"Springer, George",OF
"Grichuk, Randall",OF
"Hernández, Teoscar",DH
"Chapman, Matt",3B
"Jansen, Danny",C

PHILLIES
player,position
"Realmuto, J.T.",C
"Hoskins, Rhys",1B
"Segura, Jean",2B
"Bohm, Alec",3B
"Gregorius, Didi",SS
"Vierling, Matt",OF
"Harper, Bryce",OF
"Schwarber, Kyle",OF
"Castellanos, Nick",DH

"""

import numpy as np
import pandas as pd
import unicodedata


# plotting basics
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# override some parameters for a 'house style'
import matplotlib as mpl
mpl.rcParams['xtick.labelsize'] = 10
mpl.rcParams['ytick.labelsize'] = 10
mpl.rcParams['font.weight'] = 'medium'
mpl.rcParams['axes.linewidth'] = 1.5
mpl.rcParams['xtick.major.width'] = 1.5
mpl.rcParams['xtick.minor.width'] = 0.75
mpl.rcParams['ytick.major.width'] = 1.5
mpl.rcParams['ytick.minor.width'] = 0.75
mpl.rcParams['xtick.minor.visible'] = True
mpl.rcParams['ytick.minor.visible'] = True

def print_lineup(AllRosterDF,AllGameDF,team,gamenum):
    """an example application that prints the roster for a given team by game number"""
    series  = AllRosterDF[(AllRosterDF['team']==team) & (AllRosterDF['gamenum']==gamenum)]
    series2 = AllGameDF[(AllGameDF['team']==team) & (AllGameDF['gamenum']==gamenum)]
    print(team,' v ',series2['opponent'].values[0],' on ',series2['date'].values[0])
    print('1',series['b1'].values[0])
    print('2',series['b2'].values[0])
    print('3',series['b3'].values[0])
    print('4',series['b4'].values[0])
    print('5',series['b5'].values[0])
    print('6',series['b6'].values[0])
    print('7',series['b7'].values[0])
    print('8',series['b8'].values[0])
    print('9',series['b9'].values[0])


# define a list of all MLB team shorthands
teams = ['LAA', 'HOU', 'OAK', 'TOR', 'ATL', 'MIL', 'STL','CHC', 'ARI', 'LAD', 'SF', 'CLE', 'SEA', 'MIA','NYM', 'WSH', 'BAL', 'SD', 'PHI', 'PIT', 'TEX','TB', 'BOS', 'CIN', 'COL', 'KC', 'DET', 'MIN','CWS', 'NYY']

year = '2021'
# bring in a DataFrame of interest:
AllGameDF = pd.read_csv('data/games'+year+'.csv')

# print a list of how many times the leadoff spot came up for each team
#for team in teams:
#    print(team,AllGameDF['pa1'][AllGameDF['team']==team].sum())

# print a list of all games between MIN and MIL
#print(AllGameDF[(AllGameDF['opponent']=='MIL') & (AllGameDF['team']=='MIN')]['date'].values)

# print all available information for a random game
#print(AllGameDF.loc[np.random.randint(0,162*30)])

# make a scatter plot of the ratio of first to ninth PAs, as a function of first PAs
#plt.figure(figsize=(4,4))

#for team in teams:
#    plt.scatter(AllGameDF['pa1'][AllGameDF['team']==team].sum(),\
#    AllGameDF['pa1'][AllGameDF['team']==team].sum()/AllGameDF['pa9'][AllGameDF['team']==team].sum(),color='black')

#plt.xlabel('1st spot PAs')
#plt.ylabel('1st/9th spot ratio')
#plt.tight_layout()
#plt.savefig('figures/first-last-ratio-2018.png')



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



# bring in all rosters from the teams:
AllRosterDF = pd.read_csv('data/team-batting-order-'+year+'.csv')

#print_lineup(AllRosterDF,AllGameDF,'MIN',125)


# plan:
# you introduce a 9-player (or 9+ player) list.
# the algorithm will spit out plausible options based on where players batted in previous years.

inputfile = '/Users/MSP/Downloads/teamlist.csv'

Lineup = pd.read_csv(inputfile)
#print(Lineup['player'])

AllPlayerDF = pd.read_csv('data/player-batting-order-'+year+'.csv')

#PlayerDF = AllPlayerDF[AllPlayerDF['player']==player]

PlayerOptions = dict()
PlayerCount = dict()
for spot in range(1,10):
    PlayerOptions[spot] = []
    PlayerCount[spot] = []

for pl in Lineup['player'].values:
    DF = AllPlayerDF[AllPlayerDF['player']==pl]
    print(pl,DF)
    for spot in range(1,10):
        if DF['b{}'.format(spot)].values[0]>0.:
            PlayerOptions[spot].append(pl)
            plrtot = np.nansum(np.array([DF['b{}'.format(x)].values[0] for x in range(1,10)]))
            PlayerCount[spot].append((DF['b{}'.format(spot)].values[0])/plrtot)

#print(PlayerOptions)
#print(PlayerCount)



AllArray = dict()
LineupScore = dict()
lineupnum = 0
for spot in range(1,10):
    #print(spot)
    lineupnum = 0
    AllArray[spot] = dict()
    LineupScore[spot] = dict()
    if spot==1:
        for pnum in range(0,len(PlayerOptions[spot])):
            AllArray[spot][lineupnum] = [PlayerOptions[spot][pnum]]
            LineupScore[spot][lineupnum] = PlayerCount[spot][pnum]
            lineupnum += 1
    else:

        for lnum in range(0,len(AllArray[spot-1].keys())):
            for pnum in range(0,len(PlayerOptions[spot])):
                #print(PlayerOptions[spot][pnum])
                #print(AllArray[spot-1][lnum])
                if PlayerOptions[spot][pnum] not in AllArray[spot-1][lnum]:
                    AllArray[spot][lineupnum] = [*AllArray[spot-1][lnum],*[PlayerOptions[spot][pnum]]]#[x for x in AllArray[spot-1][lnum]].append([PlayerOptions[spot][pnum]])
                    LineupScore[spot][lineupnum] = LineupScore[spot-1][lnum] + PlayerCount[spot][pnum]
                    #print(AllArray[spot][lineupnum])
                    lineupnum += 1
    #print(spot,AllArray)

#print(AllArray[spot])
#print(LineupScore[spot].values())
vals = np.array(list(LineupScore[spot].values()))
#print(vals)
print(np.nanmax(vals),np.nanargmax(vals))
likelylineups = (-1.*vals).argsort()[0:10]

for lineup in likelylineups:
    print(np.round(vals[lineup]/9.,3),AllArray[spot][int(lineup+1)])
