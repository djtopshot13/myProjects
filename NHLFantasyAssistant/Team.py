class Team:
    def __init__(self, name, players, points_for, points_against, matchup_wins, matchup_losses):
        self.name = name
        self.players = players
        self.points_for = points_for
        self.points_against = points_against
        self.matchup_wins = matchup_wins
        self.matchup_losses = matchup_losses

    def displayTeamRecord(self):
        print(f"{self.name} ({self.matchup_wins}, {self.matchup_losses})")