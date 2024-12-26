class RosterGrade:
    def __init__(self, free_agents, undrafted_players):
        self.free_agents = free_agents
        self.undrafted_players = undrafted_players
        self.draft_VORP, self.draft_VORP_pos_count = self.createVORPTeam(undrafted_players)
        self.curr_VORP, self.curr_VORP_pos_count = self.createVORPTeam(free_agents)

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