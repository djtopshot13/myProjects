from Utils import ESPNLeague
from .Skater import Skater
from .Goalie import Goalie
from ToolObjects import Matchup
from ToolObjects import RosterGrade
from ToolObjects import StreakTracker

class League:
    def __init__(self, teams, matchups, draft_dict, rostered_players, free_agents, recent_activity, player_map, standings, curr_matchup_period, settings):
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
        self.roster_grader = self._make_Roster_Grader()
        self.streak_tracker = self._make_Streak_Tracker()
        self.team_record_map = self.matchup.team_record_map
    
    def _make_Roster_Grader(self):
        sorted_free_agents = sorted(self.free_agents, key=lambda player: player.curr_year_total.get('PTS', 0), reverse=True)
        return RosterGrade.RosterGrade(self.teams, self.draft_dict, sorted_free_agents, self.undrafted_list)

    def _make_Matchup(self):
        return Matchup.Matchup(self.curr_matchup_period, self.matchups, self.teams)
    
    def _make_Streak_Tracker(self):
        return StreakTracker.StreakTracker(self.free_agents, self.teams)
    
    
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
                
                
                    

        # It should add a player that is within all_players, but not within drafted_players
        sorted_undrafted_players = sorted(undrafted_players, key=lambda player: player.curr_year_proj.get('PTS', 0), reverse=True) # Sort by projected values to get best expected players for draft grade
        
        return sorted_undrafted_players # return list of sorted_undrafted_players
    
    def leagueDraftPowerRankings(self):
        self.roster_grader.powerRankingReport(True)

    def leagueCurrPowerRankings(self):
        self.roster_grader.powerRankingReport(False)

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
        for key in teams[0].stats_keys_dict.keys():
            team_stats.append(key)  
        for stat in team_stats:
            self.BestTeamStatSort(stat)
    def pointPositionReport(self):
        goalie_points_dict = self.goaliePointReport()
        skater_points_dict = self.skaterPointReport()
        for team in self.teams.values():
            goalie_points = goalie_points_dict[team]
            skater_points = skater_points_dict[team]
            goalie_pt_pct = round(goalie_points / team.points_for * 100, 1)
            skater_pt_pct = round(skater_points / team.points_for * 100, 1)
            if (skater_pt_pct + goalie_pt_pct != 100):
                print(f"Error with {team} positional point percent report")
            else: 
                print(f"{team}: Percent of points by Goalie[{goalie_pt_pct}], Percent of points by Skaters[{skater_pt_pct}]")
    def goaliePointReport(self):
        
        goalie_point_dict = {}
        for team in self.teams.values():
            goalie_points = 0
            goalie_points += team.stats_dict["W"] * 4
            goalie_points += team.stats_dict["SO"] * 3
            goalie_points += team.stats_dict["OTL"]
            goalie_points += round(team.stats_dict['SV'] / 5, 1)
            goalie_points -= team.stats_dict['GA'] * 2
            goalie_points = round(goalie_points, 1)

            print(f"{team.name}: {goalie_points} points from goalies")
            goalie_point_dict[team] = goalie_points
        return goalie_point_dict
    
    def skaterPointReport(self):
        
        skater_point_dict = {}
        for team in self.teams.values():
            skater_points = 0
            skater_points += team.stats_dict["G"] * 2
            skater_points += team.stats_dict["A"]
            skater_points += round(team.stats_dict["BLK"] / 2, 1)
            skater_points += round(team.stats_dict['PPP'] / 2, 1)
            skater_points += round(team.stats_dict['SHP'] / 2, 1)
            skater_points += round(team.stats_dict["SOG"] / 10, 1)
            skater_points += round(team.stats_dict['HIT'] / 10, 1)
            skater_points = round(skater_points, 1)

            print(f"{team.name}: {skater_points} points from skaters")
            skater_point_dict[team] = skater_points
        return skater_point_dict
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
        
            
    def streakReport(self, team="all", position="all", streak_type="all", min_threshold=float("-inf"), max_threshold=float("inf"), pro_team="all"):
        self.streak_tracker.streakReport(team, position, streak_type, min_threshold, max_threshold, pro_team)


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

    # 

    def createLeague():
        # Initialize all necessary variables to be passed into League constructor
        _season_points = ESPNLeague._get_Season_Points()
        _points_for = _season_points[0]
        _points_against = _season_points[1]
        _points_diff = _season_points[2]
        _free_agents = ESPNLeague._get_Free_Agents()
        _roster_players = ESPNLeague._construct_Players(ESPNLeague._get_Rostered_Players(), "R")
        _draft_dict = ESPNLeague._get_Drafted_Players(_roster_players, _free_agents)
        _box_scores = ESPNLeague._get_Box_Scores()
        _recent_activity = ESPNLeague._get_Recent_Activity()
        _player_map = ESPNLeague._get_Player_Map()
        _league_standings = ESPNLeague._get_League_Standings()
        _curr_matchup_period = ESPNLeague._get_Curr_Matchup_Period()
        _league_settings = ESPNLeague._get_League_Settings()
        _team_objects = ESPNLeague._initialize_Team_Objects(_points_for, _points_against, _points_diff, _draft_dict)

        new_league = League(_team_objects, _box_scores, _draft_dict, _roster_players, _free_agents, 
                            _recent_activity, _player_map, _league_standings, _curr_matchup_period, _league_settings)
        
        return new_league
    
    

    