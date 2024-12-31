class StreakTracker:
    def __init__(self, free_agents, teams):
        self.free_agents = free_agents
        self.teams = teams
        self.full_roster_map, self.full_code_map = self.streakRosterCodeMap()
        # print(self.full_roster_map)
        # print(self.full_code_map)
        self.free_agent_roster_map = self.full_roster_map["free_agents"].copy()
        self.free_agent_code_map = self.full_code_map["free_agents"].copy()
        self.team_roster_map = self.full_roster_map.copy()
        del self.team_roster_map['free_agents']
        self.team_code_map = self.full_code_map.copy()
        del self.team_code_map['free_agents']
        self.full_streak_ordering = self.sortStreakOrder()
        # print(self.full_streak_ordering)
        print(self.teams)

    def streakRosterCodeMap(self):
        roster_map, code_map = self.freeAgentRosterMap()
        roster_map, code_map = self.teamRosterMap(roster_map, code_map)
        return roster_map, code_map

    def freeAgentRosterMap(self):
        roster_map = {"free_agents": []}
        code_map = {"free_agents": []}
        roster = self.free_agents
        for player in roster:
            player_data = self.getPlayerData(player)
            player_data, player_code = self.generatePlayerCodeStreak(player_data)
            if player_code == "333":
                continue
            roster_map["free_agents"].append({player: player_data})
            if player_code not in code_map["free_agents"]:
                code_map["free_agents"].append(player_code)

        roster_map["free_agents"].sort(key=lambda player: list(player.keys())[0].avg_points, reverse=True)
        code_map["free_agents"].sort(key=lambda code: int(code))
        return roster_map, code_map

    def teamRosterMap(self, roster_map, code_map):
        for team in list(self.teams.values()):
            code_map[team] = []
            roster_map[team] = []
            roster = team.players
            for player in roster:
                player_data = self.getPlayerData(player)
                player_data, player_code = self.generatePlayerCodeStreak(player_data)
                if player_code == "333":
                    continue
                roster_map[team].append({player: player_data})
                if player_code not in code_map[team]:
                    code_map[team].append(player_code)
            roster_map[team].sort(key=lambda player: list(player.keys())[0].avg_points, reverse=True)
            code_map[team].sort(key=lambda code: int(code))
        return roster_map, code_map

    def sortStreakOrder(self):
        full_streak_ordering = {}
        key_vals = ["free_agents"]
        for team in list(self.teams.values()):
            key_vals.append(team)

        for key in key_vals:
            full_streak_ordering[key] = {}
            for code in self.full_code_map[key]:
                if code not in full_streak_ordering[key]:
                    full_streak_ordering[key][code] = []

                for player in self.full_roster_map[key]:
                    if player[list(player.keys())[0]]["code"] == code:
                        full_streak_ordering[key][code].append(player)
                    else: 
                        continue
        return full_streak_ordering


    def skaterStreakReport(self):
        self.streakReport(position="skater")
    def forwardStreakReport(self):
        self.streakReport(position="forward")
    def defensemanStreakReport(self):
        self.streakReport(position="defenseman")
    def goalieStreakReport(self):
        self.streakReport(position="goalie")

    def streakReport(self, position="all", streak_type="all"):
        team_keys = ["free_agents"]
        for team in list(self.teams.values()):
            team_keys.append(team)
        team_key_index = {"free_agents": 1}
        for team in list(self.teams.values()):
            for i in range(len(self.teams)):
                team_key_index[team] = i + 2
        position_keys = ["all", "skater", "forward", "defenseman", "goalie"]
        code_filter = ["all", "hot", "consistent", "cold", "warm", "cool", "heating_up", "cooling_down", "injured_or_minor_league"]
        
        if streak_type != "all" and streak_type in code_filter:
            print(f"{streak_type} Streak Report\n\n")
        print("Full Streak Report\n\n")
        for key in team_keys:
            if key != "free_agents":
                print(f"{key} Streaks:\n\n")
            else: 
                print("Free Agent Streaks:\n\n")
            code_map = self.full_code_map[key]
            if streak_type != "all" and streak_type in code_filter:
                code_map = self.filterCodeMap(code_map, streak_type)
            for code in code_map:
                code_key = self.codeDecipher(code)
                if key == "free_agents":
                    if code not in self.full_streak_ordering[key]:
                        print(f"No Free Agents with {code_key[0]} 30 Day Streak | {code_key[1]} 15 Day Streak | {code_key[2]} 7 Day Streak")
                    else:
                        players = self.full_streak_ordering["free_agents"][code]
                        if position in position_keys:
                            if position != "all" and position in position_keys:
                                players = self.playerPositionFilter(players, position)
                        self.streakFreeAgentReport(players, code_key)
                else:
                    if code not in self.full_streak_ordering[key]:
                        print(f"No players from {key} with {code_key[0]} 30 Day Streak | {code_key[1]} 15 Day Streak | {code_key[2]} 7 Day Streak")
                    else:
                        players = self.full_streak_ordering[key][code]
                        if position in position_keys:
                            if position != "all" and position in position_keys:
                                players = self.playerPositionFilter(players, position)
                        self.streakTeamReport(players, code_key, key)

    def streakFreeAgentReport(self, players, code_key):
        if players != []:
            player_size = len(players)
        else: 
            player_size = 0

        # print("Free Agent Streaks:\n\n")
        if player_size == 0:
            print(f"No Player Data for {code_key[0]} 30 Day Streak | {code_key[1]} 15 Day Streak | {code_key[2]} 7 Day Streak\n\n")
        elif player_size != 1:
            print(f"{player_size} Players with {code_key[0]} 30 Day Streak | {code_key[1]} 15 Day Streak | {code_key[2]} 7 Day Streak\n\n")
        else:
            print(f"{player_size} Player with {code_key[0]} 30 Day Streak | {code_key[1]} 15 Day Streak | {code_key[2]} 7 Day Streak\n\n")
        self.printRosterStreak(players)

    def streakTeamReport(self, players, code_key, key):
        if players != []:
            player_size = len(players)
        else: 
            player_size = 0

        if player_size == 0:
            print(f"No Player Data for {code_key[0]} 30 Day Streak | {code_key[1]} 15 Day Streak | {code_key[2]} 7 Day Streak\n\n")
        elif player_size != 1:
            print(f"{player_size} Players with {code_key[0]} 30 Day Streak | {code_key[1]} 15 Day Streak | {code_key[2]} 7 Day Streak\n\n")
        else:
            print(f"{player_size} Player with {code_key[0]} 30 Day Streak | {code_key[1]} 15 Day Streak | {code_key[2]} 7 Day Streak\n\n")
        self.printRosterStreak(players)


    def playerPositionFilter(self, players, position):
        position_players = []
        for player in players:
            player_object = list(player.keys())[0]
            if position == "skater":
                if player_object.position != "G":
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

    def filterCodeMap(self, code_map, streak_type):
        filtered_code_map = []
        code_check = True
        for code in code_map:
            if streak_type == "hot":
                filtered_code_map = ["000"]
            if streak_type == "consistent":
                filtered_code_map= ["111"]
            if streak_type == "cold":
                filtered_code_map = ["222"]
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