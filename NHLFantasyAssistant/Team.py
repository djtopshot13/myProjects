class Team:
    def __init__(self, division_id, team_id, name, players, points_for, points_against, points_diff, matchup_wins, matchup_losses, draft_list, stats_dict):
        self.division_id = division_id
        self.team_id = team_id
        self.name = name
        self.players = players
        self.points_for = points_for
        self.points_against = points_against
        self.points_diff = points_diff
        self.matchup_wins = matchup_wins
        self.matchup_losses = matchup_losses
        self.draft_list = draft_list
        self.stats_dict = stats_dict

    def displayTeamRecord(self):
        return f"{self.name} ({self.matchup_wins}, {self.matchup_losses})"
    
    def draftOrder(self):
        msg = []
        msg.join(f"{self.name} Draft Order \n -------------------- \n")
        pick_num = 0
        for draft in self.draft_list:
            pick_num += 1
            msg.join(f"{pick_num}. {draft} \n")
            msg.join("--------------------")
        return msg
    
    def getTeamPointsFor(self):
        return self.points_for
    
    def getTeamPointsAgainst(self):
        return self.points_against
    
    def getTeamPointsDiff(self):
        return self.points_diff
    
    def getTeamWins(self):
        return self.matchup_wins
    
    def getTeamLosses(self):
        return self.matchup_losses
    
    def getTeamStat(self, stat_name):
        if stat_name in self.stats_dict:
            stat_value = int(self.stats_dict[stat_name])
            stat_alias, reversedCheck, end_of_phrase = self.getStatName(stat_name)
            return stat_value, stat_name, stat_alias, reversedCheck, end_of_phrase
        else:
            print("Error Retrieving Team Stat. Use a Different Stat\n")
            return 0, "Error", "Error", False, "Error"
            
    def getStatName(self, stat):
        reversedCheck = True
        stat_value = self.stats_dict[stat]
        stat_key_dict = {'BLK': "Blocked Shots", 'W': "Goalie Wins", 'L': "Goalie Losses", 'SA': "Shot Attempts",
                         'GA': "Goals Against", 'SV': "Saves", 'PPP': "Power Play Points", 
                         'SO': "Shutouts", 'SHP': "Short-Handed Points", 'OTL': "Goalie Overtime Losses",
                         'G': "Goals", 'A': "Assists", '+/-': "+/-", 'PPG': "Power Play Goals", 
                         'PPA':  "Power Play Assists", 'SHG': "Short-Handed Goals", 'SHA': "Short-Handed Assists",
                         'FOW': "Faceoffs Won", 'SOG': "Shots on Goal", 'HIT': "Hits"}
        stat_alias = stat_key_dict[stat]
        end_of_phrase = stat_alias if stat_value != 1 else stat_alias[:-1]

        
        if stat == 'GA': 
            end_of_phrase = stat_alias if stat_value != 1 else "Goal Against"
            reversedCheck = False
        elif stat == 'OTL':
            end_of_phrase = stat_alias if stat_value != 1 else stat_alias[:-2]
        elif stat == 'L':
            end_of_phrase = stat_alias if stat_value != 1 else stat_alias[:-2]
            reversedCheck = False
        elif stat == '+/-':
            end_of_phrase = ""
        elif stat == 'FOW':
            end_of_phrase = stat_alias if stat_value != 1 else "Faceoff Won"
        elif stat == 'SOG': 
            end_of_phrase = stat_alias if stat_value != 1 else "Shot on Goal"
        
        
            
    
        return stat_alias, reversedCheck, end_of_phrase