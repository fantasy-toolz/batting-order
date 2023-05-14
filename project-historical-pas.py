

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


player = 'Wil Myers'

# bring in all statistical data
for year in ['2014','2015','2016','2017','2018','2019','2020','2021']:
    #print(year)
    df = pd.read_csv('data/yearlystats-'+year+'.csv')
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
    df = pd.read_csv('data/player-batting-order-'+year+'.csv')
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

# a few hand replacements, sadly.
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


def project_three_year_average(AllPlayerStatsDF,year,player,minusyears=3):
    years = [str(year-i) for i in range(1,minusyears+1)]
    #print(years)
    #print(AllPlayerStatsDF[AllPlayerStatsDF['year'].isin(years)])
    dftmp = AllPlayerStatsDF[(AllPlayerStatsDF['Name'].values==player) & (AllPlayerStatsDF['year'].isin(years))]

    threeyearmean = 0.
    yearnum = 0.
    for year in years:
        try:
            if year == '2020':
                threeyearmean += dftmp[dftmp['year']==year]['PA'].values[0]*(162./60.)
                yearnum += 1.
            else:
                threeyearmean += dftmp[dftmp['year']==year]['PA'].values[0]
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


qyears = ['2021','2020','2019','2018','2017']
projectedtotal = np.zeros([len(names),len(qyears)])

pafloor = 300.
yearaverage = 3
dpa = 150.

for yearaverage in [1,2,3]:
    for pafloor in [0.,150.,300.,450.,600.]:
        for iname,name in enumerate(names):
            compname = strip_accents(name.lstrip())
            if compname in switchdict.keys():
                compname = switchdict[compname]
            w = namevals[namevals==compname]
            if len(w)==0:
                print(compname)
            #if compname == 'Wil Myers':
                #print(AllPlayerStats[AllPlayerStats['Name']==compname])
            for iyear,year in enumerate(qyears):
                    projected = project_three_year_average(AllPlayerStats,int(year),compname,minusyears=yearaverage)
                    try:
                        actual    = AllPlayerStats[(AllPlayerStats['Name']==compname) & (AllPlayerStats['year']==year)]['PA'].values[0]
                    except:
                        actual    = 0.

                    if year == '2020':
                        actual *= (162./60.)
                    if (actual > 0) & (projected > pafloor) & (projected < pafloor+dpa):
                        #print(compname,year,projected,actual)
                        projectedtotal[iname,iyear] = (projected-actual)/actual
                        #projectedtotal[iname,iyear] = (actual-projected)/projected
                    else:
                        projectedtotal[iname,iyear] = np.nan
                #print(batting_position_stats(AllPlayerBO,rearrange_name(compname)))


        # make the key assumption that 2020 is prorated from 60 games -> 162 games


        # can start by considering all 2021 players...where did they bat in previous years? How similar are they?

        # make a couple plots
        plt.figure()
        for iyear,year in enumerate(qyears):
            # get the guys who aren't nans
            valid_comparison_guys = projectedtotal[np.isfinite(projectedtotal[:,iyear]),iyear]
            sortedarr  = valid_comparison_guys[valid_comparison_guys.argsort()]
            nsortedarr = np.linspace(0.,1.,len(valid_comparison_guys))
            plt.plot(sortedarr,nsortedarr,color=cm.viridis(iyear/4.,1.),lw=1.,label=year+' (N={})'.format(len(valid_comparison_guys)))

        plt.plot([0.,0.],[0.,1.0],color='grey',linestyle='dashed',lw=1.)
        plt.plot([-1.5,1.5],[0.5,0.5],color='grey',linestyle='dashed',lw=1.)

        plt.title('(projected-actual)\n/actual')
        plt.legend()
        plt.axis([-1.5,1.5,0.,1.])
        plt.xlabel('PA difference')
        plt.ylabel('Cumulative number')
        plt.tight_layout()

        plt.savefig('figures/compare_{}year_projected_pas_min{}.png'.format(yearaverage,int(pafloor)))
