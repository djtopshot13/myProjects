class Player: 
    # ['acquisitionType', 'eligibleSlots', 'injured', 'injuryStatus', 'lineupSlot', 'name', 'playerId', 'position', 'proTeam', 'stats'] variables and methods currently connected to players
    def __init__(self, name, team, proTeam, position, points, games_played,
                health_status, roster_availability, prevYearProjDict, prevYearTotalDict, currYearProjDict,
                currYearTotalDict, last7Dict, last15Dict):
        self.name = name
        self.team = team
        self.proTeam = proTeam
        self.position = position
        self.points = points
        self.gamesPlayed = games_played
        self.healthStatus = health_status
        self.rosterAvailability = roster_availability
        self.avg_points = round(points / games_played, 1)
        self.prevYearProjDict = prevYearProjDict
        self.prevYearTotalDict = prevYearTotalDict
        self.currYearProjDict = currYearProjDict
        self.currYearTotalDict = currYearTotalDict
        self.last7Dict = last7Dict
        self.last15Dict = last15Dict
    
    def displayPlayerInfo(self):
        print(f"{self.name} ({self.team}) - {self.position}: {self.points} points")
        
    