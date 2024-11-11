class Team:
    def __init__(self, division_id, team_id, name, players, points_for, points_against, point_diff, matchup_wins, matchup_losses):
        self.division_id = division_id
        self.team_id = team_id
        self.name = name
        self.players = players
        self.points_for = points_for
        self.points_against = points_against
        self.point_diff = point_diff
        self.matchup_wins = matchup_wins
        self.matchup_losses = matchup_losses

    def displayTeamRecord(self):
        print(f"{self.name} ({self.matchup_wins}, {self.matchup_losses})")