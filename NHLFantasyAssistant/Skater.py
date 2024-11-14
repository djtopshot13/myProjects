import Player

class Skater(Player):
    def __init__(self, name, team, position, points, games_played, health_status, roster_availability, goals, assists, pp_points, sh_points, shots_on_goal, hits, blocked_shots):
        super().__init__(name, team, "G", points, games_played, health_status, roster_availability)
        self.goals = goals
        self.assists = assists
        self.pp_points = pp_points
        self.sh_points = sh_points
        self.shots_on_goal = shots_on_goal
        self.hits = hits
        self.blocked_shots = blocked_shots
        
          