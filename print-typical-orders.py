
import numpy as np
import pandas as pd


teams = ['LAA', 'HOU', 'OAK', 'TOR', 'ATL', 'MIL', 'STL','CHC', 'ARI', 'LAD', 'SF', 'CLE', 'SEA', 'MIA','NYM', 'WSH', 'BAL', 'SD', 'PHI', 'PIT', 'TEX','TB', 'BOS', 'CIN', 'COL', 'KC', 'DET', 'MIN','CWS', 'NYY']

#teams = ['LAA','HOU']

year='2022'
AllRosterDF = pd.read_csv('data/player-batting-order-'+year+'.csv')



f = open('/Users/mpetersen/FantasyBaseball/fantasy-toolz.github.io/Lineups/lineup'+year+'.html','w')

hdr = '<!DOCTYPE html>\n<html>\n  <head>\n    <title>'+year+' Lineups</title>\n    <link rel="stylesheet" href="style.css" />\n    <meta charset="UTF-8">\n    <!--https://www.w3schools.com/css/css_table.asp-->\n  </head>\n\n  <body>\n  <h2>Batting Order Breakdown</h2>\n  <p>For each team, what is the "typical" '+year+' lineup, and how\n  frequently was each player in said lineup spot?</p>'
tail = '</body>\n</html>'

print(hdr,file=f)


for team in teams:
    typical_order = np.empty(9,dtype='S30')
    typical_value = np.zeros(9)
    tlist = np.array(AllRosterDF['player'][AllRosterDF['team']==team].values)
    nplayers = len(tlist)

    for plr in tlist:

        #print(plr,OrderDict[team][plr],np.nansum(OrderDict[team][plr]))


        #denom = 60.
        plrarray = AllRosterDF[(AllRosterDF['team']==team) & (AllRosterDF['player']==plr)]
        #print(plrarray)

        denom = 0.
        for o in range(0,9):
            denom += plrarray['b'+str(o+1)].values[0]
        #denom = np.nansum(OrderDict[team][plr])

        for o in range(0,9):
            #print(float(OrderDict[team][plr][o])/np.nansum(OrderDict[team][plr]))
            #print('values...',plrarray['b'+str(o+1)].values[0]/denom,typical_value[o],denom)
            if (plrarray['b'+str(o+1)].values[0]/denom >= typical_value[o]) & (denom>1.):
                #print(plr)
                typical_order[o] = plr.encode()
                try:
                    typical_value[o] = plrarray['b'+str(o+1)]/denom
                except:
                    pass

    #print('<br><h3><a href="figures/'+year+team+'order.png">',team,'</a></h3>',file=f)
    print('<br><h3>',team,'</h3>',file=f)
    print('<table id="customers">',file=f)
    print('<tr><th> Order </th><th> Player </th><th> Frequency (%) </th></tr>',file=f)
    for o in range(0,9):
        print('<tr><td>',o+1,'</td><td>',typical_order[o].decode(),'</td><td>',np.round(100.*typical_value[o],1),'</td></tr>',file=f)
        #print(o+1,typical_order[o].decode(),typical_value[o])


    print('</table>',file=f)


print(tail,file=f)

f.close()
