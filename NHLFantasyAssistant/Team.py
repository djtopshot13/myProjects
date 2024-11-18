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
        self.__dCount = self.getPositionCount()[0]
        self.__fCount = self.getPositionCount()[1]
        self.__gcount = self.getPositionCount()[2]
        

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
    
    def displayRoster(self):
        count = 0
        for player in self.players:
            count = count + 1
            print(f"{count}. {player.name} ({player.eligibleSlots[0][0]})")

            print("Testing Player Variables")
            # print(player.acquisitionType) # returns ADD, DRAFT, or TRADE
            # print(player.eligibleSlots) # returns [[Forward, Defense, Goalie,], [actual position of Forward], ['Util'] if F or D, ['Bench'], and [IR]
            # print(player.injured) # returns True if IR or OUT, not if DTD
            # print(player.injuryStatus) # returns ACTIVE if healthy, then returns DAY_TO_DAY, INJURY_RESERVE, or OUT
            # print(player.lineupSlot) # returns value from eligibleSlots of where player is currently located
            # print(player.playerId)
            # print(player.proTeam)
            # print(player.stats) # nested dictionaries that could be split. Inner Dictionaries: 'Total 2024' (prevYear), 'Total 2025' (currYear), 
            # 'Last 7 2025' stats from previous 7 games, 'Last 15 2025' stats from previous 15 games, 'Projected 2024' (prevYearProj), 'Projected 2025' (currYearProj)

    def getPositionCount(self):
        dCount = 0
        fCount = 0
        gCount = 0
        for player in self.players:
            if player.eligibleSlots[0][0] == 'D':
                dCount = dCount + 1
            elif player.eligibleSlots[0][0] == 'F':
                fCount = fCount + 1
            else:
                gCount = gCount + 1

        print(f"Number of Players by Position:")
        print(f"Forward: {fCount}\t Defense: {dCount}\t Goalie: {gCount}")
        return dCount, fCount, gCount
    
    def PlayerFantasyPoints(self):
        points = 0
        for player in self.players:
            points = points + player.stats['Total 2025']['total']['G'] * 2
            
    def PositionAvgPoints(self):
        for player in self.players:
            points = player.stats['P']
            if player.eligibleSlots[0][0] == 'D':
                dPoints = dPoints + points
            elif player.eligibleSlots[0][0] == 'F':
                fPoints = fPoints + points
            else: 
                gPoints = gPoints + points

        avgDPoints = round(dPoints / self.__dCount, 1)
        avgFPoints = round(fPoints / self.__fCount, 1)
        avgGPoints = round(gPoints / self.__gcount, 1)

        print(f"Avg Points by Position:")
        print(f"Forward: {avgFPoints}\t Defense: {avgDPoints}, Goalie: {avgGPoints}")

        return avgDPoints, avgFPoints, avgGPoints