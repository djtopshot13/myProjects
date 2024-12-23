class Player: 
    # ['acquisitionType', 'eligibleSlots', 'injured', 'injuryStatus', 'lineupSlot', 'name', 'playerId', 'position', 'proTeam', 'stats'] variables and methods currently connected to players
    def __init__(self, name, team, pro_team, position, points, games_played,
                health_status, roster_availability, prev_year_proj, prev_year_total, curr_year_proj,
                curr_year_total, last_7_dict, last_15_dict, last_30_dict):
        self.name = name
        self.team = team
        self.pro_team = pro_team
        self.position = position
        self.points = points
        self.games_played = games_played
        self.health_status = health_status
        self.roster_availability = roster_availability
        self.prev_year_proj = prev_year_proj
        self.prev_year_total = prev_year_total
        self.curr_year_proj = curr_year_proj
        self.curr_year_total = curr_year_total
        self.last_7_dict = last_7_dict
        self.last_15_dict = last_15_dict
        self.last_30_dict = last_30_dict
        self.avg_points = round(points / games_played, 1) if games_played != 0 else 0
        
    def displayPlayerInfo(self):
        return f"{self.name} ({self.position}): [{self.points}] points"

    def displayPlayerAveragePoints(self):
        return f"{self.name} ({self.position}): [{self.avg_points}] average points"
        
    def displayDraftPlayerInfo(self):
        return f"{self.name} ({self.position}): [{self.curr_year_proj.get('PTS', 0)}] projected points"
    
    def displayUndraftedPlayerInfo(self):
        return f"{self.name} ({self.position}): [{self.curr_year_proj.get('PTS', 0)}] projected points"
    
    def __repr__(self):
        return f"Player({self.name}<{self.pro_team}>[{self.position}])"