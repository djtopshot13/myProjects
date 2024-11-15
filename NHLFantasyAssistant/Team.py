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
        stat_alias = ""
        end_of_phrase = ""
        stat_value = self.stats_dict[stat]
        if stat == 'BLK': 
            stat_alias = "Blocked Shots"
            end_of_phrase = stat_alias if stat_value != 1 else stat_alias[:-1]
        elif stat == 'SA': 
            stat_alias = "Shot Attempts"
            end_of_phrase = stat_alias if stat_value != 1 else stat_alias[:-1]
        elif stat == 'GA': 
            stat_alias = "Goals Against"
            end_of_phrase = stat_alias if stat_value != 1 else "Goal Against"
            reversedCheck = False
        elif stat == 'SV':
            stat_alias = "Saves"
            end_of_phrase = stat_alias if stat_value != 1 else stat_alias[:-1]
        elif stat == 'PPP':
            stat_alias = "Power Play Points"
            end_of_phrase = stat_alias if stat_value != 1 else stat_alias[:-1]
        elif stat == 'SO':
            stat_alias = "Shutouts"
            end_of_phrase = stat_alias if stat_value != 1 else stat_alias[:-1]
        elif stat == 'SHP':
            stat_alias = "Short-Handed Points"
            end_of_phrase = stat_alias if stat_value != 1 else stat_alias[:-1]
        elif stat == 'OTL':
            stat_alias = "Overtime Losses"
            end_of_phrase = stat_alias if stat_value != 1 else stat_alias[:-2]
        elif stat == 'G':
            stat_alias = "Goals"
            end_of_phrase = stat_alias if stat_value != 1 else stat_alias[:-1]
        elif stat == 'A':
            stat_alias = "Assists"
            end_of_phrase = stat_alias if stat_value != 1 else stat_alias[:-1]
        elif stat == '+/-':
            stat_alias = stat
        elif stat == 'PPG':
            stat_alias = "Power Play Goals"
            end_of_phrase = stat_alias if stat_value != 1 else stat_alias[:-1]
        elif stat == 'PPA':
            stat_alias = "Power Play Assists"
            end_of_phrase = stat_alias if stat_value != 1 else stat_alias[:-1]
        elif stat == 'SHG': 
            stat_alias = "Short-Handed Goals"
            end_of_phrase = stat_alias if stat_value != 1 else stat_alias[:-1]
        elif stat == 'SHA':
            stat_alias = "Short-Handed Assists"
            end_of_phrase = stat_alias if stat_value != 1 else stat_alias[:-1]
        elif stat == 'FOW':
            stat_alias = "Faceoffs Won"
            end_of_phrase = stat_alias if stat_value != 1 else "Faceoff Won"
        elif stat == 'SOG': 
            stat_alias = "Shots on Goal"
            end_of_phrase = stat_alias if stat_value != 1 else stat_alias[:-1]
        elif stat == 'HIT':
            stat_alias = "Hits"
            end_of_phrase = stat_alias if stat_value != 1 else stat_alias[:-1]
    
        return stat_alias, reversedCheck, end_of_phrase