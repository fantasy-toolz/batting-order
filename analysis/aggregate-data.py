

import pandas as pd


year = '2023'
outdir = ''
outdir = 'Preseason/'



teams = ['LAA', 'HOU', 'OAK', 'TOR', 'ATL', 'MIL', 'STL','CHC', 'AZ', 'LAD', 'SF', 'CLE', 'SEA', 'MIA','NYM', 'WSH', 'BAL', 'SD', 'PHI', 'PIT', 'TEX','TB', 'BOS', 'CIN', 'COL', 'KC', 'DET', 'MIN','CWS', 'NYY']


DF = pd.read_csv('data/{}{}/{}.csv'.format(outdir,year,teams[0]))
DF['team'] = teams[0]
DF.pop('Unnamed: 10')

for team in teams[1:]:
    DF2 = pd.read_csv('data/{}{}/{}.csv'.format(outdir,year,team))
    DF2['team'] = team
    DF2.pop('Unnamed: 10')
    DF = pd.concat([DF,DF2])

DF.to_csv('data/{}Aggregate/{}-all-lineups.csv'.format(outdir,year),index=False)