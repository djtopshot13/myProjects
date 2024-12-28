class RosterGrade:
    def __init__(self, teams, draft_dict, free_agents, undrafted_players):
        self.teams = teams
        self.draft_dict = draft_dict
        self.free_agents = free_agents
        self.undrafted_players = undrafted_players
        self.draft_VORP, self.draft_VORP_pos_count = self.createVORPTeam(undrafted_players)
        self.curr_VORP, self.curr_VORP_pos_count = self.createVORPTeam(free_agents)
        
        self.avg_proj_points_dict = self.projectionVORP(True, self.projectionTeams(True))
        self.avg_total_points_dict = self.projectionVORP(False, self.projectionTeams(False))

    def createVORPTeam(self, player_list):
        forward_players, defense_players, goalie_players = [], [], []
        full_roster = []
        MAX_F_COUNT = 15
        MIN_F_COUNT = 9
        MAX_D_COUNT = 11
        MIN_D_COUNT= 5
        MAX_G_COUNT = 4
        MIN_G_COUNT = 2
        TOTAL_PLAYER_COUNT = 22

        # go through all undrafted players and add players by position, should be in greatest to least order
        for player in player_list:
            if player.position == 'F':
                forward_players.append(player)
            if player.position == 'D':
                defense_players.append(player)
            if player.position == 'G':
                goalie_players.append(player)

        # set up roster with the top players for the min count of each position
        full_roster.extend(forward_players[i] for i in range(MIN_F_COUNT))
        full_roster.extend(defense_players[i] for i in range(MIN_D_COUNT))
        full_roster.extend(goalie_players[i] for i in range(MIN_G_COUNT))

        # set count values to min count since those players are added to the VORP team (Value of Remaining Players)
        f_count = MIN_F_COUNT
        d_count = MIN_D_COUNT
        g_count = MIN_G_COUNT

        # go through all player types for remaining 6 positions on roster
        for player in player_list:
            # finish when all position counts are equal to the total count
            if f_count + d_count + g_count == TOTAL_PLAYER_COUNT:
                break
            # if the player has already been added skip over the loop logic that iteration
            if player in full_roster:
                continue
            # this should happen when there are still available spots and the player is not already in full_roster
            else:
                # check what position the next highest scoring player is and that the position count doesn't exceed the max position count
                # If the player and count pass, then increase position count by 1 and add the player to the list
                if player in forward_players and f_count < MAX_F_COUNT:
                    f_count += 1
                    full_roster.append(player)
                if player in defense_players and d_count < MAX_D_COUNT:
                    d_count += 1
                    full_roster.append(player)
                if player in goalie_players and g_count < MAX_G_COUNT:
                    g_count += 1 
                    full_roster.append(player)

        pos_count = [f_count, d_count, g_count]
        if player_list == self.undrafted_players:
            sorted_full_roster = sorted(full_roster, key=lambda player: player.curr_year_proj.get('PTS', 0), reverse=True)
        elif player_list  == self.free_agents:
            sorted_full_roster = sorted(full_roster, key=lambda player: player.curr_year_total.get('PTS', 0), reverse=True)
        else:
            print("This is an error in Roster Grade that shouldn't be reached!\n")
        return sorted_full_roster, pos_count
    
    def displayDraftVORP(self):
        print("VORP Roster after League Draft:\n")
        print(f"Forwards: {self.draft_VORP_pos_count[0]}\t Defensemen: {self.draft_VORP_pos_count[1]}\t Goalies: {self.draft_VORP_pos_count[2]}\n")
        for index, player in enumerate(self.draft_VORP):
            print(f"{index+1}. {player.displayUndraftedPlayerInfo()}")
        print()

    def projectionTeams(self, draft_bool):
        avg_points_dict = {team: 0 for team in self.teams}
        avg_points_dict['VORP'] = 0
        for team in self.teams:
            if draft_bool:
                avg_points_dict[team] = self.teams[team].avgProjectedPoints()
            else:
                avg_points_dict[team] = self.teams[team].avgTotalPoints()
        return avg_points_dict
        

    def projectionVORP(self, draft_bool, avg_points_dict):
        vorp_roster_count = 22
        vorp_roster = self.draft_VORP if draft_bool else self.curr_VORP
        vorp_sum = 0
        for i in range(vorp_roster_count):
            player = vorp_roster[i]
            if draft_bool:
                proj_points = player.curr_year_proj.get('PTS', 0)
            else:
                proj_points = player.avg_points * 75
            if proj_points == 0:
                vorp_roster_count -= 1
            vorp_sum += proj_points
            avg_proj_points = round(vorp_sum / vorp_roster_count, 1)
            avg_points_dict['VORP'] = avg_proj_points

        return avg_points_dict

    def powerRankingReport(self, draft_bool):
        sorted_points_list, power_rankings = [], []
        if draft_bool:
            points_dict = self.avg_proj_points_dict
        else:
            points_dict = self.avg_total_points_dict
        
        sorted_points_list = list(points_dict.values())
        sorted_points_list.sort(reverse=True)
        for i in range(len(sorted_points_list)):
            for key in points_dict.keys():
                val = sorted_points_list[i]
                if points_dict[key] == val:
                    power_rankings.append({key: val})
        if draft_bool:
            print("League Draft Power Ranking Results:")
            print("============================================================")
        else:
            print("League Current Power Ranking Results:")
            print("============================================================")
        ranking_count = 0
        for ranking in power_rankings:
            ranking_count += 1
            team = list(ranking.keys())[0]
            proj_points = list(ranking.values())[0]
            if team == "VORP":
                vorp_team = team
                vorp_proj_points = proj_points
                ranking_count -= 1
                continue
            if draft_bool:
                print(f"{ranking_count}. {team} with {proj_points} average projected points")
                print("============================================================")
            else: 
                print(f"{ranking_count}. {team} with {proj_points} average points")
                print("============================================================")

        print()
        if draft_bool:
            print(f"{vorp_team} roster had {vorp_proj_points} average projected points")
        else:
            print(f"{vorp_team} roster has {vorp_proj_points} average points")