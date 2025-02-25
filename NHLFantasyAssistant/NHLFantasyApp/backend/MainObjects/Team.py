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
        self.stats_keys_dict = {'W': "Goalie Wins", 'SO': "Shutouts", 'OTL': "Goalie Overtime Losses", 'SV': "Saves",
                         'L': "Goalie Losses", 'GA': "Goals Against", 'G&A': "Goals and Assists", 'G': "Goals", 'A': "Assists", 
                         'PPP': "Power Play Points", 'PPG': "Power Play Goals", 'PPA':  "Power Play Assists", 'SHP': "Short-Handed Points", 
                         'SHG': "Short-Handed Goals", 'SHA': "Short-Handed Assists", 'BLK': "Blocked Shots",'HIT': "Hits", 
                         'SOG': "Shots on Goal", 'SA': "Shot Attempts", '+/-': "+/-", 'FOW': "Faceoffs Won"}

    def __repr__(self):
        return f"Team({self.name})"

    def displayTeamRecord(self, record_map):
        return f"{self.name} [{self.matchup_wins}, {self.matchup_losses}]({record_map['streak'][self.name][self.matchup_wins + self.matchup_losses - 1]})"
    
    def draftOrder(self):
        msg = []
        msg.join(f"{self.name} Draft Order \n -------------------- \n")
        pick_num = 0
        for draft in self.draft_list:
            pick_num += 1
            msg.join(f"{pick_num}. {draft} \n")
            msg.join("--------------------")
        return msg
    
    # Called by BestTeamStatSort in MyLeague.py
    # Checks to make sure that stat is in the stat dictionary or else it raises an error
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
                         'G': "Goals", 'A': "Assists", '+/-': "+/-", 'G&A': "Goals and Assists", 'PPG': "Power Play Goals", 
                         'PPA':  "Power Play Assists", 'SHG': "Short-Handed Goals", 'SHA': "Short-Handed Assists",
                         'FOW': "Faceoffs Won", 'SOG': "Shots on Goal", 'HIT': "Hits"}
        stat_alias = stat_key_dict[stat]
        end_of_phrase = stat_alias if stat_value != 1 else stat_alias[:-1]

        
        if stat == 'GA': 
            end_of_phrase = stat_alias if stat_value != 1 else "Goal Against"
            reversedCheck = False
        elif stat == 'G&A':
            end_of_phrase = stat_alias if stat_value != 1 else "Goal or Assist"
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
                player_info = player.displayPlayerInfo()
                print(f"{count}. {player_info}")


    def displayAvgPointsSortedRoster(self):
        sorted_players = sorted(self.players, key=lambda player: player.avg_points, reverse=True)
        count = 0
        for player in sorted_players:
            count = count + 1
            player_info = player.displayPlayerAveragePoints()
            print(f"{count}. {player_info}")

    def displayPointsSortedRoster(self):
        sorted_players = sorted(self.players, key=lambda player: player.points, reverse=True)
        count = 0
        for player in sorted_players:
            count = count + 1
            player_info = player.displayPlayerInfo()
            print(f"{count}. {player_info}")

    def displayDraftRoster(self):
        # sorted_players = sorted(self.draft_list, key=lambda player: player.curr_year_proj.get('PTS', 0), reverse=True)
        count = 0
        sorted_draft_list = sorted(self.draft_list, key=lambda player: player.curr_year_proj.get('PTS', 0), reverse=True)
        for player in sorted_draft_list:
            count = count + 1
            player_info = player.displayDraftPlayerInfo()
            

            is_on_roster = any(player.name == rostered_player.name
                               for rostered_player in self.players)
            if is_on_roster:
                print(f"{count}. {player_info}")
            else:
                print(f"{count}. {player_info} --- No Longer on Roster")

    def getPositionCount(self):
        dCount = 0
        fCount = 0
        gCount = 0
        for player in self.players:
            if player.position == 'D':
                dCount = dCount + 1
            elif player.position == 'F':
                fCount = fCount + 1
            else:
                gCount = gCount + 1

        print(f"Number of Players by Position:")
        print(f"Forward: {fCount}\t Defense: {dCount}\t Goalie: {gCount}")

        self.PositionAvgPoints(dCount, fCount, gCount)
        return dCount, fCount, gCount
    
    def playerFantasyPointCalculator(self, player):
        headings = ['Projected 2024', 'Total 2024', 'Total 2025', 'Projected 2025', 'Last 7 2025', 'Last 15 2025', 'Last 30 2025']
        points_dict = {}
        for header in headings:
            if header in player.stats:
                points = goals_against = saves = wins = shutouts = overtime_losses = goals = assists = shots = hits = blocked_shots = pp_points = sh_points = 0
                if player.position == 'G':
                    goals_against = player.stats[header].get('total', {}).get('GA', 0) * -2
                    saves = round(player.stats[header].get('total', {}).get('SV', 0) / 5, 1)
                    shutouts = player.stats[header].get('total', {}).get('SO', 0) * 3
                    wins = player.stats[header].get('total', {}).get('W', 0) * 4
                    overtime_losses = player.stats[header].get('total', {}).get('OTL', 0)
                else: 
                    goals = player.stats[header].get('total', {}).get('G', 0) * 2
                    assists = player.stats[header].get('total', {}).get('A', 0)
                    shots = round(player.stats[header].get('total', {}).get('SOG', 0) / 10, 1)
                    hits = round(player.stats[header].get('total', {}).get('HIT', 0) / 10, 1)
                    blocked_shots = round(player.stats[header].get('total', 0).get('BLK', 0) / 2, 1)
                    pp_points = round(player.stats[header].get('total', {}).get('PPP', 0) / 2, 1)
                    sh_points = round(player.stats[header].get('total', {}).get('SHP', 0) / 2, 1)
                
                points = goals_against + saves + shutouts + wins + overtime_losses + goals + assists + shots + hits + blocked_shots + pp_points + sh_points
                points_dict[header] = round(points, 1)
            else:
                continue
            
        return points_dict

    # def playerFantasyPoints(self, player):
    #     points = player.points
    #     return points
            
    def PositionAvgPoints(self, dCount, fCount, gCount):
        fPoints = 0
        dPoints = 0
        gPoints = 0
        for player in self.players:
            points = self.playerFantasyPoints(player)
            if player.position == 'D':
                dPoints = dPoints + points
            elif player.position == 'F':
                fPoints = fPoints + points
            else: 
                gPoints = gPoints + points

        avgDPoints = round(dPoints / dCount, 1) if dCount != 0  else 0
        avgFPoints = round(fPoints / fCount, 1) if fCount != 0  else 0
        avgGPoints = round(gPoints / gCount, 1) if gCount != 0  else 0

        print(f"Avg Points by Position:")
        print(f"Forward: {avgFPoints}\t Defense: {avgDPoints}\t Goalie: {avgGPoints}")

        return avgDPoints, avgFPoints, avgGPoints

    
    def avgProjectedPoints(self):
        sum = 0
        player_count = len(self.draft_list)
        for player in self.draft_list:
            # if player_count == 23:
            #     if player.health_status != "ACTIVE":
            #         continue
            projected_points = player.curr_year_proj.get('PTS', 0)
            if projected_points == 0:
                player_count -= 1
            sum += projected_points
        
        avg_points = round(sum / player_count, 1)
        return avg_points
    
    def avgTotalPoints(self):
        sum = 0
        player_count = len(self.players)
        for player in self.players:
            if player_count == 23:
                if player.health_status == "INJURY_RESERVE":
                    player_count -= 1
                    continue
            proj_points = player.avg_points * 75
            if proj_points == 0:
                player_count -= 1
            sum += proj_points
        
        avg_points = round(sum / player_count, 1)
        return avg_points