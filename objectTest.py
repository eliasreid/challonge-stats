class Player:
    
    def __init__(self, tag):
        self.tag = tag
        self.currElo = 1200
        self.prevElo = 1200
        self.wins = 0
        self.loses = 0

    
    def updateElo(self, change):
        self.currElo = self.currElo+change

    def refreshElo(self):
        self.prevElo=self.currElo

e = Player("elias")

#can I update equaivalently 

e.updateElo(12)

print(str(e.currElo))

print(str(e.prevElo))