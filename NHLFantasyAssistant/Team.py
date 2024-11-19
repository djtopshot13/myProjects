from Skater import Skater
from Goalie import Goalie

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
        self.new_players = self._construct_Rostered_Players()
        

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
    
    

        
    def _construct_Rostered_Players(self):
        new_players = []
        for player in self.players:
            prev_year_proj = player.stats.get('Projected 2024', {}).get('total', {})
            prev_year_total = player.stats.get('Total 2024', {}).get('total', {})
            curr_year_proj = player.stats.get('Projected 2025', {}).get('total', {})
            curr_year_total = player.stats.get('Total 2025', {}).get('total', {})
            last_7_dict = player.stats.get('Last 7 2025', {}).get('total', {})
            last_15_dict = player.stats.get('Last 15 2025', {}).get('total', {})
            last_30_dict = player.stats.get('Last 30 2025', {}).get('total', {})

            points = self.playerFantasyPointCalculator(player)
            games_played = curr_year_total.get('GP', 0)
            health_status = player.injuryStatus
            roster_availability = False

            prev_year_proj['PTS'] = points.get('Projected 2024', 0)
            prev_year_total['PTS'] = points.get('Total 2024', 0)
            curr_year_proj['PTS'] = points.get('Projected 2025', 0)
            curr_year_total['PTS'] = points.get('Total 2025', 0)
            last_7_dict['PTS'] = points.get('Last 7 2025', 0)
            last_15_dict['PTS'] = points.get('Last 15 2025', 0)
            last_30_dict['PTS'] = points.get('Last 30 2025', 0)
            
            if player.eligibleSlots[0][0] == 'G':
                goals_against = curr_year_total.get('GA', 0)
                shutouts = curr_year_total.get('SO', 0)
                wins = curr_year_total.get('W', 0)
                ot_losses = curr_year_total.get('OTL', 0)
                new_player = Goalie(player.name, self.name, player.pro_team, 'G', curr_year_total.get('PTS', 0),
                        games_played, health_status, roster_availability, prev_year_proj, prev_year_total, curr_year_proj,
                        curr_year_total, last_7_dict, last_15_dict, last_30_dict, goals_against, shutouts, wins, ot_losses)
            else:
                forward_types = {'Center': 'C', 'Left Wing': 'LW', 'Right Wing': 'RW'}
                skater_position = forward_types[player.eligibleSlots[1]] if player.eligibleSlots[0][0] == 'F' else player.eligibleSlots[0][0]
                goals = curr_year_total.get('G', 0)
                assists = curr_year_total.get('A', 0)
                pp_points = curr_year_total.get('PPP', 0)
                sh_points = curr_year_total.get('SHP', 0)
                shots_on_goal = curr_year_total.get('SOG', 0)
                hits = curr_year_total.get('HIT', 0)
                blocked_shots = curr_year_total.get('BLK', 0)
                
                new_player = Skater(player.name, self.name, player.proTeam, player.eligibleSlots[0][0], curr_year_total.get('PTS', 0), games_played,
                        health_status, roster_availability, prev_year_proj, prev_year_total, curr_year_proj,  curr_year_total, last_7_dict,
                        last_15_dict, last_30_dict, skater_position, goals, assists, pp_points, sh_points, shots_on_goal, hits, blocked_shots)
                
            new_players.append(new_player)
            print(dir(new_players))
            return new_players
                
    def displayRoster(self):
        count = 0
        for player in self.new_players:
            count = count + 1
            print(f"{count}. {player.name} ({player.position})")

            # print("Testing Player Variables")
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
        for player in self.new_players:
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
            print(player.stats)
            points = goals_against = saves = wins = shutouts = overtime_losses = goals = assists = shots = hits = blocked_shots = pp_points = sh_points = 0
            if player.eligibleSlots[0][0] == 'G':
                goals_against = player.stats.get(header, {}).get('total', {}).get('GA', 0) * -2
                saves = round(player.stats.get(header, {}).get('total', {}).get('SV', 0) / 5, 1)
                shutouts = player.stats.get(header, {})('total', {}).get('SO', 0) * 3
                wins = player.stats.get(header, {}).get('total', {}).get('W', 0) * 4
                overtime_losses = player.stats.get(header, {}).get('total', {}).get('OTL', 0)
            else: 
                goals = player.stats.get(header, {}).get('total', {}).get('G', 0) * 2
                assists = player.stats.get(header, {}).get('total', {}).get('A', 0)
                shots = round(player.stats.get(header, {}).get('total', {}).get('SOG', 0) / 10, 1)
                hits = round(player.stats.get(header, {}).get('total', {}).get('HIT', 0) / 10, 1)
                blocked_shots = round(player.stats.get(header, {}).get('total', 0).get('BLK', 0) / 2, 1)
                pp_points = round(player.stats.get(header, {}).get('total', {}).get('PPP', 0) / 2, 1)
                sh_points = round(player.stats.get(header, {}).get('total', {}).get('SHP', 0) / 2, 1)
            
            points = goals_against + saves + shutouts + wins + overtime_losses + goals + assists + shots + hits + blocked_shots + pp_points + sh_points
            points_dict[header] = points
            
        return points_dict

    def playerFantasyPoints(self, player):
        points = player.points
        return points
            
    def PositionAvgPoints(self, dCount, fCount, gCount):
        fPoints = 0
        dPoints = 0
        gPoints = 0
        for player in self.new_players:
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

    
      