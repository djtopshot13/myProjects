import Player

class Goalie(Player):
    def __init__(self, name, team, position, points, games_played, health_status, roster_availability, avg_goals_against, shutouts, wins, otl_losses, saves, save_percentage):
        super().__init__(name, team, "G", points, games_played, health_status, roster_availability)
        self.avg_goals_against = avg_goals_against
        self.shutouts = shutouts
        self.wins = wins
        self.otl_losses = otl_losses
        self.saves = saves
        self.save_percentage = save_percentage

        