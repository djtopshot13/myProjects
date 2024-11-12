class Team:
    def __init__(self, division_id, team_id, name, players, points_for, points_against, point_diff, matchup_wins, matchup_losses, draft_dict, stats_dict):
        self.division_id = division_id
        self.team_id = team_id
        self.name = name
        self.players = players
        self.points_for = points_for
        self.points_against = points_against
        self.point_diff = point_diff
        self.matchup_wins = matchup_wins
        self.matchup_losses = matchup_losses
        self.draft_dict = draft_dict
        self.stats_dict = stats_dict

    def displayTeamRecord(self):
        return f"{self.name} ({self.matchup_wins}, {self.matchup_losses})"
    
    def draftOrder(self):
        msg = f"{self.name} Draft Order \n -------------------- \n"
        pick_num = 0
        for draft in self.draft_dict.keys():
            pick_num += 1
            msg += f"{pick_num}. {draft} \n"
            msg += "--------------------"
        return msg
    
    