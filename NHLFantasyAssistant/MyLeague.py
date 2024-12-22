import League
import Player
import Skater
import Goalie
import Matchup

class MyLeague:
    def __init__(self, teams, matchups, draft_dict, rostered_players, free_agents, recent_activity, player_map, standings, curr_matchup_period, settings):
        # self.free_agents = teams['Free Agents'].players
        # del teams['Free Agents']
        self.teams = teams
        self.matchups = matchups
        self.draft_dict = draft_dict
        self._rostered_players = rostered_players
        self.free_agents = free_agents
        self.recent_activity = recent_activity
        self.player_map = player_map
        self.standings = standings
        self.curr_matchup_period = curr_matchup_period
        self.settings = settings
        self._all_players = self._get_All_Players()
        self.undrafted_list = self._get_Undrafted_Players()
        self.matchup = self._make_Matchup()
        self.team_record_map = self.matchup.team_record_map
  

    def _make_Matchup(self):
        return Matchup.Matchup(self.curr_matchup_period, self.matchups, self.teams)
    
    # Check to make sure that only player objects are added
    def _get_All_Players(self):
        all_players = []
        all_players = self.free_agents.copy()
        for players in self._rostered_players.values(): # double check that this only returns player objects and no other object typ
            for player in players: # nested list by team value possibly to iterate over
                all_players.append(player)
        return all_players # Should return a list that includes players from the free_agents list anad from rostered_players

    def _get_Undrafted_Players(self):
        all_players = self._all_players
        # Use all_players to iterate over and check both rostered and unrostered players for those that were drafted
        # _free_agents = self.free_agents
        # _roster_players = self._rostered_players # Should return dictionary of drafted_players with team as key

        # best_projected = sorted(self.free_agents, key=lambda player: player.curr_year_proj.get('PTS', 0), reverse=True)
        # for player in best_projected:
        #     print(player.displayUndraftedPlayerInfo())
        
        draft_size = 22
        full_draft_list = []
        for team in self.teams:
            for i in range(draft_size):
                drafted_player = self.draft_dict[team][i]
                # print(drafted_player.rosterAvailability)
                full_draft_list.append(drafted_player)
        
        drafted_players = list(set(all_players) & set(full_draft_list))
        undrafted_players = list(set(all_players) - set(drafted_players))
        # undrafted_players = list(set(undrafted_players) - set(full_draft_list))
        best_projected_undrafted = sorted(undrafted_players, key=lambda player: player.curr_year_proj.get('PTS', 0), reverse=True)
        # for player in best_projected_undrafted:
        #     print(player.displayUndraftedPlayerInfo())

        # for player in all_players: # This doesn't work fully yet
        #     # print(type(player))
        #     for draftee in full_draft_list:
        #         if player.team == "":
        #                 is_drafted = False
        #         else:
        #             continue

        #     if not is_drafted:
        #             print(f"This player is undrafted: {player.name}")
        #             undrafted_players.append(player)
        #             continue
        #     else:
        #         print(f"Check failed for player: {player.name}")
                
                
                    

        # It should add a player that is within all_players, but not within drafted_players
        sorted_undrafted_players = sorted(undrafted_players, key=lambda player: player.curr_year_proj.get('PTS', 0), reverse=True) # Sort by projected values to get best expected players for draft grade
        # print(sorted_undrafted_players)
        # proj_dict_count = 0
        # for player in sorted_undrafted_players:
        #     if player.curr_year_proj.get('PTS', 0) != 0:
        #         proj_dict_count += 1
        #     player.displayUndraftedPlayerInfo()
        # print(self.draft_dict)
        # print(proj_dict_count)
        return sorted_undrafted_players # return list of sorted_undrafted_players
    
    def LeagueDraftGrade(self):
        # Calculate VORP (Value of Remaining/Undrafted Players) with the most projected points
        # Compare the difference between each fantasy team's projected point total and the VORP projected points
        # Grade each team accordingly, the larger positive difference, the better the grade

        # initialize starter lists with undrafted_players and empty lists by player position
        undrafted_players = self.undrafted_list
        forward_players = []
        defense_players = []
        goalie_players = []
        # set up min and max count by position along with total roster count at draft day
        max_d_count = 11
        min_d_count = 5
        max_g_count = 4
        min_g_count = 2
        max_f_count = 15
        min_f_count = 9
        total_count = 22

        # go through all undrafted players and add players by position, should be in greatest to least order
        for player in undrafted_players:
            if player.position == 'F':
                forward_players.append(player)
            elif player.position == 'D':
                defense_players.append(player)
            elif player.position == 'G':
                goalie_players.append(player)

        # set up roster with the top players for the min count of each position
        min_position_roster = []
        min_position_roster.extend(forward_players[i] for i in range(min_f_count))
        min_position_roster.extend(defense_players[i] for i in range(min_d_count))
        min_position_roster.extend(goalie_players[i] for i in range(min_g_count))

        # set count values to min count since those players are added to the VORP team (Value of Remaining Players)
        f_count = min_f_count
        d_count = min_d_count
        g_count = min_g_count

        # set up full roster list by copying all the min roster values 
        full_roster = min_position_roster.copy()
        
        # go through all player types for remaining 6 positions on roster
        for player in undrafted_players:
            # finish when all position counts are equal to the total count
            if f_count + d_count + g_count == total_count:
                break
            # if the player has already been added skip over the loop logic that iteration
            if player in full_roster:
                continue
            # this should happen when there are still available spots and the player is not already in full_roster
            else:
                # check what position the next highest scoring player is and that the position count doesn't exceed the max position count
                # If the player and count pass, then increase position count by 1 and add the player to the list
                if player in forward_players and f_count < max_f_count:
                    f_count += 1
                    full_roster.append(player)
                elif player in defense_players and d_count < max_d_count:
                    d_count += 1
                    full_roster.append(player)
                elif player in goalie_players and g_count < max_g_count:
                    g_count += 1 
                    full_roster.append(player)
                
        # print statement that shows how many players of each position were added
        # should be one unique VORP team to get max score unless players of same position have duplicate projected points   
        print("VORP Roster after League Draft:\n")
        print(f"Forwards: {f_count}\t Defensemen: {d_count}\t Goalies: {g_count}")
        # set print statement up to print the position in the player roster with projected points for the current year, name, and position
        # I might be able to sort it too if I wanted 
        sorted_full_roster = sorted(full_roster, key=lambda player: player.curr_year_proj.get('PTS', 0), reverse=True)
        for index, player in enumerate(sorted_full_roster, 1):
            # print(player.curr_year_proj)
            print(f"{index}. {player.displayUndraftedPlayerInfo()}")
        print()

        
        
        avg_projected_points_dict = {team: 0 for team in self.teams}
        avg_projected_points_dict['VORP'] = 0
        for team in self.teams:
            roster_count = 22
            team_sum = 0
            for i in range(roster_count):
                player = self.draft_dict[team][i]
                projected_points = player.curr_year_proj.get('PTS', 0)
                if projected_points == 0:
                    roster_count -= 1
                team_sum += projected_points
            avg_proj_points = round(team_sum / roster_count, 1)
            avg_projected_points_dict[team] = avg_proj_points

        roster_count = 22
        vorp_sum = 0
        for i in range(roster_count):
            player = sorted_full_roster[i]
            projected_points = player.curr_year_proj.get('PTS', 0)
            if projected_points == 0:
                roster_count -= 1
                vorp_sum += projected_points
            avg_proj_points = round(team_sum / roster_count, 1)
            avg_projected_points_dict['VORP'] = avg_proj_points

        power_rankings = []
        draft_rankings = []
        power_rankings = list(avg_projected_points_dict.values())
        power_rankings.sort(reverse=True)
        for i in range(len(power_rankings)):
            for key in avg_projected_points_dict.keys():
                val = power_rankings[i]
                if avg_projected_points_dict[key] == val:
                    draft_rankings.append({key: val})
        print("League Draft Grade Results:")
        print("=======================================================")
        for index, ranking in enumerate(draft_rankings):
            team = list(ranking.keys())[0]
            proj_points = list(ranking.values())[0]
            if index == len(self.teams):
                vorp_team = team
                vorp_proj_points = proj_points
                break
            print(f"{index + 1}. {team} with {proj_points} average projected points")
            print("=======================================================")

        print()
        print(f"{vorp_team} roster had {vorp_proj_points} average projected points")

        # Set up projected point for current year by team method in team file -> def teamProjectedPoints() -> return total projected points 
        
        # set dictionary with team name as key and difference between team projected points and VORP projected points as values in the dictionary

        # Determine how to assess grade level once the differences are obtained and can be seen and compared

        # Maybe don't return dictionary and just print the grades with the associated differences 


    # print each matchup result from the beginning of the season to the most recent completed matchup
    def printSeasonMatchupResults(self):
        self.matchup.seasonMatchupResults()

    def printWeeklyMatchupResults(self, index):
        self.matchup.weeklyMatchupResults(index)
        
    
    # method to print in order of best win-loss percentage to worst win-loss percentage with team name and associated season record
    def LeagueStandings(self):
        print(f"League Standings\n"
            "----------------------------------------------")
        # sort standings properly by matchup wins, set up max wins and prevRank variable to get proper position with tied records
        sorted_standings = sorted(self.standings, key=lambda standing: standing.wins, reverse=True)
        max_wins = sorted_standings[1].wins
        prevRank = 1

        # loop over standings
        for index, standing in enumerate(sorted_standings):
            # get next best team 
            team = self.teams[standing.team_name]
            # check for tie and set rank equal to prevRank
            if team.matchup_wins == max_wins:
                rank = prevRank
            # if not a tie, change max_wins
            # rank = position in list
            # prevRank = position in list for next iteration
            else:
                max_wins = team.matchup_wins
                rank = index + 1
                prevRank = rank
            # print the position in league followed by team method that prints team name and team season record
            print(f"{rank}. {team.displayTeamRecord(self.team_record_map)}\n"
                "----------------------------------------------")
        print("\n")

    def DivisionStandings(self, div_id):
        print(f"Division {div_id} Standings\n"
            "----------------------------------------------")
        # sort standings properly by matchup wins, set up max wins and prevRank variable to get proper position with tied records
        division_standings = []
        sorted_standings = sorted(self.standings, key=lambda standing: standing.wins, reverse=True)
        for standing in sorted_standings:
            if standing.division_id == div_id - 1:
                division_standings.append(standing)

        max_wins = division_standings[0].wins
        prevRank = 1

        # loop over standings
        for index, standing in enumerate(division_standings):
            # get next best team 
            team = self.teams[standing.team_name]
            # check for tie and set rank equal to prevRank
            if team.matchup_wins == max_wins:
                rank = prevRank
            # if not a tie, change max_wins
            # rank = position in list
            # prevRank = position in list for next iteration
            else:
                max_wins = team.matchup_wins
                rank = index + 1
                prevRank = rank
            # print the position in league followed by team method that prints team name and team season record
            print(f"{rank}. {team.displayTeamRecord(self.team_record_map)}\n"
                "----------------------------------------------")
        print("\n")



    # This method should print the round number followed by the order of draft with player name and team name in snake fashion
    def LeagueDraftResults(self):
        # **IDEA maybe calculate draft number as a player variable for a drafted player len(teams) * round + (j + 1) or len(teams) * round - k + 8 to use in each inner loop

        # initalize starter values like only 22 rounds of drafting for each team, draft_dict with all draft players
        # msg string to add to throughout, and draft_order with the teams in correct order
        DRAFT_ROUNDS = 22
        draft_dict = self.draft_dict
        # print(draft_dict)
        msg = ""
        DRAFT_ORDER = ["Luuky Pooky", "Dallin's Daring Team", "Shortcake Miniture Schnauzers",
                    "Live Laff Love", "Hockey", "Kings Shmings", "Dillon's Dubs", "Mind Goblinz"]
        # when player was picked, sort of intuitive since it is just incremented throughout
        # could be saved as a variable for a drafted player
        draft_num = 0
        
        # outer loop to iterate over for each round from 0-21
        for round in range(DRAFT_ROUNDS):
            # if else to check if round num is even
            if round % 2 == 0:
                # add draft round header
                msg += f"Round {round + 1} Draft Results \n-------------------------\n"
                # inner for loop to go in normal draft order based on number of teams (from 0-7)
                for j in range(len(self.teams)):
                    draft_num += 1 
                    # grab team name from draft_order
                    team = DRAFT_ORDER[j]
                    # grab player from dictionary with team name as key and grab player from list with round number
                    player = draft_dict[team][round]
                    # add player name, team name, and draft num in position format to msg string
                    if int(str(draft_num)[len(str(draft_num))-2:]) > 10 and int(str(draft_num)[len(str(draft_num))-2:]) < 14:
                        msg += f"{player.name} ({team}) - drafted {draft_num}th \n"
                    elif str(draft_num)[len(str(draft_num))-1] == "1":
                        msg += f"{player.name} ({team}) - drafted {draft_num}st \n"
                    elif str(draft_num)[len(str(draft_num))-1] == "2":
                        msg += f"{player.name} ({team}) - drafted {draft_num}nd \n"
                    elif str(draft_num)[len(str(draft_num))-1] == "3":
                        msg += f"{player.name} ({team}) - drafted {draft_num}rd \n"
                    else: 
                        msg += f"{player.name} ({team}) - drafted {draft_num}th \n"
                    # add a new line at the end of the loop for next round results
                    if (j == 7):
                        msg += "\n"
            # this logic happens if round number is not even
            else:
                # add draft round header
                msg += f"Round {round + 1} Draft Results \n-------------------------\n"
                # inner for loop to go in reverse order based on number of teams (7-0)
                for k in range(len(self.teams) - 1, -1, -1):
                    draft_num += 1
                    # get team name from draft_order
                    team = DRAFT_ORDER[k]
                    # get player from dictionary with team name as key and get the player from list using round number
                    player = draft_dict[team][round]
                    # add player name, team name and draft position to string output
                    if int(str(draft_num)[len(str(draft_num))-2:]) > 10 and int(str(draft_num)[len(str(draft_num))-2:]) < 14:
                        msg += f"{player.name} ({team}) - drafted {draft_num}th \n"
                    elif str(draft_num)[len(str(draft_num))-1] == "1":
                        msg += f"{player.name} ({team}) - drafted {draft_num}st \n"
                    elif str(draft_num)[len(str(draft_num))-1] == "2":
                        msg += f"{player.name} ({team}) - drafted {draft_num}nd \n"
                    elif str(draft_num)[len(str(draft_num))-1] == "3":
                        msg += f"{player.name} ({team}) - drafted {draft_num}rd \n"
                    else: 
                        msg += f"{player.name} ({team}) - drafted {draft_num}th \n"
                    # add a new line at the end of the for loop for next round results
                    if k == 0:
                        msg += "\n"

        # print string output after going through each round
        print(msg)

    # This method prints from best team to worst team in stat category
    def BestTeamStatSort(self, stat_name):
        # initialize empty list for stat_list, set reverseCheck to true for sorting from biggest to lowest
        # end of phrase is empty and stat alias too, will be used for print output checks
        stats_list = []
        reverseCheck = True
        end_of_phrase = ""
        stat_alias= ""

        # for loop in teams dictionary
        # check for existing stat variables 
        # else go into stat dictionary within team object method
        # stat alias is nicer output name for stat that differs from variable name
        # end of phrase is usually the stat alias without the ending 's' for singular version
        # will be changed for irregular singulars
        for team_name, team in self.teams.items():

            # logic for points_for
            if stat_name == "points_for":
                stat = team.points_for
                stat_alias = "Points For"
                end_of_phrase = stat_alias if stat != 1 else "Point For"

            # logic for points_against
            elif stat_name == "points_against":
                stat = team.points_against
                # reverse is switched to False since we want lowest to highest for this category
                reverseCheck = False
                stat_alias = "Points Against"
                end_of_phrase = stat_alias if stat != 1 else "Point Against"

            # logic for points_diff
            elif stat_name == "points_diff":
                stat = team.points_diff
                stat_alias = "Point Differential"

            # logic for matchup_wins
            elif stat_name ==  "matchup_wins":
                stat = team.matchup_wins
                stat_alias = "Matchup Wins"
                end_of_phrase = stat_alias if stat != 1 else stat_alias[:-1]

            # logic for matchup_losses
            elif stat_name == "matchup_losses":
                stat = team.matchup_losses
                reverseCheck = False
                stat_alias = "Matchup Losses"
                # subtract ending "es" instead of just the "s"
                end_of_phrase = stat_alias if stat != 1 else stat_alias[:-2]

            # logic for other more specific stats
            else:
                # use helper team object function to return necessary values for stats_list
                stat, stat_name, stat_alias, reverseCheck, end_of_phrase = team.getTeamStat(stat_name)

            # append the stat, team_name and end_of phrase to be used for printing
            stats_list.append([stat, team_name, end_of_phrase])

        # sort the stats_list based on reverseCheck, most often True for highest to lowest, sometimes set to False by stat to go from lowest to highest
        stats_list.sort(reverse=reverseCheck)

        # call print method that uses the stats_list and stat_alias to print proper ordering
        self.printTeamStatsChart(stats_list, stat_alias)
        
        # not sure if I need to return the stats_list
        # return stats_list 
    
    # prints the output of stats_list which is ordered from best team to worst team
    def printTeamStatsChart(self, stats_list, stat_alias):

        # formatting string variables by finding max length of strings
        max_team_name_length = max(len(stat[1]) for stat in stats_list)
        max_points_length = max(len(f"{stat[0]} {stat[2]}") for stat in stats_list)
        total_length = max_points_length + max_team_name_length + 10
            
            
        # print stat_title with formatting
        title = 'Team ' + stat_alias + ' Ranking Report'
        print(f"{'='*total_length}")
        print(f"{title}".center(total_length))
        print(f"{'='*total_length}")

        # set up values to help with check for ties
        prevRank = 1
        best_stat = stats_list[0][0]
        # for loop to go through stats list and print the stat val and stat end of phrase
        for index, stat in enumerate(stats_list):
            stat_value = stat[0]
            stat_end = stat[2]
            stat_info = f"{stat_value} {stat_end}"
            team_name = stat[1]

            # check for tie and use prevRank values
            if stat_value == best_stat:
                rank = prevRank
            # if there isn't a tie, set best_stat to new stat_value
            # set rank to position in list
            # set prevRank equal to rank for the future ties
            else:
                best_stat = stat_value
                rank = index + 1
                prevRank = rank

            # print format with position, team name and stat info 
            print(f"{rank:2}. {team_name.ljust(max_team_name_length)}: {stat_info.rjust(max_points_length)}")
            print(f"{'-'*total_length}")

        print() # new line after finishing method

    def printAllBestTeamStat(self):
        teams = []
        team_stats = ["points_for", "points_against", "points_diff", "matchup_wins", "matchup_losses"]
        for team in self.teams.values():
            teams.append(team)
        for key in teams[0].stats_dict.keys():
            team_stats.append(key)  
        for stat in team_stats:
            self.BestTeamStatSort(stat)

    def printTeamRosters(self):
        for team in self.teams.values():
            self.titleFormat(team)
            team.displayRoster()
            print()


    def printTeamByPoints(self):
        for team in self.teams.values():
            self.titleFormat(team)
            team.displayPointsSortedRoster()
            print()
            
    def printTeamByAvgPoints(self):
        for team in self.teams.values():
            self.titleFormat(team)
            team.displayAvgPointsSortedRoster()
            print()        

    def printDraftedTeam(self):
        for team in self.teams.values():
            self.titleFormat(team)
            team.displayDraftRoster()
            print()

    def titleFormat(self, team):
        title_length = len(team.name) + 5
        print(f"{team.name}".center(title_length))
        print(f"{"="*title_length}")

    # **I need to look over this and refactor it possibly
    # **Biggest need is to check if undrafted_players are all constructed correctly
    # Team lists with full rosters are being passed in somehow as well and are being removed with this code 
    # Maybe try to refactor, so team list objects aren't included in the rostered_players variable
    def printPlayersByAvgPoints(self):
        players_to_remove = []
        for player_key, player in self._rostered_players.items():
            if type(player) != Skater or type(player) != Goalie:
                players_to_remove.append(player_key)

        for player_key in players_to_remove:
            del self._rostered_players[player_key]

        sorted_rostered_players = sorted(self._rostered_players.values(), key=lambda player: player.avg_points, reverse=True)

        for index, player in enumerate(sorted_rostered_players):
            print(f"{index + 1}. {player.name} ({player.position}): [{player.avg_points} avg pts] - ({player.team})")

    # ** This needs to be refactored as well 
    # Team lists with full rosters are being passed in somehow as well and are being removed with this code 
    # Maybe try to refactor, so team list objects aren't included in the rostered_players variable
    def printPlayersByPoints(self):
        players_to_remove = []
        
        for player_key, player in self._rostered_players.items():
            if type(player) != Skater or type(player) != Goalie:
                players_to_remove.append(player_key)

        for player_key in players_to_remove:
            del self._rostered_players[player_key]

        sorted_rostered_players = sorted(self._rostered_players.values(), key=lambda player: player.points, reverse=True)

        for index, player in enumerate(sorted_rostered_players):
            # print(dir(player))
            print(f"{index + 1}. {player.name} ({player.position}): [{player.points} pts] - ({player.team})")
        
            
    def StreakReport(self, hot, players):
        def sort_players_by_degree(degree_list):
            # Sort players by point increase in descending order
            return sorted(degree_list, key=lambda player: player[1], reverse=True)
        
        if players == self.free_agents:
            roster = players
            if hot:
                print(f"Hot Streak Tracker for Free Agents:\n")
                first_degree, second_degree, third_degree, consistent = self.StreakTracker(hot, roster)
                full_second_degree = [(player, increase) for player, increase in first_degree 
                                  if any(player == p2[0] for p2 in second_degree)]
                full_third_degree = [(player, increase) for player, increase in full_second_degree 
                                  if any(player == p3[0] for p3 in third_degree)]
                sorted_first_degree = sort_players_by_degree(first_degree)
                sorted_second_degree = sort_players_by_degree(second_degree)
                sorted_third_degree = sort_players_by_degree(third_degree)
                sorted_full_second_degree = sort_players_by_degree(full_second_degree)
                sorted_full_third_degree = sort_players_by_degree(full_third_degree)
                sorted_consistent = []
                sorted_consistent.append(sort_players_by_degree(consistent[0]))
                sorted_consistent.append(sort_players_by_degree(consistent[1]))
                sorted_consistent.append(sort_players_by_degree(consistent[2]))
                self.hotStreakFullReport('', sorted_first_degree, sorted_second_degree, sorted_third_degree, sorted_full_second_degree, sorted_full_third_degree, sorted_consistent)
            else:
                print(f"Cold Streak Tracker for Free Agents:\n")
                cold_streak = self.StreakTracker(hot, roster)
                sorted_cold_streak = sort_players_by_degree(cold_streak)
                self.coldStreakFullReport('', cold_streak)

                        

        else:
            # team_list = []
            for index, team in enumerate(self.teams):
                # team_list.append(team.name)
                roster = players[team].players
                if hot:
                    if index == 0: 
                        print("Hot Streak Tracker for Rostered Players:\n")
                    first_degree, second_degree, third_degree, consistent = self.StreakTracker(hot, roster)
                    full_second_degree = [(player, increase) for player, increase in first_degree 
                                  if any(player == p2[0] for p2 in second_degree)]
                    full_third_degree = [(player, increase) for player, increase in full_second_degree 
                                  if any(player == p3[0] for p3 in third_degree)]
                    sorted_first_degree = sort_players_by_degree(first_degree)
                    sorted_second_degree = sort_players_by_degree(second_degree)
                    sorted_third_degree = sort_players_by_degree(third_degree)
                    sorted_full_second_degree = sort_players_by_degree(full_second_degree)
                    sorted_full_third_degree = sort_players_by_degree(full_third_degree)
                    sorted_consistent = []
                    sorted_consistent.append(sort_players_by_degree(consistent[0]))
                    sorted_consistent.append(sort_players_by_degree(consistent[1]))
                    sorted_consistent.append(sort_players_by_degree(consistent[2]))
                    self.hotStreakFullReport(team, sorted_first_degree, sorted_second_degree, sorted_third_degree, sorted_full_second_degree, sorted_full_third_degree, sorted_consistent)
                else:
                    if index == 0:
                        print("Cold Streak Tracker for Rostered Players:\n")
                    cold_streak = self.StreakTracker(hot, roster)
                    sorted_cold_streak = sort_players_by_degree(cold_streak)
                    self.coldStreakFullReport('', cold_streak)
    
                
    def StreakTracker(self, hot, roster):
        first_degree, second_degree, third_degree = [], [], []
        hot_3rd, consistent_3rd, cold_3rd = [], [], []
        hot_2nd, consistent_2nd, cold_2nd = [], [], []
        hot_1st, consistent_1st, cold_1st = [], [], []
        
        roster_map = {}
        player_report = {player: [[] for _ in range(3)] for player in roster}
        for player in roster:
            if player.position == "G":
                gp_key = "GS"
            else:
                gp_key = "GP"
            avg_points_total = player.avg_points
            points_7 = player.last_7_dict.get('PTS', 0)
            games_played_7 = player.last_7_dict.get(gp_key, 0)
            avg_points_7 = round(points_7 / games_played_7, 1) if games_played_7 != 0 else 0 
            avg_difference_7 = round(avg_points_7 - avg_points_total, 1)
            points_15 = player.last_15_dict.get('PTS', 0)
            games_played_15 = player.last_15_dict.get(gp_key, 0)
            avg_points_15 = round(points_15 / games_played_15, 1) if games_played_15 != 0  else 0
            avg_difference_15 = round(avg_points_15 - avg_points_total, 1)
            points_30 = player.last_30_dict.get('PTS', 0)
            games_played_30 = player.last_30_dict.get(gp_key, 0)
            avg_points_30 = round(points_30 / games_played_30, 1) if games_played_30 != 0  else 0
            avg_difference_30 = round(avg_points_30 - avg_points_total, 1)
            
            
            player_data = {
                "last_7_days": {
                    "points": points_7,
                    "games_played": games_played_7,
                    "avg_points": avg_points_7,
                    "avg_difference": avg_difference_7
                },
                "last_15_days": {
                    "points": points_15,
                    "games_played": games_played_15,
                    "avg_points": avg_points_15,
                    "avg_difference": avg_difference_15
                },
                "last_30_days": {
                    "points": points_30,
                    "games_played": games_played_30,
                    "avg_points": avg_points_30, 
                    "avg_difference": avg_difference_30
                }, 
                "avg_points": avg_points_total
            }
            roster_map[player] = player_data


            if games_played_30 > 0:
                if avg_points_30 > avg_points_total:
                    player_report[player][0].append("Hot")
                    roster_map[player]["last_30_days"]["streak"] = "Hot"
                elif avg_points_30 == avg_points_total:
                    player_report[player][0].append("Consistent")
                    roster_map[player]["last_30_days"]["streak"] = "Consistent"
                else:
                    player_report[player][0].append("Cold")
                    roster_map[player]["last_30_days"]["streak"] = "Cold"
            else: 
                player_report[player][0].append("_")
                roster_map[player]["last_30_days"]["streak"] = "N/A"

            if games_played_15 > 0:
                if avg_points_15 > avg_points_total:
                    player_report[player][1].append("Hot")
                    roster_map[player]["last_15_days"]["streak"] = "Hot"
                elif avg_points_15 == avg_points_total:
                    player_report[player][1].append("Consistent")
                    roster_map[player]["last_15_days"]["streak"] = "Consistent"
                else:
                    player_report[player][1].append("Cold")
                    roster_map[player]["last_15_days"]["streak"] = "Cold"
            else:
                player_report[player][1].append("_")
                roster_map[player]["last_15_days"]["streak"] = "N/A"

            if games_played_7 > 0:
                if avg_points_7 > avg_points_total:
                    player_report[player][2].append("Hot")
                    roster_map[player]["last_7_days"]["streak"] = "Hot"
                elif avg_points_7 == avg_points_total:
                    player_report[player][2].append("Consistent")
                    roster_map[player]["last_7_days"]["streak"] = "Consistent"
                else:
                    player_report[player][2].append("Cold")
                    roster_map[player]["last_7_days"]["streak"] = "Cold"
            else:
                player_report[player][2].append("_")
                roster_map[player]["last_7_days"]["streak"] = "N/A"

        

        maps = [["Hot"], ["Consistent"], ["Cold"], ["_"]] 
        player_order = {}
        for player in roster:
            # print(player.name)
            # print()
            player_priority = ""
            player_mapping = player_report[player]
            # print(player_mapping)
            # print()
            for map_idx in range(2, -1, -1):
                status = player_mapping[map_idx]
                # print(status)
                # print()
                if status in maps:
                    priority = maps.index(status)
                    player_priority = player_priority + str(priority)
                else:
                    # print("Status not found\n")
                    break

            player_order[player] = player_priority

        sorted_player_order = sorted(player_order.items(), key=lambda item: int(item[1]) if item[1] != '_' else 3)
        # print(sorted_player_order)
        
        first_code = "000"
        code_map = [first_code]
        full_streak_ordering = {}
        player_list = []
        for player in sorted_player_order:
            player_name = player[0] 
            code = player[1]
            if code != first_code:
                full_streak_ordering[first_code] = player_list
                code_map.append(code)
                first_code = code
                player_list = []
                # print("Code Change")
            player_list.append({player_name: roster_map[player_name]})

        full_streak_ordering[first_code] = player_list
        # print(full_streak_ordering) # sort the sub lists by iterating through code_map as keys and sorting by avg_30, avg_15, avg_7 and finally avg_total
        # use threshold to filter out players with an avg_total less than threshold for a scan of higher power players
        # print(code_map)
        code_map.remove("333")
        print(code_map)

        full_hot_3rd, full_hot_2nd, full_hot_1st, full_cons_3rd, full_cons_2nd, full_cons_1st, full_cold_3rd, full_cold_2nd, full_cold_1st =  [], [], [], [], [], [], [], [], []
        heating_up, cooling_down = [], []
        # full_cold_3rd, full_cold_2nd, full_cold_1st, full_empty_2nd, full_empty_1st  = [], [], [], [], [] all empty are full 3rd degree and pointless
        for code in code_map: 
            curr_code_streak = full_streak_ordering[code] 
            code_key = self.codeDecipher(code)
            streak_list_length = len(curr_code_streak)
            print(f"{streak_list_length} Players with {code_key[0]} 30 Day Streak | {code_key[1]} 15 Day Streak | {code_key[2]} 7 Day Streak\n\n")
            self.streakPrintFormat(curr_code_streak)
            for player in curr_code_streak: 
                # if code == "333":
                #     full_empty_3rd.append(player)
                # if code[-2:] == "33":
                #     full_empty_2nd.append(player)
                # if code[-1] == "3":
                #     full_empty_1st.append(player)
                if code == "000":
                    full_hot_3rd.append(player)
                if code[-2:] == "00":
                    full_hot_2nd.append(player)
                if code[-1] == "0":
                    full_hot_1st.append(player)
                if code == "111":
                    full_cons_3rd.append(player)
                if code[-2:] == "11":
                    full_cons_2nd.append(player)
                if code[-1] == "1":
                    full_cons_1st.append(player)
                if code == "222":
                    full_cold_3rd.append(player)
                if code[-2:] == "22":
                    full_cold_2nd.append(player)
                if code[-1] == "2":
                    full_cold_1st.append(player)
                if code == "222":
                    full_cold_3rd.append(player)
                if code[-2:] == "22":
                    full_cold_2nd.append(player)
                if code[-1] == "2":
                    full_cold_1st.append(player)

                if int(code[-1]) == int(code[-2]) + 1 and int(code[-2]) == int(code[-3]) + 1:
                    heating_up.append(player)

                if int(code[-3]) == int(code[-2]) + 1 and int(code[-2]) == int(code[-1]) + 1:
                    cooling_down.append(player)
                
                
        # full_hot_3rd = sorted(full_hot_3rd, key=lambda player: player.values()['avg_points'])
       
        # print("Full 2nd Degree Hot Streak:\n")
        # print(full_hot_2nd)
        # print()
        # print("Full 1st Degree Hot Streak:\n")
        # print(full_hot_1st)
        # print("\n\n")

        # print("Full 3rd Degree Conistent Streak:\n")
        # print(full_cons_3rd)
        # print()
        # print("Full 2nd Degree Conistent Streak:\n")
        # print(full_cons_2nd)
        # print()
        # print("Full 1st Degree Conistent Streak:\n")
        # print(full_cons_1st)
        # print("\n\n")
        
        # print("Full 3rd Degree Cold Streak:\n")
        # print(full_cons_3rd)
        # print()
        # print("Full 2nd Degree Cold Streak:\n")
        # print(full_cons_2nd)
        # print()
        # print("Full 1st Degree Cold Streak:\n")
        # print(full_cons_1st)
        # print("\n\n")

        # print("Players Trending Hot:\n")
        # print(heating_up)
        # print()
        # print("Players Trending Cold:\n")
        # print(cooling_down)
        # print("\n\n")

        

    def printStreakPlayers(self, full_streak_list):
        print("Printing Streak List:\n")
        player_list, skater_list, goalie_list = [], [], []
        for player in full_streak_list:
            player_object = list(player.keys())[0]
            if player_object.position != "G":
                skater_list.append(player_object)
            else:
                goalie_list.append(player_object)
            player_list.append(player_object)
        skater_list.sort(key=lambda player: player.avg_points, reverse=True)
        goalie_list.sort(key=lambda player: player.avg_points, reverse=True)
        player_list.sort(key=lambda player: player.avg_points, reverse=True)
        
        print("All Players:\n")
        # print(f"{player_list}\n")
        self.streakPrintFormat(player_list)

        print("Skaters:\n")
        # print(f"{skater_list}\n")   
        self.streakPrintFormat(skater_list)

        print("Goalies:\n")
        # print(f"{goalie_list}\n\n")
        self.streakPrintFormat(goalie_list)
        
    def streakPrintFormat(self, player_list):
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

            
            print(f"{index + 1}. {player_obj}:\n\n")
            if streak_30 == "Consistent":
                print(f"Last 30 Days: {streak_30} Streak maintaining {avg_points} avg points\n")
            elif streak_30 == "N/A":
                print(f"Last 30 Days: Not enough data to generate any anaylsis\n")
            else:
                print(f"Last 30 Days: {streak_30} Streak with change of {point_diff_30} from {avg_points} avg points\n")

            if streak_15 == "Consistent":
                print(f"Last 15 Days: {streak_15} Streak maintaining {avg_points} avg points\n")
            elif streak_15 == "N/A":
                print(f"Last 15 Days: Not enough data to generate any anaylsis\n")
            else:
                print(f"Last 15 Days: {streak_15} Streak with change of {point_diff_15} from {avg_points} avg points\n")

            if streak_7 == "Consistent":
                print(f"Last 7 Days: {streak_7} Streak maintaining {avg_points} avg points\n\n")
            elif streak_7 == "N/A":
                print(f"Last 7 Days: Not enough data to generate any anaylsis\n\n")
            else:
                print(f"Last 7 Days: {streak_7} Streak with change of {point_diff_7} from {avg_points} avg points\n\n")


        # print(full_hot_3rd)
        # print()
        
    def codeDecipher(self, code):
        code_key = []
        for idx in range(-3, 0):
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


        # maps key 
        # Full = 0
        # Consistent = 1
        # Cold = 2
        # Empty = 3
        # I think this should work for the most part Full 3rd degree 000 full second degree X00 first full degree XX0
                
            
            
                        

                


        # if hot:
        #     return first_degree, second_degree, third_degree, consistent
        # else:
        #     return cold_streak

        # first_degree is full already, full second degree is just the intersection of second and first, and then full third is intersection of third and 

    def hotStreakFullReport(self, team, first_degree, second_degree, third_degree, full_second_degree, full_third_degree, consistent):
        all_players = []
        if team:
            print(f"{team} Hot Streak Report:\n")

        print("Full 3rd Degree Hot Streak:\n")
        for player, increase_30 in full_third_degree:
            player_15 = next((p for p, inc in full_second_degree if p == player), None)
            player_7 = next((p for p, inc in first_degree if p == player), None)
            if player_15 and player_7:
                increase_15 = next(inc for p, inc in full_second_degree if p == player)
                increase_7 = next(inc for p, inc in first_degree if p == player)
                all_players.append(player)
                print(f"{player.name} had {increase_30:.2f} points above average over 30 days, {increase_15:.2f} points above average over 15 days, and {increase_7:.2f} points above average over 7 days \n")

        # self.hotStreakSingleReport(full_third_degree, all_players)
        
        print("Partial 3rd Degree Hot Streak:\n")
        self.hotStreakSingleReport(third_degree, all_players)

        print("Full Second Degree Hot Streak:\n")
        for player, increase_15 in full_second_degree:
            if player not in all_players:
                player_7 = next((p for p, inc in first_degree if p == player), None)
                if player_7:
                    increase_7 = next(inc for p, inc in first_degree if p == player)
                    all_players.append(player)
                    print(f"{player.name} had {increase_15:.2f} points above average over 15 days, and {increase_7:.2f} points above average over 7 days \n")

        # self.hotStreakSingleReport(full_second_degree, all_players)

        print("Partial 2nd Degree Hot Streak:\n")
        self.hotStreakSingleReport(second_degree, all_players)

        print("Full First Degree Hot Streak:\n")
        for player, increase_7 in first_degree:
            if player not in all_players:
                all_players.append(player)
                print(f"{player.name} had {increase_7:.2f} points above average over 7 days \n")

        title = ["1st Level Room Temp Players", "2nd Level Room Temp Players List", "3rd Level Room Temp Players List"]
        for i in range(2, -1, -1):
            print(f"{title[i]}:\n")
            self.hotStreakSingleReport(consistent[i], all_players)
        
    def hotStreakSingleReport(self, streak_list, all_players):
        for index, player in enumerate(streak_list):
            player_obj = player[0]
            avg_points_increase = player[1]
            if player_obj in all_players:
                continue
            all_players.append(player_obj)
            print(f"{index+1}. {player_obj.name} with {avg_points_increase}\n")

    def createLeague():
        # Initialize all necessary variables to be passed into League constructor
        _season_points = League._get_Season_Points()
        _points_for = _season_points[0]
        _points_against = _season_points[1]
        _points_diff = _season_points[2]
        _free_agents = League._get_Free_Agents()
        _roster_players = League._construct_Players(League._get_Rostered_Players(), "R")
        _draft_dict = League._get_Drafted_Players(_roster_players, _free_agents)
        _box_scores = League._get_Box_Scores()
        _recent_activity = League._get_Recent_Activity()
        _player_map = League._get_Player_Map()
        _league_standings = League._get_League_Standings()
        _curr_matchup_period = League._get_Curr_Matchup_Period()
        _league_settings = League._get_League_Settings()
        _team_objects = League._initialize_Team_Objects(_points_for, _points_against, _points_diff, _draft_dict)

        new_league = MyLeague(_team_objects, _box_scores, _draft_dict, _roster_players, _free_agents, 
                            _recent_activity, _player_map, _league_standings, _curr_matchup_period, _league_settings)
        
        return new_league
    
    

    