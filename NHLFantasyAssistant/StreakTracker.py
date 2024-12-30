class StreakTracker:
    def __init__(self, free_agents, teams):
        self.free_agents = free_agents
        self.teams = teams
        self.full_roster_map, self.full_code_map = self.streakRosterCodeMap()
        self.free_agent_roster_map = self.full_roster_map["free_agents"]
        self.free_agent_code_map = self.full_code_map["free_agents"]
        self.team_roster_map = self.full_code_map
        del self.team_roster_map["free_agents"]
        self.team_code_map = self.full_code_map
        del self.team_code_map["free_agents"]
        self.full_streak_ordering = self.sortStreakOrder()

    def skaterStreakReport(self):
        self.streakReport("skater")
    def forwardStreakReport(self):
        self.streakReport("forward")
    def defensemanStreakReport(self):
        self.streakReport("defenseman")
    def goalieStreakReport(self):
        self.streakReport("goalie")

    def streakReport(self, position):
        team_keys = ["free_agents"]
        team_keys.append(team for team in self.teams)
        team_key_index = {"free_agents": 1}
        for team in self.teams:
            for i in range(len(self.teams)):
                team_key_index[team: i+2]
        position_keys = ["all", "skater", "forward", "defenseman", "goalie"]
        
        # self.streakPrintFormat(team_keys)
        print("Full Streak Report\n\n")
        for key in team_keys:
            count = 0
            for code in self.full_code_map[key]:
                code_key = self.codeDecipher(code)
                count += 1
                if key == "free_agents":
                    if count != team_key_index[key]:
                        print(f"No Free Agents with {code_key[0]} 30 Day Streak | {code_key[1]} 15 Day Streak | {code_key[2]} 7 Day Streak")
                    else:
                        players = self.full_roster_map["free_agents"][code]
                        if position in position_keys:
                            if position != "all":
                                players = self.playerPositionFilter(players, position)
                        self.streakFreeAgentReport(players, code_key)
                else:
                    if count != team_key_index[key]:
                        print(f"No players from {key} with {code_key[0]} 30 Day Streak | {code_key[1]} 15 Day Streak | {code_key[2]} 7 Day Streak")
                    else:
                        players = self.full_roster_map[key][code]
                        if position in position_keys:
                            if position != "all":
                                players = self.playerPositionFilter(players, position)
                        self.streakTeamReport(players, code_key)

    def streakFreeAgentReport(self, players, code_key):
        player_size = len(players)

        print("Free Agent Streaks:\n")
        if player_size != 1:
            print(f"{player_size} Players with {code_key[0]} 30 Day Streak | {code_key[1]} 15 Day Streak | {code_key[2]} 7 Day Streak\n\n")
        else:
            print(f"{player_size} Player with {code_key[0]} 30 Day Streak | {code_key[1]} 15 Day Streak | {code_key[2]} 7 Day Streak\n\n")

    def playerPositionFilter(self, players, position):
        position_players = []
        for player in players:
            player_object = list(player.keys())[0]
            if position == "skater":
                if player_object.position != "G":
                    position_players.append(player)
                else:
                    continue
            elif position == "forward":
                if player_object.position == "F":
                    position_players.append(player)
                else: 
                    continue
            elif position == "defenseman":
                if player_object.position == "D":
                    position_players.append(player)
            elif position == "goalie":
                if player_object.position == "G":
                    position_players.append(player)
            else:
                print("Error something went wrong here somehow in filtering by player position!")

            return position_players


    def singleStreakAnalysis(self, code_map, full_streak_ordering, code):
        if code not in code_map:
            print(f"Invalid Code \"{code}\": Please try another code\n")
        else:
            streak_list = full_streak_ordering[code]
            code_key = self.codeDecipher(code)
            streak_list_size = len(streak_list)
            if streak_list_size != 1:
                print(f"{streak_list_size} Players with {code_key[0]} 30 Day Streak | {code_key[1]} 15 Day Streak | {code_key[2]} 7 Day Streak\n\n")
            else:
                print(f"{streak_list_size} Player with {code_key[0]} 30 Day Streak | {code_key[1]} 15 Day Streak | {code_key[2]} 7 Day Streak\n\n")
            self.printStreakPlayers(streak_list)

    def fullDepthStreakAnalysis(self, code_map, full_streak_ordering):
        for code in code_map: 
            self.singleStreakAnalysis(code_map, full_streak_ordering, code)

    def printStreakPlayers(self, full_streak_list):
        player_list, forward_list, defense_list, goalie_list = [], [], [], []
        for player in full_streak_list:
            player_object = list(player.keys())[0]
            if player_object.position == "F":
                forward_list.append(player)
            elif player_object.position == "D":
                defense_list.append(player)
            else:
                goalie_list.append(player)
            player_list.append(player)

        forward_list.sort(key=lambda player: list(player.keys())[0].avg_points, reverse=True)
        defense_list.sort(key=lambda player: list(player.keys())[0].avg_points, reverse=True)
        goalie_list.sort(key=lambda player: list(player.keys())[0].avg_points, reverse=True)
        player_list.sort(key=lambda player: list(player.keys())[0].avg_points, reverse=True)
        
        player_size = len(player_list)
        forward_size = len(forward_list)
        defense_size = len(defense_list)
        goalie_size = len(goalie_list)

        if player_size == 1:
            print(f"Player:\n\n")
            self.streakPrintFormat(player_list)
        else:
            print(f"All Players:\n\n")
        # print(f"{player_list}\n")
            self.streakPrintFormat(player_list)

            if forward_size != 1:
                print(f"{forward_size} Forwards:\n\n")
            else:
                print(f"{forward_size} Forward:\n\n")
            # print(f"{skater_list}\n")   
            self.streakPrintFormat(forward_list)
            if defense_size != 1:
                print(f"{len(defense_list)} Defensemen:\n\n")
            else:
                print(f"{len(defense_list)} Defenseman:\n\n")
            # print(f"{skater_list}\n")   
            self.streakPrintFormat(defense_list)
            if goalie_size != 1:
                print(f"{len(goalie_list)} Goalies:\n\n")
            else:
                print(f"{len(goalie_list)} Goalie:\n\n")
            # print(f"{goalie_list}\n\n")
            self.streakPrintFormat(goalie_list)
        
    def streakPrintFormat(self, player_list):
        goalie_list, forward_list, defense_list  = [], [], []
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
            if player_obj.position == "G":
                goalie_list.append(player)
            elif player_obj.position == "F":
                forward_list.append(player)
            else:
                defense_list.append(player)
            
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

        roster_map.sort(key=lambda player: list(player[0]).avg_points, reverse=True)
        code_map["free_agents"].sort(key=lambda code: int(code))
        return roster_map, code_map

    def teamRosterMap(self, roster_map, code_map):
        for team in self.teams:
            code_map[team: []]
            roster_map[team: []]
            roster = self.teams[team]
            for player in roster:
                player_data = self.getPlayerData(player)
                player_data, player_code = self.generatePlayerCodeStreak(player_data)
                if player_code == "333":
                    continue
                roster_map[team].append({player: player_data})
                if player_code not in code_map[team]:
                    code_map[team].append(player_code)
            roster_map.sort(key=lambda player: list(player[0]).avg_points, reverse=True)
            code_map[team].sort(key=lambda code: int(code))

        return roster_map, code_map


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
        key_values = ["avg_difference_30", "games_played_30", "avg_difference_15", "games_played_15", "avg_difference_7", "games_played_7"]
        code_calc = {"Hot": "0", "Consistent": "1", "Cold": "2", "Empty": "3"}
        player_code = ""
        for idx, time in enumerate(time_blocks):
            avg_diff_idx = idx * 2
            games_played_idx = avg_diff_idx + 1
            avg_diff_key = key_values[avg_diff_idx]
            games_played_key = key_values[games_played_idx]
            
            avg_difference = player_data[time][avg_diff_key]
            games_played = player_data[time][games_played_key]
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
    
    def sortStreakOrder(self):
        full_streak_ordering = {}
        key_vals = ["free_agents"]
        for team in self.teams:
            key_vals.append(team)

        for key in key_vals:
            for code in self.full_code_map[key]:
                full_streak_ordering[key][code] = []
                for player in self.full_roster_map[key]:
                    if player[1]["code"] == code:
                        full_streak_ordering[key][code].append(player)
                    else: 
                        continue
        return full_streak_ordering
    
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