from Player import Player

class Skater(Player):
    def __init__(self, name, team, pro_team, position, points, 
                games_played, health_status, roster_availability, 
                 prev_year_proj, prev_year_total, curr_year_proj,
                curr_year_total, last_7_dict, last_15_dict, last_30_dict,
                skater_position, goals, assists, pp_points, sh_points, shots_on_goal, hits, blocked_shots):
        
        # new_player = Skater(player.name, self.name, player.proTeam, player.eligibleSlots[0][0], curr_year_total.get('PTS', 0), games_played,
                        # health_status, roster_availability, prev_year_proj, prev_year_total, curr_year_proj,  curr_year_total, last_7_dict,
                        # last_15_dict, last_30_dict, skater_position, goals, assists, pp_points, sh_points, shots_on_goal, hits, blocked_shots)
        
        super().__init__(name, team, pro_team, position, points,
                        games_played, health_status, roster_availability, 
                        prev_year_proj, prev_year_total, curr_year_proj,
                        curr_year_total, last_7_dict, last_15_dict, last_30_dict)
        self.skater_position = skater_position
        self.goals = goals
        self.assists = assists
        self.pp_points = pp_points
        self.sh_points = sh_points
        self.shots_on_goal = shots_on_goal
        self.hits = hits
        self.blocked_shots = blocked_shots

        self.avg_points = 0 if games_played == 0 else round(points / games_played, 1)
