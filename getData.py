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

#creating this tournament seems to work
#tournament = challonge.tournaments.show("o1p1nelk")

# works to get participants
# print(challonge.participants.index(tournament["id"]))

# Get latest tournament challonge.tournaments.index()[-1]


# print("test 1: " + list.__str__(challonge.tournaments.index(created_after="2018-10-01")))
            
#'tournament_type'

#read dat

#real names on right (values)
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

#so this code returns a list of all of the tournaments. order - oldest to newest
# challonge.tournaments.index(created_after="2018-10-01")

# for now, just get all the data from a certain date

season = challonge.tournaments.index(created_after="2019-01-01",include_matches=1) #date range should be configurable


season = [t for t in season if t["tournament_type"]=="round robin"]

outfile = open("output.csv","w")

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


    currElo = prevElo

    #iterate over matches - calc elo scores for players
    for m in challonge.matches.index(eId):

        # if winner's id is None, there there is no match result to count, skip m
        if m["winner_id"] == None:
            continue

        winner=IDtoPlayer[m["winner_id"]]
        loser=IDtoPlayer[m["loser_id"]]

        outfile.write(winner+", "+ loser+"\n")

        # print("winner Elo: " + str(prevElo[winner]))
        # print("loser Elo: " + str(prevElo[loser]))
    
        #use previous elos to calcuclate elo change, then apply change to curretn elos of players.

        eloChange = calcEloChange(prevElo[winner], prevElo[loser],1,maxChange)


        print("elochange: "+str(eloChange))

        currElo[winner] +=eloChange
        currElo[loser] -= eloChange

    outfile.write("\n")

outfile.close()

#not quite same result, could be due to corrections made to input.
print(str(currElo))



# if len(sys.argv) == 3:


#     dataURL = "https://challonge.com/api/tournaments/" + sys.argv[1] + ".json?include_matches=1&include_participants=1&api_key=drV8xB1mess5varGdkbP43r5RmitLOWjyrYlsJTF"

#     #this is required to avoid http 403 when retrieving data from url
#     opener = urllib.request.build_opener()
#     opener.addheaders = [('User-agent', 'Mozilla/5.0')]
#     urllib.request.install_opener(opener)

#     #save json data to file
#     r=urllib.request.urlretrieve(dataURL,sys.argv[2]+".json")



#ok, now do Elo code stuff

