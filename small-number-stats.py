


import numpy as np
import pandas as pd

from bs4 import BeautifulSoup
import requests

import unicodedata

# plotting basics
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import namecorrections

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
mpl.rcParams['xtick.minor.visible'] = False
mpl.rcParams['ytick.minor.visible'] = False


basedir = ''
player = 'C.J. Cron'
year = '2022'


PSdf = pd.read_csv("../Rankings2022/predictions/AllPitching_2022_2022.csv")

#PlayerStats = PSdf[PSdf['Name']==player]
#print(PlayerStats)

allplayers = PSdf['Name']
hrrate = np.zeros(allplayers.size)
hrnum = np.zeros(allplayers.size)
panum = np.zeros(allplayers.size)

stat = 'HR'

for ip,player in enumerate(allplayers):
    try:
        hrrate[ip] = PSdf[PSdf['Name']==player][stat].values[0]/PSdf[PSdf['Name']==player]['TBF'].values[0]
        hrnum[ip] = PSdf[PSdf['Name']==player][stat].values[0]
        panum[ip] = PSdf[PSdf['Name']==player]['TBF'].values[0]
    except:
        pass

#print(hrrate)
plrsort = (hrrate).argsort()

tbfloor=30.
nplr = 0.
for ip in plrsort[0:100]:
    if panum[ip]>tbfloor:
        print('{0:30s} {1:4.3f} {2:3d} {3:3d}'.format(allplayers[ip],hrrate[ip],int(hrnum[ip]),int(panum[ip])))
        nplr += 1.
    if nplr > 10:
        break

"""

# bring in all statistical data
PSdf = pd.read_csv(basedir+'data/yearlystats-'+year+'.csv')

#PlayerStats = PSdf[PSdf['Name']==player]
#print(PlayerStats)

allplayers = PSdf['Name']
hrrate = np.zeros(allplayers.size)
hrnum = np.zeros(allplayers.size)
panum = np.zeros(allplayers.size)

stat = 'H'

for ip,player in enumerate(allplayers):
    try:
        hrrate[ip] = PSdf[PSdf['Name']==player][stat].values[0]/PSdf[PSdf['Name']==player]['PA'].values[0]
        hrnum[ip] = PSdf[PSdf['Name']==player][stat].values[0]
        panum[ip] = PSdf[PSdf['Name']==player]['PA'].values[0]
    except:
        pass

#print(hrrate)
plrsort = (-1.*hrrate).argsort()

for ip in plrsort[0:10]:
    print('{0:30s} {1:4.3f} {2:3d} {3:3d}'.format(allplayers[ip],hrrate[ip],int(hrnum[ip]),int(panum[ip])))


# bring in batting order data
BOdf = pd.read_csv(basedir+'data/player-batting-order-'+year+'.csv')
PlayerBO = BOdf[BOdf['player']==namecorrections.rearrange_name(player)]
#print(PlayerBO)
"""

"""
HR
Danny Jansen                   0.250   2   8
Austin Barnes                  0.200   2  10
C.J. Cron                      0.128   5  39
Vladimir Guerrero Jr.          0.125   5  40
Alan Trejo                     0.125   1   8
Albert Pujols                  0.118   2  17
Jonah Heim                     0.118   2  17
Byron Buxton                   0.115   3  26
Seiya Suzuki                   0.114   4  35
Nolan Arenado                  0.114   4  35

RBI
Alan Trejo                     0.625   5   8
Luke Williams                  0.600   3   5
Jonah Heim                     0.471   8  17
Jose Ramirez                   0.375  15  40
Jazz Chisholm Jr.              0.370  10  27
Charlie Culberson              0.364   4  11
Nolan Arenado                  0.343  12  35
Cam Gallagher                  0.333   1   3
Francisco Mejia                0.333   7  21
Michael Chavis                 0.333   6  18

R
Kyle Isbel                     1.000   1   1
Tom Murphy                     0.545   6  11
Lars Nootbaar                  0.400   2   5
Danny Jansen                   0.375   3   8
Jon Berti                      0.364   4  11
Charlie Culberson              0.364   4  11
Jonah Heim                     0.353   6  17
Dee Strange-Gordon             0.333   1   3
Ha-seong Kim                   0.333   7  21
Marwin Gonzalez                0.333   1   3

SB
Edward Olivares                0.333   1   3
Daz Cameron                    0.250   1   4
Jose Azocar                    0.250   1   4
Travis Jankowski               0.154   2  13
Eli White                      0.143   1   7
Luis Robert                    0.135   5  37
Adam Engel                     0.111   2  18
Steven Duggar                  0.111   3  27
Adalberto Mondesi              0.103   3  29
Jose Trevino                   0.100   1  10

H
A.J. Pollock                   0.571   4   7
Danny Jansen                   0.500   4   8
Yonathan Daza                  0.500   6  12
Jose Trevino                   0.500   5  10
Alfonso Rivas III              0.500   2   4
Michael Chavis                 0.444   8  18
Owen Miller                    0.424  14  33
Alec Bohm                      0.412   7  17
Jonathan Villar                0.409   9  22
Austin Barnes                  0.400   4  10

ER (worst)
Duane Underwood Jr.            1.000   1   1
Travis Lakins Sr.              0.500   4   8
Mike Mayers                    0.455   5  11
Caleb Thielbar                 0.438   7  16
Kolby Allard                   0.417   5  12
Brian Moran                    0.400   2   5
Cody Stashak                   0.400   2   5
Spencer Howard                 0.400   6  15
Brett Phillips                 0.400   4  10
Wil Myers                      0.400   2   5

(tbf limit)
Hyun-Jin Ryu                   0.314  11  35
Trevor Rogers                  0.257   9  35
Freddy Peralta                 0.243   9  37
Nick Pivetta                   0.229   8  35
Jose Berrios                   0.226   7  31
Kyle Freeland                  0.217  10  46
Joan Adon                      0.213  10  47
Reid Detmers                   0.206   7  34
JT Brubaker                    0.205   8  39
Zack Wheeler                   0.200   8  40
Chris Mazza                    0.200   7  35

No BB
Tylor Megill                   0.000   0  36
Joe Musgrove                   0.000   0  45
Kevin Gausman                  0.000   0  45

No HR
Drew Hutchison                 0.000   0  31
Miles Mikolas                  0.000   0  43
Zack Greinke                   0.000   0  43
Patrick Corbin                 0.000   0  60
Adrian Houser                  0.000   0  41
Brandon Woodruff               0.000   0  41
Shane Bieber                   0.000   0  37
Justin Steele                  0.000   0  38
Paul Blackburn                 0.000   0  38
Dylan Cease                    0.000   0  41
Trevor Rogers                  0.000   0  35

"""
