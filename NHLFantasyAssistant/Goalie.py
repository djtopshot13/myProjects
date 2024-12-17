from Player import Player

class Goalie(Player):
    def __init__(self, name, team, pro_team, position, points, 
                games_played, health_status, roster_availability, 
                prev_year_proj, prev_year_total, curr_year_proj,
                curr_year_total, last_7_dict, last_15_dict, last_30_dict,
                goals_against, average_goals_against, shutouts, wins, losses, ot_losses, saves, save_percentage):
        
        super().__init__(name, team, pro_team, position, points,
                        games_played, health_status, roster_availability, 
                        prev_year_proj, prev_year_total, curr_year_proj,
                        curr_year_total, last_7_dict, last_15_dict, last_30_dict)
        self.goals_against = goals_against
        self.average_goals_against = average_goals_against
        self.shutouts = shutouts
        self.wins = wins
        self.losses = losses
        self.ot_losses = ot_losses
        self.saves = saves
        self.save_percentage = round(save_percentage * 100, 1)
        

        self.avg_points = 0 if self.games_played == 0 else round(points / games_played, 1)

