class Player: 
    def __init__(self, name, team, proTeam, position, points, games_played, health_status, roster_availability, goals, assists, pp_points, sh_points):
        self.name = name
        self.team = team
        self.proTeam = proTeam
        self.position = position
        self.points = points
        self.gamesPlayed = games_played
        self.healthStatus = health_status
        self.rosterAvailability = roster_availability
        self.avg_points = round(points / games_played, 1)
        self.goals = goals
        self.assists = assists
        self.pp_points = pp_points
        self.sh_points = sh_points
    
    def displayPlayerInfo(self):
        print(f"{self.name} ({self.team}) - {self.position}: {self.points} points")
        
    