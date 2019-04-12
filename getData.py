import sys
import json
import challonge

#calculates Elo for player A from match result
# res is playerA's actual score, so 1 for win, 0 for loss
def calcEloChange(prevEloA, prevEloB, res, k):

    expectedA = 1 / ( 1 + 10 ** ((prevEloB-prevEloA) / 400 ) )

    return k*(res - expectedA)

#need to figure out more elegant way to handle credentials - can't open-source code right now due to this. 

with open("credentials.config") as f:
    user = f.readline().strip()
    key = f.readline().strip()
    challonge.set_credentials(user, key)

#keys: typos / alternate names
#values: proper names
aliases ={
    "Smithsyn": "SmithSyn",
    "Shleeepy": "Shleepy" ,
    "SSGansta": "SS-Gangsta",
    "elray": "Elray",
    "El-Ray": "Elray",
    "El-ray": "Elray",
    "el-ray": "Elray",
    "PromiseFace": "Dru-Gatti",
    "Drugatti": "Dru-Gatti",
    "Dru-gatti": "Dru-Gatti"
}


# gets all of the tournaments from specified date range 
season = challonge.tournaments.index(created_after="2019-01-01",include_matches=1) #date range should be configurable


season = [t for t in season if t["tournament_type"]=="round robin"]

outfile = open("output.csv","w")

#SHOULD REFACTOR A BIT - MAKE OBJECT TO REPRESENT PLAYER
# OBJECT CAN HAVE STATS LIKE WINS / LOSSES, ETC

#First investigate why my stats arent the same as prev code i was using.. 

#scores to contain names of players and their "current" elo scores (scores going into an event)
# dictinary of name: score(float)
prevElo = {}
currElo = {}

eloDefault=1200
maxChange=32

# need to iterate over tounrneys in seasons, then over 

for event in season: #this should work because season is a list (iterable object)

    eId = event["id"]

    #get all participants - this has their ID and username
    pData = challonge.participants.index(eId)

    #map IDs of players (which is what the match contains) to their names
    IDtoPlayer={}

    #iterate over players in the event(THIS IS PROBABLY A BAD COMMENT)
    for p in pData:

        name = p["name"]

        #fix names to correct input errors / name changes
        if name in aliases:
            name = aliases[name]

        IDtoPlayer[p["id"]] = name

        # add player to score list if missing
        if name not in prevElo:
            prevElo[name] = eloDefault
            currElo[name] = eloDefault


    #at this point in code, on first event, there is is a prev elo for all the players (1200), but no curr elo

    #for incoming players, make curr Elo as well

    #previous should become current
    #curr elo is nothing, so dont wanna do this...
    prevElo = currElo.copy()
    #I think there's a problem with this adn the above elodefault piece



    #iterate over matches - calc elo scores for players
    for m in challonge.matches.index(eId):

        # if winner's id is None, there there is no match result to count, skip m
        if m["winner_id"] == None:
            continue

        winner=IDtoPlayer[m["winner_id"]]
        loser=IDtoPlayer[m["loser_id"]]

        

        # print("winner Elo: " + str(prevElo[winner]))
        # print("loser Elo: " + str(prevElo[loser]))
    
        #use previous elos to calcuclate elo change, then apply change to curretn elos of players.

        eloChange = calcEloChange(prevElo[winner], prevElo[loser],1,maxChange)


        # print("elochange: "+str(eloChange))

        currElo[winner] +=eloChange
        currElo[loser] -= eloChange

        outfile.write(winner + ", "+str(prevElo[winner]) + ", "+ loser + ", "+str(prevElo[loser]) + "\n")

    outfile.write("\n")

outfile.close()

#not quite same result, could be due to corrections made to input.
print(str(currElo))


