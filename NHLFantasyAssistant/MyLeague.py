import League
import Player
import Skater
import Goalie

class MyLeague:
    def __init__(self, teams, matchups, draft_dict, undrafted_dict, rostered_players, free_agents, recent_activity, player_map, standings, curr_matchup_period, settings):
        self.teams = teams
        self.matchups = matchups
        self.draft_dict = draft_dict
        self.undrafted_dict = undrafted_dict
        self._rostered_players = rostered_players
        self.free_agents = free_agents
        self.recent_activity = recent_activity
        self.player_map = player_map
        self.standings = standings
        self.curr_matchup_period = curr_matchup_period
        self.settings = settings

        # self._all_players = self._get_All_Players()
        
    # I don't think I need this method any more since there's already one in the regular League file now
    # def _get_Rostered_Players(self):
    #     rostered_players = []
    #     for team in self.teams.values():
    #         for player in team.players:
    #             rostered_players.append(player)
    #     return rostered_players
    
    # I don't know if I need to refactor this and see if I can get the unrostered players since I get free agents in the other League as well.
    # def _get_Unrostered_Players(self):
    #     my_team = self.teams["Dillon's Dubs"]
    #     unrostered_players = _construct_Available_Players(_get_Available_Players())
    #     return unrostered_players
    
    # Check to make sure that only player objects are added
    def _get_All_Players(self):
        all_players = []
        all_players = self.free_agents.copy()
        for players in self._rostered_players.values(): # double check that this only returns player objects and no other object typ
            for player in players: # nested list by team value possibly to iterate over
                all_players.append(player)
        return all_players # Should return a list that includes players from the free_agents list anad from rostered_players

    def _get_Undrafted_Players(self):
        all_players = self._all_players # Use all_players to iterate over and check both rostered and unrostered players for those that were drafted
        _free_agents = League._construct_Players(League._get_Available_Players(), 'FA')
        _roster_players = League._construct_Players(League._get_Rostered_Players(), 'R')
        drafted_players = League._get_Drafted_Players(_roster_players, _free_agents) # Should return dictionary of drafted_players with team as key
        undrafted_players = [player for player in all_players if player not in drafted_players.values() and type(player) == Player] # This doesn't work fully yet
        # It should add a player that is within all_players, but not within drafted_players
        sorted_undrafted_players = sorted(undrafted_players, key=lambda player: player.curr_year_proj, reverse=True) # Sort by projected values to get best expected players for draft grade
        # print(sorted_undrafted_players)
        return sorted_undrafted_players # return list of sorted_undrafted_players
    
    def LeagueDraftGrade(self):
        # Calculate VORP (Value of Remaining/Undrafted Players) with the most projected points
        # Compare the difference between each fantasy team's projected point total and the VORP projected points
        # Grade each team accordingly, the larger positive difference, the better the grade

        # initialize starter lists with undrafted_players and empty lists by player position
        undrafted_players = self.undrafted_dict
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
        print(f"Forwards: {f_count}\t Defensemen: {d_count}\t Goalies: {g_count}")
        # set print statement up to print the position in the player roster with projected points for the current year, name, and position
        # I might be able to sort it too if I wanted 
        sorted_full_roster = sorted(full_roster, key=lambda player: player.curr_year_proj.get('PTS', 0), reverse=True)
        for index, player in enumerate(sorted_full_roster, 1):
            # print(player.curr_year_proj)
            print(f"{index}. {player.displayUndraftedPlayerInfo()}")

        # Set up projected point for current year by team method in team file -> def teamProjectedPoints() -> return total projected points 
        
        # set dictionary with team name as key and difference between team projected points and VORP projected points as values in the dictionary

        # Determine how to assess grade level once the differences are obtained and can be seen and compared

        # Maybe don't return dictionary and just print the grades with the associated differences 


    # set up matchup results print method 
    # prints winning team name, losing team name, and the point margin that was won by
    def printWeekMatchupResults(self, weekNum):
        matchups = self.matchups[weekNum] # get the matches of the week using the weekNum parameter
        print(f"\nWeek {weekNum} Matchup Results: \n") # print header with which week is being represented
        for i in range(len(self.teams) // 2): # Iterate over the number of matches per week which should be 4 in this 8 team league
            curr_matchup = matchups[i] # use the week matchups and iterate from 0-3 to get all 4 matchups

            # set if else case to determine winning team based on being home or away since that's how the matchup object is set up
            # if home team wins 
            if (curr_matchup.home_score > curr_matchup.away_score):
                # winning team and winning score -> home team name and home team score
                # losing team and losing score -> away team name and away team score
                winning_team = curr_matchup.home_team.team_name
                winning_score = curr_matchup.home_score
                losing_team = curr_matchup.away_team.team_name
                losing_score = curr_matchup.away_score

            # else away team wins
            else:
                # winning team and winning score -> away team name and away team score
                # losing team and losing score -> home team name and home team score
                winning_team = curr_matchup.away_team.team_name
                winning_score = curr_matchup.away_score  
                losing_team = curr_matchup.home_team.team_name
                losing_score = curr_matchup.home_score

            # set up point margin by getting the difference between winning and losing score rounded to 1 decimal place
            score_deficit = round(winning_score - losing_score, 1)
            # print statement with winning team, winning score [win message] losing team and losing score with point margin
            print(f"{winning_team}({winning_score} pts) won against {losing_team}({losing_score} pts) by {score_deficit} pts \n")

    # print each matchup result from the beginning of the season to the most recent completed matchup
    def printSeasonMatchupResults(self):
        # Call printWeekMatchupResults in loop from beginning to most recent matchup period to show season results
        for i in range(1, self.curr_matchup_period):
            self.printWeekMatchupResults(i)
    
    # method to print in order of best win-loss percentage to worst win-loss percentage with team name and associated season record
    def LeagueStandings(self):
        print(f"League Standings\n"
            "-----------------------------------------")
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
            print(f"{rank}. {team.displayTeamRecord()}\n"
                "-----------------------------------------")
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

    # not sure if this is used 
    # I think I was trying to format the team record results 
    # and use this instead to print the standings
    # Check on this another time 

    # def LeagueRecord(self):
    #     for team in self.teams.values():
    #         self.titleFormat(team)
    #         team.displayTeamRecord()
    #         print()


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
        
            




    def createLeague():
        # Initialize all necessary variables to be passed into League constructor
        _season_points = League._get_Season_Points()
        _points_for = _season_points[0]
        _points_against = _season_points[1]
        _points_diff = _season_points[2]
        _free_agents = League._construct_Players(League._get_Available_Players(), 'FA')
        _roster_players = League._construct_Players(League._get_Rostered_Players(), "R")
        _draft_dict, _undrafted_dict = League._get_Drafted_Undrafted_Players(_roster_players, _free_agents)
        _box_scores = League._get_Box_Scores()
        _recent_activity = League._get_Recent_Activity()
        _player_map = League._get_Player_Map()
        _league_standings = League._get_League_Standings()
        _curr_matchup_period = League._get_Curr_Matchup_Period()
        _league_settings = League._get_League_Settings()
        _team_objects = League._initialize_Team_Objects(_points_for, _points_against, _points_diff, _draft_dict)

        new_league = MyLeague(_team_objects, _box_scores, _draft_dict, _undrafted_dict, _roster_players, _free_agents,
                            _recent_activity, _player_map, _league_standings, _curr_matchup_period, _league_settings)
        
        return new_league
    
    

    