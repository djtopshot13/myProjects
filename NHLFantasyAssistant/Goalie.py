import Player

class Goalie(Player):
    def __init__(self, name, team, proTeam, position, points, games_played, health_status, roster_availability, goals, assists, pp_points, sh_points, goals_against, shutouts, wins, otl_losses, saves, save_percentage):
        super().__init__(name, team, proTeam, "G", points, games_played, health_status, roster_availability, goals, assists, pp_points, sh_points)
        self.goals_against = goals_against
        self.shutouts = shutouts
        self.wins = wins
        self.otl_losses = otl_losses
        self.saves = saves
        self.save_percentage = round(save_percentage * 100, 1)
        self.avg_goals_against = round(self.goals_against / games_played, 2)

