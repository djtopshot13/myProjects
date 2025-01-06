class StreakTracker:
    # set up for streaktracker object with initialization being defined
    # use free_agent list and teams dictionary to create the StreakTracker
    def __init__(self, free_agents, teams):
        self.free_agents = free_agents # take free_agents list as is
        self.teams_dict = teams
        self.teams_keys = list(self.teams_dict.keys()) # save team name keys for filtering
        self.teams = list(self.teams_dict.values()) # convert to just a list of all team objects
        # method that returns dictionary with team, then player with associated player data - full_roster_map
        # key values are team objects and free_agents string and the values are just the list of unique player codes associated with that team
        self.full_roster_map, self.full_code_map = self.fullRosterCodeMap() 

        # sub list of full_roster_map just under the free_agents key
        # sub list of full_code_map just under the free_agents key
        self.free_agent_roster_map, self.free_agent_code_map = self.freeAgentRosterCodeMap() # returns 2 lists with dict elements comprised of player objects and player data

        # sub list of full_roster_map excluding the free_agents key and associated list value
        # sub list of full_code_map excluding the free_agents key and associated list value
        self.team_roster_map, self.team_code_map = self.teamRosterCodeMap() # returns 2 dictionaries with team object keys list of type dict with player object key and player data value
        

        # This combines the full_code_map and full_roster_map
        # The outermost key is the team followed by the code with a list of player objects as keys to player data
        # This is how the proper information can be ascertained much more simply
        self.full_streak_ordering = self.sortStreakOrder() 

# utilizes sub functions to get free_agents initialized first
# then augmenting the previous dictionaries with the team player objects and player data
    def fullRosterCodeMap(self): 
        roster_map = {}
        code_map = {}
        for i in range(len(self.teams) + 1):
            if i == 0:
                team = "free_agents"
                roster = self.free_agents
            else:
                team = self.teams[i-1]
                roster = team.players
        # similar implementation, but iterate over team objects list
        # for team in self.teams:
            roster_map[team] = [] # initialize new key of team object with empty list value for roster_map
            code_map[team] = [] # initialize new key of team object with empty list value for code_map
            # roster = team.players # set roster by using the current team object's players class variable (list of Player objects)
            # iterate over player object list
            for player in roster:
                player_data = self.getPlayerData(player) # this is the value for each individual player dictionary and is determined using the helper function
                player_data, player_code = self.generatePlayerCodeStreak(player_data)
                if player_code == "333":
                    continue
                roster_map[team].append({player: player_data})
                if player_code not in code_map[team]:
                    code_map[team].append(player_code)
            roster_map[team].sort(key=lambda player: list(player.keys())[0].avg_points, reverse=True)
            code_map[team].sort(key=lambda code: int(code))
        return roster_map, code_map

# free_agent roster and code map generated and returned
    def freeAgentRosterCodeMap(self):
        # roster_map = {"free_agents": []} # initialize roster_map as dictionary with key "free_agents" and value being set to an empty list
        # code_map = {"free_agents": []} # initialize code_map as dictionary with key "free_agents" and value being set to an empty list
        # roster = self.free_agents # use the free_agents instance variable (list of Player objects) to iterate over for data
        # # iterate over all free agents
        # for player in roster:
        #     player_data = self.getPlayerData(player) # this is the value for each individual player dictionary and is determined using the helper function
        #     player_data, player_code = self.generatePlayerCodeStreak(player_data) # this function modifies the previous data to add the player's streak code and return their streak code separately as well
        #     if player_code == "333": 
        #         continue # avoid adding any players with no stats at all for the season. No games played within last 30 days is the assumption in this case
        #     roster_map["free_agents"].append({player: player_data}) # otherwise add a new dictionary to the list with the player object and the associated data
        #     if player_code not in code_map["free_agents"]: 
        #         code_map["free_agents"].append(player_code) # if the current player streak code is not contained in code_map then add it in

        # # sort by highest avg_points to show stronger consistent players over the season so far and those that might not have as high of scores due to injury
        # roster_map["free_agents"].sort(key=lambda player: list(player.keys())[0].avg_points, reverse=True) # access player object in dict_keys to get avg_points class variable
        # code_map["free_agents"].sort(key=lambda code: int(code)) 
        # sort from lowest to highest streak code to have the best player codes first as well

        # this should work by using a copy of the original full maps for both player rosters and streak codes and modifying it
        roster_map, code_map = self.full_roster_map["free_agents"].copy(), self.full_code_map["free_agents"].copy()
        return roster_map, code_map # return both lists

    def teamRosterCodeMap(self):
        # roster_map = {}
        # code_map = {}
        # # similar implementation, but iterate over team objects list
        # for team in self.teams:
        #     roster_map[team] = [] # initialize new key of team object with empty list value for roster_map
        #     code_map[team] = [] # initialize new key of team object with empty list value for code_map
        #     roster = team.players # set roster by using the current team object's players class variable (list of Player objects)
        #     # iterate over player object list
        #     for player in roster:
        #         player_data = self.getPlayerData(player) # this is the value for each individual player dictionary and is determined using the helper function
        #         player_data, player_code = self.generatePlayerCodeStreak(player_data)
        #         if player_code == "333":
        #             continue
        #         roster_map[team].append({player: player_data})
        #         if player_code not in code_map[team]:
        #             code_map[team].append(player_code)
        #     roster_map[team].sort(key=lambda player: list(player.keys())[0].avg_points, reverse=True)
        #     code_map[team].sort(key=lambda code: int(code))

        # this should work by using a copy of the original full maps for both player rosters and streak codes and modifying it
        roster_map, code_map = self.full_roster_map.copy(), self.full_code_map.copy()
        del roster_map["free_agents"]
        del code_map["free_agents"]
        return roster_map, code_map

    def sortStreakOrder(self):
        full_streak_ordering = {} # initialize full_streak_ordering as a dictionary
        key_vals = list(self.full_roster_map.keys()) # initialize same keys as found in full_roster_map and full_code_map

        for key in key_vals: 
            full_streak_ordering[key] = {} # begin by setting dictionaries for each team key
            for code in self.full_code_map[key]: # use codes found within the corresponding team code list
                if code not in full_streak_ordering[key]: # if this code isn't already in the full_streak_ordering at the key value,
                    full_streak_ordering[key][code] = [] # initialize an empty list to add dictionaries too with player object and player data

                for player in self.full_roster_map[key]: # iterate over team's roster
                    if player[list(player.keys())[0]]["code"] == code: # check if player object equals the current code
                        full_streak_ordering[key][code].append(player) # if it does, add the same element found in roster_map

        return full_streak_ordering # return the finished full_streak_ordering after all loops have been iterated over 


    # def skaterStreakReport(self):
    #     self.streakReport(position="skater")
    # def forwardStreakReport(self):
    #     self.streakReport(position="forward")
    # def defensemanStreakReport(self):
    #     self.streakReport(position="defenseman")
    # def goalieStreakReport(self):
    #     self.streakReport(position="goalie")

    # *** Idea: add team filter as well which is equivalent to grabbing keys from full_streak_ordering
    def streakReport(self, team="all", position="all", streak_type="all", min_threshold=float("-inf"), max_threshold=float("inf")):
        team_keys = []
        # team_key_index = {"free_agents": 1}
        # for index, team in enumerate(self.teams):
        #     team_key_index[team] = index + 2
        if team != "all":
            if team == "free_agents":
                team_keys.append(team) 
            elif team in self.teams_keys:
                team_keys.append(self.teams_dict[team])
            elif type(team) == list:
                for element in team:
                    if element == "free_agents":
                        team_keys.append(element)
                    elif element in self.teams_keys:
                        team_keys.append(self.teams_dict[element])
                    else:
                        print("Invalid team element entered in function call\n\n")
                        return
            else:
                print("Invalid team entered in function call\n\n")
                return 
        else:
            team_keys = list(self.full_streak_ordering.keys())

        position_keys = ["all", "skater", "forward", "defenseman", "goalie"]
        code_filter = ["all", "hot", "consistent", "cold", "warm", "cool", "heating_up", "cooling_down", "injured_or_minor_league"]
        
        if streak_type != "all":
            if streak_type in code_filter:
                print(f"{streak_type} Streak Report\n\n")
            elif type(streak_type) == list:
                for streak in streak_type:
                    if streak in code_filter:
                        print(f"{streak} Streak Report\n\n")
                    else:
                        print("Invalid streak type element entered in function call\n\n")
                        return
            else: 
                print("Invalid streak type entered in function call\n\n")
                return
        else:
            print("Full Streak Report\n\n")
        for key in team_keys:
            if key != "free_agents":
                print(f"{key} Streaks:\n\n")
            else: 
                print("Free Agent Streaks:\n\n")
            code_map = set()
            if streak_type != "all":
                if streak_type in code_filter:
                    code_map.update(self.filterCodeMap(key, streak_type))
                    code_map = sorted(code_map, key=lambda code: int(code))
                elif type(streak_type) == list:
                    for streak in streak_type:
                        if streak in code_filter:
                            code_map.update(self.filterCodeMap(key, streak))
                        else:
                            print("Invalid streak type element entered in function call\n\n")
                            return
                    code_map = sorted(code_map, key=lambda code: int(code))
                else: 
                    print("Invalid streak type entered in function call\n\n")
                    return
            else: 
                code_map = self.full_code_map[key]
            if code_map == []:
                print("Empty Code Map: No players in desired streak type generated")
            else:
                for code in code_map:
                    code_key = self.codeDecipher(code)
            
                    if code not in self.full_streak_ordering[key]:
                        if key != "free_agents":
                            print(f"No players from {key} with {code_key[0]} 30 Day Streak | {code_key[1]} 15 Day Streak | {code_key[2]} 7 Day Streak")
                        else:
                            print(f"No Free Agents with {code_key[0]} 30 Day Streak | {code_key[1]} 15 Day Streak | {code_key[2]} 7 Day Streak")
                    else:
                        players = self.full_streak_ordering[key][code]
                        if position != "all":
                            if position in position_keys:
                                players = self.playerPositionFilter(players, position)
                                self.streakRosterReport(players, code_key)
                            elif type(position) == list:
                                for element in position:
                                    players = self.playerPositionFilter(players, element)
                                    self.streakRosterReport(players, code_key, min_threshold, max_threshold)
                            else:
                                print("Invalid position entered in function call")
                        else:      
                            self.streakRosterReport(players, code_key, min_threshold, max_threshold)
                
                    # if code not in self.full_streak_ordering[key]:
                    #     print(f"No players from {key} with {code_key[0]} 30 Day Streak | {code_key[1]} 15 Day Streak | {code_key[2]} 7 Day Streak")
                    # else:
                    #     players = self.full_streak_ordering[key][code]
                    #     if position in position_keys:
                    #         if position != "all" and position in position_keys:
                    #             players = self.playerPositionFilter(players, position)
                    #     self.streakTeamReport(players, code_key, key)

    # def streakFreeAgentReport(self, players, code_key):
    #     if players != []:
    #         player_size = len(players)
    #     else: 
    #         player_size = 0

    #     # print("Free Agent Streaks:\n\n")
    #     if player_size == 0:
    #         print(f"No Player Data for {code_key[0]} 30 Day Streak | {code_key[1]} 15 Day Streak | {code_key[2]} 7 Day Streak\n\n")
    #     elif player_size != 1:
    #         print(f"{player_size} Players with {code_key[0]} 30 Day Streak | {code_key[1]} 15 Day Streak | {code_key[2]} 7 Day Streak\n\n")
    #     else:
    #         print(f"{player_size} Player with {code_key[0]} 30 Day Streak | {code_key[1]} 15 Day Streak | {code_key[2]} 7 Day Streak\n\n")
    #     self.printRosterStreak(players)

    def streakRosterReport(self, players, code_key, min_threshold=float("-inf"), max_threshold=float("inf")):
        filtered_players = []
        if players != []:
            for player in players:
                player_obj = list(player.keys())[0]
                if player_obj.avg_points >= min_threshold and player_obj.avg_points <= max_threshold:
                    filtered_players.append(player)
            
            player_size = len(filtered_players)
        else: 
            player_size = 0

        if player_size == 0:
            print(f"No Player Data for {code_key[0]} 30 Day Streak | {code_key[1]} 15 Day Streak | {code_key[2]} 7 Day Streak\n\n")
        elif player_size != 1:
            print(f"{player_size} Players with {code_key[0]} 30 Day Streak | {code_key[1]} 15 Day Streak | {code_key[2]} 7 Day Streak\n\n")
        else:
            print(f"{player_size} Player with {code_key[0]} 30 Day Streak | {code_key[1]} 15 Day Streak | {code_key[2]} 7 Day Streak\n\n")
        self.printRosterStreak(filtered_players)


    def playerPositionFilter(self, players, position):
        position_players = []
        for player in players:
            player_object = list(player.keys())[0]
            if position == "skater":
                if type(player_object.position) != "G":
                    position_players.append(player)
            elif position == "forward":
                if player_object.position == "F":
                    position_players.append(player)
            elif position == "defenseman":
                if player_object.position == "D":
                    position_players.append(player)
            elif position == "goalie":
                if player_object.position == "G":
                    position_players.append(player)
            else:
                print("Error something went wrong here somehow in filtering by player position!")

            return position_players

    def filterCodeMap(self, key, streak_type):
        filtered_code_map = []
        code_map = self.full_code_map[key]
        hot_key = "000"
        cons_key = "111"
        cold_key = "222"
        if streak_type == "hot" and hot_key in code_map:
                filtered_code_map = [hot_key]
        if streak_type == "consistent" and cons_key in code_map:
            filtered_code_map = [cons_key]
        if streak_type == "cold" and cold_key in code_map:
            filtered_code_map = ["222"]

        for code in code_map:
            code_check = True
            if streak_type == "warm":
                for char in code:
                    if char != "0" and char != "1":
                        code_check = False
                if code_check:
                    filtered_code_map.append(code)
            if streak_type == "cool":
                for char in code:
                    if char != "1" and char != "2":
                        code_check = False
                if code_check:
                    filtered_code_map.append(code)
            if streak_type == "heating_up":
                if int(code[0]) < int(code[1]) and int(code[1]) < int(code[2]):
                    filtered_code_map.append(code)
            if streak_type == "cooling_down":
                if int(code[0]) > int(code[1]) and int(code[1]) > int(code[2]):
                    filtered_code_map.append(code)
            if streak_type == "injured_or_minor_league":
                if "3" in code:
                    filtered_code_map.append(code)

        return filtered_code_map

    def printRosterStreak(self, player_list):
        forward_count, defensemen_count, goalie_count = 0, 0, 0
        forward_list, defensemen_list, goalie_list = [], [], []
        for player in player_list:
            
            # if player_obj.avg_points >= threshold:
                player_obj = list(player.keys())[0]
                if player_obj.position == "F":
                    forward_count += 1
                    forward_list.append(player)
                if player_obj.position == "D":
                    defensemen_count += 1
                    defensemen_list.append(player)
                if player_obj.position == "G":
                    goalie_count += 1
                    goalie_list.append(player)
        if forward_count == 0:
           print("No Forward Data\n\n")
        elif forward_count != 1:
            print(f"{forward_count} Forwards:\n\n")
        else:
            print(f"{forward_count} Forward:\n\n")
        self.printPlayerStreaks(forward_list)
        
        if defensemen_count == 0:
           print("No Defensemen Data\n\n")
        elif defensemen_count != 1:
            print(f"{defensemen_count} Defensemen:\n\n")
        else:
            print(f"{defensemen_count} Defenseman:\n\n")
        self.printPlayerStreaks(defensemen_list)

        if goalie_count == 0:
           print("No Goalie Data\n\n")
        elif goalie_count != 1:
            print(f"{goalie_count} Goalies:\n\n")
        else:
            print(f"{goalie_count} Goalie:\n\n")
        self.printPlayerStreaks(goalie_list)

    def printPlayerStreaks(self, player_list):
        for index, player in enumerate(player_list):
            player_obj = list(player.keys())[0]
            player_dict = player_list[index][player_obj]
            avg_points = player_dict["avg_points"]
            streak_30 = player_dict["last_30_days"]["streak"]
            streak_15 = player_dict["last_15_days"]["streak"]
            streak_7 = player_dict["last_7_days"]["streak"]
            point_diff_30 = player_dict["last_30_days"]["avg_difference"]
            point_diff_15 = player_dict["last_15_days"]["avg_difference"]
            point_diff_7 = player_dict["last_7_days"]["avg_difference"]
            point_sign_30 = "+" if point_diff_30 > 0 else ""
            point_sign_15 = "+" if point_diff_15 > 0 else ""
            point_sign_7 = "+" if point_diff_7 > 0 else ""   
            print(f"{index + 1}. {player_obj}:\n\n")
            if streak_30 == "Consistent":
                print(f"Last 30 Days: {streak_30} Streak maintaining {avg_points} avg points\n")
            elif streak_30 == "Empty":
                print(f"Last 30 Days: Not enough data to generate any analysis\n")
            else:
                print(f"Last 30 Days: {streak_30} Streak with change of {point_sign_30}{point_diff_30} from {avg_points} avg points\n")

            if streak_15 == "Consistent":
                print(f"Last 15 Days: {streak_15} Streak maintaining {avg_points} avg points\n")
            elif streak_15 == "Empty":
                print(f"Last 15 Days: Not enough data to generate any analysis\n")
            else:
                print(f"Last 15 Days: {streak_15} Streak with change of {point_sign_15}{point_diff_15} from {avg_points} avg points\n")

            if streak_7 == "Consistent":
                print(f"Last 7 Days: {streak_7} Streak maintaining {avg_points} avg points\n\n")
            elif streak_7 == "Empty":
                print(f"Last 7 Days: Not enough data to generate any analysis\n\n")
            else:
                print(f"Last 7 Days: {streak_7} Streak with change of {point_sign_7}{point_diff_7} from {avg_points} avg points\n\n")

    def getPlayerData(self, player):
        avg_points_total = player.avg_points
        points_7 = player.last_7_dict.get('PTS', 0)
        games_played_7 = player.last_7_dict.get('GP', 0)
        avg_points_7 = round(points_7 / games_played_7, 1) if games_played_7 != 0 else 0 
        avg_difference_7 = round(avg_points_7 - avg_points_total, 1)
        points_15 = player.last_15_dict.get('PTS', 0)
        games_played_15 = player.last_15_dict.get('GP', 0)
        avg_points_15 = round(points_15 / games_played_15, 1) if games_played_15 != 0  else 0
        avg_difference_15 = round(avg_points_15 - avg_points_total, 1)
        points_30 = player.last_30_dict.get('PTS', 0)
        games_played_30 = player.last_30_dict.get('GP', 0)
        avg_points_30 = round(points_30 / games_played_30, 1) if games_played_30 != 0  else 0
        avg_difference_30 = round(avg_points_30 - avg_points_total, 1)

        player_data = {
            "last_30_days": {
                "points": points_30,
                "games_played": games_played_30,
                "avg_points": avg_points_30, 
                "avg_difference": avg_difference_30
            }, 
            "last_15_days": {
                "points": points_15,
                "games_played": games_played_15,
                "avg_points": avg_points_15,
                "avg_difference": avg_difference_15
            },
            "last_7_days": {
                "points": points_7,
                "games_played": games_played_7,
                "avg_points": avg_points_7,
                "avg_difference": avg_difference_7
            },
            "avg_points": avg_points_total
        }
        return player_data


    def generatePlayerCodeStreak(self, player_data):
        time_blocks = ["last_30_days", "last_15_days", "last_7_days"]
        code_calc = {"Hot": "0", "Consistent": "1", "Cold": "2", "Empty": "3"}
        player_code = ""
        for idx, time in enumerate(time_blocks): 
            avg_difference = player_data[time]["avg_difference"]
            games_played = player_data[time]["games_played"]
            if games_played > 0:
                if avg_difference > 0:
                    player_data[time]["streak"] = "Hot"
                elif avg_difference == 0:
                    player_data[time]["streak"] = "Consistent"
                else:
                    player_data[time]["streak"] = "Cold"
            else:
                player_data[time]["streak"] = "Empty"

            player_code += code_calc[player_data[time]["streak"]]

        player_data["code"] = player_code 
    
        return player_data, player_code
    
    def codeDecipher(self, code):
        code_key = []
        for idx in range(3):
            digit = code[idx]
            if digit == "0":
                code_key.append("Hot")
            elif digit == "1":
                code_key.append("Consistent")
            elif digit == "2":
                code_key.append("Cold")
            else:
                code_key.append("Empty")
        return code_key