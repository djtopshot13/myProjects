class Player: 
    def __init__(self, name, team, position, points, games_played, health_status, roster_availability):
        self.name = name
        self.team = team
        self.position = position
        self.points = points
        self.gamesPlayed = games_played
        self.healthStatus = health_status
        self.rosterAvailability = roster_availability
        self.avg_points = round(points / games_played, 1)
    
    def displayPlayerInfo(self):
        print(f"{self.name} ({self.team}) - {self.position}: {self.points} points")
        # if (self.health_status != "healthy"):
        #     print(f"{self.name} is {self.health_status}")
        # if (self.rosterAvailability != "availaible"):
        #     print(f"{self.name} is not available to be added")