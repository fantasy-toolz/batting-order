

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


player = 'Ronald Acuna Jr.'

years = ['2020','2021','2022','2023']

# get into stat-scraping
# import stat_scraping as ss
# year = '2022'
# DF = ss.scrape_fangraphs_leaders('bat', year = 2022, data_type = 'Standard', agg_type='Player', split=0)
# DF.to_csv('/Users/mpetersen/FantasyBaseball/batting-order/data/yearlystats-'+year+'.csv')

# bring in all statistical data
for year in years:
    #print(year)
    df = pd.read_csv('data/Aggregate/yearlystats-'+year+'.csv')
    print(year)

    for x in df['Name'].values:
        try:
            #print(x)
            #print(strip_accents(x))
            df['Name'][df['Name']==x] = strip_accents(x)
        except:
            pass

    df['year'] = year
    if year==years[0]:
        AllPlayerStats = df
    else:
        AllPlayerStats = pd.concat([AllPlayerStats,df])

#print(PlayerStats.columns)
PlayerStats = AllPlayerStats[AllPlayerStats['Name']==player]
#print(PlayerStats)


# bring in batting order data
for year in years:
    #print(year)
    df = pd.read_csv('data/Aggregate/player-batting-order-'+year+'.csv')

    keyvals = ['b1','b2','b3','b4','b5','b6','b7','b8','b9']
    for k in keyvals:
        for x in df[k].values:
            try:
                #print(strip_accents(x))
                df[k][df[k]==x] = strip_accents(x)
            except:
                pass

    df['year'] = year
    if year == years[0]:
        AllPlayerBO = df
    else:
        AllPlayerBO = pd.concat([AllPlayerBO,df])

PlayerBO = AllPlayerBO[AllPlayerBO['player']==rearrange_name(player)]
print(PlayerBO)

names = [rearrange_name(x) for x in AllPlayerBO[AllPlayerBO['year']=='2023']['player'].values]
print(names)

namevals = AllPlayerStats['Name'].values

# a few hand replacements, sadly.
# these are for guys who have a different name in the order record and on fangraphs
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
switchdict['Luis Robert Jr.'] = 'Luis Robert'
switchdict['Luis Robert'] = 'Luis Robert Jr.'


def project_three_year_average(AllPlayerStatsDF,year,player,stat='PA',minusyears=3):
    years = [str(year-i) for i in range(1,minusyears+1)]
    #print(years)
    #print(AllPlayerStatsDF[AllPlayerStatsDF['year'].isin(years)])
    dftmp = AllPlayerStatsDF[(AllPlayerStatsDF['Name'].values==player) & (AllPlayerStatsDF['year'].isin(years))]

    threeyearmean = 0.
    yearnum = 0.
    for year in years:
        try:
            if year == '2020':
                threeyearmean += dftmp[dftmp['year']==year][stat].values[0]*(162./60.)
                yearnum += 1.
            else:
                threeyearmean += dftmp[dftmp['year']==year][stat].values[0]
                yearnum += 1.
        except:
            pass

    if yearnum > 0:
        return np.round(threeyearmean/yearnum)
    else:
        return 0.

def batting_position_stats(AllPlayerBODF,player,year=-1):
    if year==-1:
        plrdf = AllPlayerBODF[AllPlayerBODF['player']==player]
        for yearval in plrdf['year'].values:
            df = plrdf[plrdf['year'] == yearval]
            print(yearval,np.nansum([1.*df['b1'],2.*df['b2'],3.*df['b3'],\
                                     4.*df['b4'],5.*df['b5'],6.*df['b6'],\
                                     7.*df['b7'],8.*df['b8'],9.*df['b9']])/\
                          np.nansum([1.*df['b1'],1.*df['b2'],1.*df['b3'],\
                                     1.*df['b4'],1.*df['b5'],1.*df['b6'],\
                                     1.*df['b7'],1.*df['b8'],1.*df['b9']]))
    else:
        plrdf = AllPlayerBODF[AllPlayerBODF['player']==player]
        df = plrdf[plrdf['year'] == year]
        return np.nansum([1.*df['b1'],2.*df['b2'],3.*df['b3'],\
                                     4.*df['b4'],5.*df['b5'],6.*df['b6'],\
                                     7.*df['b7'],8.*df['b8'],9.*df['b9']])/\
                          np.nansum([1.*df['b1'],1.*df['b2'],1.*df['b3'],\
                                     1.*df['b4'],1.*df['b5'],1.*df['b6'],\
                                     1.*df['b7'],1.*df['b8'],1.*df['b9']])






f = open('data/Aggregate/three_year_batting_stats_2021-2023.csv','w')
print('player,threeyearG,threeyearPA,battingpos2023,2023modelPAs162',file=f)

print('And now, missing players:')


for iname,name in enumerate(names):
    print(iname,name)
    compname = strip_accents(name.lstrip())
    if compname in switchdict.keys():
        compname = switchdict[compname]
    w = namevals[namevals==compname]
    #print(w)
    if len(w)==0:
        print(compname)
    #if compname == 'Wil Myers':
        #print(AllPlayerStats[AllPlayerStats['Name']==compname])
    projectedG = project_three_year_average(AllPlayerStats,2023,compname,stat='G',minusyears=3)
    projectedPA = project_three_year_average(AllPlayerStats,2023,compname,stat='PA',minusyears=3)

    outpos = np.round(batting_position_stats(AllPlayerBO,rearrange_name(compname),year='2023'),2)
    #if np.isnan(outpos):
        #print(compname,rearrange_name(compname))

    paguess = np.round(2*(-9*outpos+380),0)

    #if np.isfinite(outpos):
    print('{0},{1},{2},{3},{4}'.format(name,projectedG,projectedPA,outpos,paguess),file=f)

f.close()

#for p in np.unique(AllPlayerBO['player']):    print(p)

for n in names: print(n)

T = pd.read_csv('predictions/lineups-2024-01-22.csv')

#for l in range(1,12):
#print(np.array(T['Lineup{}'.format(l)].values))

f = open('data/Aggregate/estimated_batting_stats_2024.csv','w')
print('player,PAprediction,threeyearavgPA,PA23,lineup23,PA23lineup,PA24lineup,threeyearavgG,G23,G22,G21',file=f)

nplayers = 0
for iname,name in enumerate(names):
    compname = strip_accents(name.lstrip())
    if compname in switchdict.keys():
        compname = switchdict[compname]


    outpos = np.round(batting_position_stats(AllPlayerBO,rearrange_name(compname),year='2023'),2)
    PA23lineup = np.round(2*(-9*outpos+380),0)
    lineup23 = outpos

    threeyearavgG  = project_three_year_average(AllPlayerStats,2023,compname,stat='G',minusyears=3)
    threeyearavgPA = project_three_year_average(AllPlayerStats,2023,compname,stat='PA',minusyears=3)
    totalG23       = project_three_year_average(AllPlayerStats,2023,compname,stat='G',minusyears=1)
    totalG22       = project_three_year_average(AllPlayerStats,2022,compname,stat='G',minusyears=1)
    totalG21       = project_three_year_average(AllPlayerStats,2021,compname,stat='G',minusyears=1)
    PAtotal23      = project_three_year_average(AllPlayerStats,2023,compname,stat='PA',minusyears=1)

    # check all hand-set lineup locations: set default as bottom of the order
    outpos = 9.0
    for l in range(1,12):
        nameset = np.array(T['Lineup{}'.format(l)].values)

        w = nameset[nameset==compname]#[0]
        if len(w)>0:
            nplayers += 1
            #print(l,compname)
            outpos = l

    PA24lineup = np.round(2*(-9*outpos+380),0)

    print('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}'.format(compname,int(np.round(PA24lineup*(totalG23/162.),0)),\
                                               threeyearavgPA,PAtotal23,lineup23,PA23lineup,PA24lineup,threeyearavgG,
                                               totalG23,totalG22,totalG21),file=f)


f.close()
print(nplayers)

