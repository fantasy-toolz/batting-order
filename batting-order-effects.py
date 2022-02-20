


import numpy as np
import pandas as pd

from bs4 import BeautifulSoup
import requests

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
mpl.rcParams['xtick.minor.visible'] = False
mpl.rcParams['ytick.minor.visible'] = False


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


switchdict = dict()
switchdict['Cedric Mullins'] = 'Cedric Mullins II'
switchdict['Hyun Jin Ryu'] = 'Hyun-Jin Ryu'
switchdict['Kwang Hyun Kim'] = 'Kwang-hyun Kim'
switchdict['Alfonso Rivas'] = 'Alfonso Rivas III'
switchdict['Andrew Young'] = 'Andy Young'
switchdict['AJ Pollock'] = 'A.J. Pollock'
switchdict['J.C. Mejia'] = 'JC Mejia'
switchdict['DJ Stewart'] = 'D.J. Stewart'
switchdict['Ha-Seong Kim'] = 'Ha-seong Kim'
switchdict['JD Hammer'] = 'J.D. Hammer'
switchdict['TJ Friedl'] = 'T.J. Friedl'

basedir = ''

# bring in all statistical data
for year in ['2014','2015','2016','2017','2018','2019','2020','2021']:
    #print(year)
    df = pd.read_csv(basedir+'data/yearlystats-'+year+'.csv')
    df['year'] = year
    if year=='2014':
        AllPlayerStats = df
    else:
        AllPlayerStats = pd.concat([AllPlayerStats,df])

#print(PlayerStats.columns)
PlayerStats = AllPlayerStats[AllPlayerStats['Name']==player]
#print(PlayerStats)


# bring in batting order data
for year in ['2014','2015','2016','2017','2018','2019','2020','2021']:
    #print(year)
    df = pd.read_csv(basedir+'data/player-batting-order-'+year+'.csv')
    df['year'] = year
    if year == '2014':
        AllPlayerBO = df
    else:
        AllPlayerBO = pd.concat([AllPlayerBO,df])


PlayerBO = AllPlayerBO[AllPlayerBO['player']==rearrange_name(player)]
#print(PlayerBO)

names = [rearrange_name(x) for x in AllPlayerBO[AllPlayerBO['year']=='2021']['player'].values]
#print(names)

namevals = AllPlayerStats['Name'].values
