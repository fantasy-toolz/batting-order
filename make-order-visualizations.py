
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm


mpl.rcParams['xtick.minor.visible'] = False
mpl.rcParams['ytick.minor.visible'] = False

teams = ['LAA', 'HOU', 'OAK', 'TOR', 'ATL', 'MIL', 'STL','CHC', 'ARI', 'LAD', 'SF', 'CLE', 'SEA', 'MIA','NYM', 'WSH', 'BAL', 'SD', 'PHI', 'PIT', 'TEX','TB', 'BOS', 'CIN', 'COL', 'KC', 'DET', 'MIN','CWS', 'NYY']

year='2022'
#AllRosterDF = pd.read_csv('data/player-batting-order-'+year+'.csv')
TeamRosterDF = pd.read_csv('data/team-batting-order-'+year+'.csv')



def make_teamgrid(team,TeamRosterDF,f,plot=False):

    # get the list of lineups
    nlineups = len(TeamRosterDF[TeamRosterDF['team']==team])

    teamgrid = np.zeros([nlineups,nlineups])

    for g1 in range(0,nlineups):
        gamelineup1 = TeamRosterDF[(TeamRosterDF['team']==team) & (TeamRosterDF['gamenum']==g1+1)]
        for g2 in range(g1,nlineups):
            gamelineup2 = TeamRosterDF[(TeamRosterDF['team']==team) & (TeamRosterDF['gamenum']==g2+1)]
            #print(gamelineup1,gamelineup2)
            for indx1 in range(0,9):
                if gamelineup1['b'+str(indx1+1)].values[0]==gamelineup2['b'+str(indx1+1)].values[0]:
                #if OrderDictList[team][g1][indx1]==OrderDictList[team][g2][indx1]:
                    teamgrid[g1][g2]+=1#np.nan
                    teamgrid[g2][g1]+=1
                if g1==g2:
                    teamgrid[g1][g2]+=np.nan

    if plot:
        plt.figure()
        plt.imshow(teamgrid,cmap=cm.viridis,vmin=0.,vmax=9.)
        plt.colorbar()

    # then select the lineup that has the most overlap with other lineups
    #print(np.nansum(teamgrid,axis=0)/len(OrderDictList[team]))
    # wherever this is maximised is the typical lineup
    simscore = np.nansum(teamgrid,axis=0)/nlineups

    # can also tweak this so it's more recent...
    simlineup = np.nanargmax(simscore)
    # could also use to quantify how volatile a team's lineup setup is
    volatility = np.nanmedian(simscore)

    # find the maximum from the recent 14 games, e.g.
    recent_games = 162
    simlineup = np.nanmax(np.where(simscore==np.nanmax(simscore[-recent_games:]))[0])
    volatility = np.nanmedian(simscore[-recent_games:])

    mostlikelylineup = TeamRosterDF[(TeamRosterDF['team']==team) & (TeamRosterDF['gamenum']==(simlineup+1))]

    #print('<tr><td><a href="figures/'+year+team+'order.png">{0}</a></td>'.format(team),end='',file=f)
    print('<tr><td>{0}</td>'.format(team),end='',file=f)
    for indx in range(0,9):

        print('<td>{0}</td>'.format(mostlikelylineup['b'+str(indx+1)].values[0]),end='',file=f)

        """
        # color if guy has been traded away from the team
        if (OrderDictList[team][simlineup][indx] in TradeList):
            if (team==OldTeam[np.where(OrderDictList[team][simlineup][indx]==np.array(TradeList))[0][0]]):
                print('<td style="color:#d63838">{0}</td>'.format(OrderDictList[team][simlineup][indx]),end='',file=f)
            else:
                print('<td>{0}*</td>'.format(OrderDictList[team][simlineup][indx]),end='',file=f)

        # set up a new color if the guy has been in the lineup fewer than X times
        elif (np.nansum(OrderDict[team][OrderDictList[team][simlineup][indx]]) <25):
            print('<td style="color:#696969">{0}</td>'.format(OrderDictList[team][simlineup][indx]),end='',file=f)

        # default
        else:
            print('<td>{0}</td>'.format(OrderDictList[team][simlineup][indx]),end='',file=f)
        """

    print('<td><a href="figures/'+year+team+'similarity.png">{0}</a></td><td>{1}</td></tr>'.format(np.round(volatility,2),simlineup+1),file=f)
    return mostlikelylineup,volatility


f = open('/Users/mpetersen/Projects/FantasyBaseball/webpage/fantasy-toolz.github.io/Lineups/lineup'+year+'.html','w')
#f = open('/Users/mpetersen/Projects/FantasyBaseball/webpage/fantasy-toolz.github.io/Lineups/lineup'+year+'posttrade.html','w')


searchable = "<script>\nwindow.onload=function(){ \nconst getCellValue = (tr, idx) => tr.children[idx].innerText || tr.children[idx].textContent;\nconst comparer = (idx, asc) => (a, b) => ((v1, v2) => \n    v1 !== '' && v2 !== '' && !isNaN(v1) && !isNaN(v2) ? v1 - v2 : v1.toString().localeCompare(v2)\n    )(getCellValue(asc ? a : b, idx), getCellValue(asc ? b : a, idx));\n// do the work...\ndocument.querySelectorAll('th').forEach(th => th.addEventListener('click', (() => {\n    const table = th.closest('table');\n    Array.from(table.querySelectorAll('tr:nth-child(n+2)'))\n        .sort(comparer(Array.from(th.parentNode.children).indexOf(th), this.asc = !this.asc))\n        .forEach(tr => table.appendChild(tr) );\n})));\n}\n</script>"
hdr = '<!DOCTYPE html>\n<html>\n  <head>\n    <title>'+year+' Lineups</title>\n    <link rel="stylesheet" href="style.css" />\n    <meta charset="UTF-8">\n    <!--https://www.w3schools.com/css/css_table.asp-->\n'+searchable+'  </head>\n\n  <body>\n  <h2>Batting Order Breakdown</h2>\n  <p>For each team, what is the "typical" '+year+' lineup?</p><p style="color:#d63838">Red colors mean the player is not on the team anymore.</p><p style="color:#696969">Grey colors mean the player has appeared in fewer than 25 games.</p>'
tail = '</body>\n</html>'

print(hdr,file=f)

#print('<br><h3><a href="figures/'+year+team+'order.png">',team,'</a></h3>',file=f)
print('<table id="customers">',file=f)
print('<tr><th>Team</th><th>1st</th><th>2nd</th><th>3rd</th><th>4th</th><th>5th</th><th>6th</th><th>7th</th><th>8th</th><th>9th</th><th>Similarity</th><th>First Appeared</th></tr>',file=f)

TV = {}
for team in teams:
    a,volatility = make_teamgrid(team,TeamRosterDF,f,plot=False)
    TV[team] = volatility


print('</table>',file=f)


print(tail,file=f)

f.close()



def make_teamgrid2(team,TeamRosterDF,f,plot=False,allprint=False):
    # get the list of lineups
    nlineups = len(TeamRosterDF[TeamRosterDF['team']==team])

    teamgrid = np.zeros([nlineups,nlineups])

    for g1 in range(0,nlineups):
        gamelineup1 = TeamRosterDF[(TeamRosterDF['team']==team) & (TeamRosterDF['gamenum']==g1+1)]
        for g2 in range(g1,nlineups):
            gamelineup2 = TeamRosterDF[(TeamRosterDF['team']==team) & (TeamRosterDF['gamenum']==g2+1)]
            #print(gamelineup1,gamelineup2)
            for indx1 in range(0,9):
                if gamelineup1['b'+str(indx1+1)].values[0]==gamelineup2['b'+str(indx1+1)].values[0]:
                #if OrderDictList[team][g1][indx1]==OrderDictList[team][g2][indx1]:
                    teamgrid[g1][g2]+=1#np.nan
                    teamgrid[g2][g1]+=1
                if g1==g2:
                    teamgrid[g1][g2]+=np.nan

    if plot:
        plt.figure()
        plt.imshow(teamgrid,cmap=cm.viridis,vmin=0.,vmax=9.)
        plt.title(team)
        plt.colorbar()
        plt.savefig('figures/2021'+team+'similarity.png',dpi=300)
        plt.savefig('/Users/mpetersen/Projects/FantasyBaseball/webpage/fantasy-toolz.github.io/Lineups/figures/2022'+team+'similarity.png',dpi=300)


    # then select the lineup that has the most overlap with other lineups
    #print(np.nansum(teamgrid,axis=0)/len(OrderDictList[team]))
    # wherever this is maximised is the typical lineup
    #simscore = np.nansum(teamgrid,axis=0)/len(OrderDictList[team])
    #simlineup = np.nanargmax(simscore)

    # could also use to quantify how volatile a team's lineup setup is
    #volatility = np.nanmedian(simscore)

    #print(OrderDictList[team][simlineup],simlineup)
    #return OrderDictList[team][simlineup],volatility



for team in teams:
    #if team=='SEA':
        #a,volatility =
        make_teamgrid2(team,TeamRosterDF,f,plot=True)


"""


# check who appears on multiple teams
# check which most recent lineups feature overlap with another team

TradeList = []
OldTeam   = []
NewTeam   = []

for t1 in teams:
    # how many games to go back to make sure we get pitchers who might hit?
    for g in range(-7,0):
        last_lineup = OrderDictList[t1][g]
        for t2 in teams:
            if t1==t2: continue
            for indx in range(0,9):
                if ((last_lineup[indx] in np.array(list(OrderDict[t2].keys()))[0:-7])):
                    if last_lineup[indx] not in TradeList:
                        TradeList.append(last_lineup[indx])
                        OldTeam.append(t2)
                        NewTeam.append(t1)
                        #print('Traded?',last_lineup[indx])

for i in range(0,len(TradeList)):
    print(OldTeam[i],NewTeam[i],TradeList[i])

year='2021'
AllRosterDF = pd.read_csv('data/player-batting-order-'+year+'.csv')

AllRosterDF[AllRosterDF['team']=='LAA']

team = 'LAA'
tlist = np.array(AllRosterDF['player'][AllRosterDF['team']==team].values)
nplayers = len(tlist)



AllRosterDF['player'][AllRosterDF['team']==team]


for team in teams:
    porder = np.zeros(len(OrderDict[team].keys()))
    pnames = np.empty(len(OrderDict[team].keys()),dtype='S30')
    tlist = np.array(list(OrderDict[team].keys()))

    for iplr,plr in enumerate(tlist[::-1]):
        #print(plr,OrderDict[team][plr],np.nansum(OrderDict[team][plr]))
        porder[iplr] = np.nansum(OrderDict[team][plr])
        pnames[iplr] = plr.encode()

    #for iplr in (-1*porder).argsort():
        #print(porder[iplr],pnames[iplr])

    fig = plt.figure(figsize=(6.5,9))
    ax = fig.add_axes([0.25,0.06,0.74,0.9])

    nplayers = len(OrderDict[team].keys())

    for ii,iplr in enumerate((porder).argsort()):
        #print(porder[iplr],pnames[iplr])
        ax.plot(np.arange(1,10,1),1.1*ii+1+OrderDict[team][pnames[iplr].decode()]/np.sum(OrderDict[team][pnames[iplr].decode()]),drawstyle='steps-mid',color=cm.viridis_r(ii/(nplayers-1)))
        ax.plot([1.,9.],[1.1*ii+1,1.1*ii+1],linestyle='dotted',lw=1.,color='grey')
        ax.text(8.6,1.1*ii+1.1,int(porder[iplr]),color=cm.viridis_r(ii/(nplayers-1)),size=12)


    ax.set_yticks(1.1*np.arange(1,nplayers+1,1))
    ax.set_yticklabels([d.decode() for d in pnames[(porder).argsort()]])
    ax.set_xticks(np.arange(1,10,1))
    ax.tick_params(axis="y",which='both',direction="in")
    ax.tick_params(axis="x",which='both',direction="in",pad=5)
    ax.yaxis.set_ticks_position('both')
    ax.xaxis.set_ticks_position('both')

    plt.savefig('figures/2021'+team+'order.png',dpi=300)
    plt.savefig('/Users/mpetersen/Projects/FantasyBaseball/webpage/fantasy-toolz.github.io/Lineups/figures/2021'+team+'order.png',dpi=300)




team = 'LAA'
"""
