import League
import Player

class MyLeague:
    def __init__(self, teams, matchups, draft, rostered_players, free_agents, recent_activity, player_map, standings, curr_matchup_period, settings):
        self.teams = teams
        self.matchups = matchups
        self.draft = draft
        self._rostered_players = rostered_players
        self.free_agents = free_agents
        self.recent_activity = recent_activity
        self.player_map = player_map
        self.standings = standings
        self.curr_matchup_period = curr_matchup_period
        self.settings = settings

        self._all_players = self._get_All_Players()
        self._undrafted_players = self._get_Undrafted_Players()
        

    # def _get_Rostered_Players(self):
    #     rostered_players = []
    #     for team in self.teams.values():
    #         for player in team.players:
    #             rostered_players.append(player)
    #     return rostered_players
    
    # def _get_Unrostered_Players(self):
    #     my_team = self.teams["Dillon's Dubs"]
    #     unrostered_players = _construct_Available_Players(_get_Available_Players())
    #     return unrostered_players
    
    
    def _get_All_Players(self):
        all_players = self.free_agents
        for players in self._rostered_players.values():
            for player in players:
                all_players.append(player)
        return all_players

    def _get_Undrafted_Players(self):
        all_players = self._all_players
        _free_agents = League._construct_Players(League._get_Available_Players(), 'FA')
        _roster_players = League._construct_Players(League._get_Rostered_Players(), "R")
        drafted_players = League._get_Drafted_Players(_roster_players, _free_agents)
        undrafted_players = [player for player in all_players if player not in drafted_players.values() and type(player) == Player]
        sorted_undrafted_players = sorted(undrafted_players, key=lambda player: player.curr_year_proj)
        # print(sorted_undrafted_players)
        return sorted_undrafted_players 
    
    def LeagueDraftGrade(self):
        undrafted_players = self._undrafted_players
        forward_players = []
        defense_players = []
        goalie_players = []
        max_d_count = 11
        min_d_count = 5
        max_g_count = 4
        min_g_count = 2
        max_f_count = 15
        min_f_count = 9
        total_count = 22

        for player in undrafted_players:
            if player.position == 'F':
                forward_players.append(player)
            elif player.position == 'D':
                defense_players.append(player)
            elif player.position == 'G':
                goalie_players.append(player)
        min_position_roster = []
        min_position_roster.extend(forward_players[i] for i in range(min_f_count))
        min_position_roster.extend(defense_players[i] for i in range(min_d_count))
        min_position_roster.extend(goalie_players[i] for i in range(min_g_count))
        f_count = min_f_count
        d_count = min_d_count
        g_count = min_g_count
        full_roster = min_position_roster.copy()
        
        for player in undrafted_players:
            if f_count + d_count + g_count == total_count:
                break
            if player in full_roster:
                continue
            else:
                if player in forward_players and f_count < max_f_count:
                    f_count += 1
                    full_roster.append(player)
                elif player in defense_players and d_count < max_d_count:
                    d_count += 1
                    full_roster.append(player)
                elif player in goalie_players and g_count < max_g_count:
                    g_count += 1 
                    full_roster.append(player)
                
            
        print(f"Forwards: {f_count}\t Defensemen: {d_count}\t Goalies: {g_count}")
        for index, player in enumerate(full_roster, 1):
            # print(player.curr_year_proj)
            print(f"{index}. {player.name} - {player.position} [{player.curr_year_proj.get('PTS', 0)}]")

        

        # do something with draftPicks to maybe store drafted players by team in dictionaries
        # then figure out grading score with remaining players

    def printWeekMatchupResults(self, weekNum):
        matchups = self.matchups[weekNum] # get the matches of the week
        print(f"\nWeek {weekNum + 1} Winners: \n")
        for i in range(len(self.teams) // 2): # Iterate over the number of matches per week
            curr_matchup = matchups[i]
            if (curr_matchup.home_score > curr_matchup.away_score):
                winning_team = curr_matchup.home_team.team_name
                winning_score = curr_matchup.home_score
                losing_team = curr_matchup.away_team.team_name
                losing_score = curr_matchup.away_score
            
            else:
                winning_team = curr_matchup.away_team.team_name
                winning_score = curr_matchup.away_score  
                losing_team = curr_matchup.home_team.team_name
                losing_score = curr_matchup.home_score

            score_deficit = round(winning_score - losing_score, 1)
            print(f"{winning_team}({winning_score} pts) won against {losing_team}({losing_score} pts) by {score_deficit} pts \n")


    def printSeasonMatchupResults(self):
        for i in range(0, self.curr_matchup_period):
            self.printWeekMatchupResults(i)

    def LeagueStandings(self):
        print(f"League Standings\n"
            "------------------------------------")
        for i in range(len(self.standings)):
            team = self.teams[self.standings[i].team_name]
            print(f"{i+1}. {team.displayTeamRecord()}\n"
                "------------------------------------")
        print("\n")

    def LeagueDraftResults(self):
        DRAFT_ROUNDS = 22
        draft_dict = self.draft
        print(draft_dict)
        msg = ""
        DRAFT_ORDER = ["Luuky Pooky", "Dallin's Daring Team", "Shortcake Miniture Schnauzers",
                    "Live Laff Love", "Hockey", "Kings Shmings", "Dillon's Dubs", "Mind Goblinz"]
        for i in range(DRAFT_ROUNDS):
            if i % 2 == 0:
                msg += f"Round {i + 1} Draft Results \n-------------------------\n"
                for j in range(len(self.teams)):
                    team = DRAFT_ORDER[j]
                    player = draft_dict[team][i]
                    msg += f"{player.name} ({team}) \n"
                    if (j == 7):
                        msg += "\n"
            else:
                msg += f"Round {i + 1} Draft Results \n-------------------------\n"
                for k in range(len(self.teams) - 1, -1, -1):
                    team = DRAFT_ORDER[k]
                    player = draft_dict[team][i]
                    msg += f"{player.name} ({team}) \n"
                    if k == 0:
                        msg += "\n"

        print(msg)
    def LeagueRecord(self):
        for team in self.teams.values():
            self.titleFormat(team)
            team.displayTeamRecord()
            print()


    def BestTeamStatSort(self, stat_name):
        stats_list = []
        reverseCheck = True
        end_of_phrase = ""
        stat_alias= ""

        for team_name, team in self.teams.items():
            if stat_name == "points_for":
                stat = team.points_for
                stat_alias = "Points For"
                end_of_phrase = stat_alias if stat != 1 else "Point For"
            elif stat_name == "points_against":
                stat = team.points_against
                reverseCheck = False
                stat_alias = "Points Against"
                end_of_phrase = stat_alias if stat != 1 else "Point Against"
            elif stat_name == "points_diff":
                stat = team.points_diff
                stat_alias = "Point Differential"
            elif stat_name ==  "matchup_wins":
                stat = team.matchup_wins
                stat_alias = "Matchup Wins"
                end_of_phrase = stat_alias if stat != 1 else stat_alias[:-1]
            elif stat_name == "matchup_losses":
                stat = team.matchup_losses
                reverseCheck = False
                stat_alias = "Matchup Losses"
                end_of_phrase = stat_alias if stat != 1 else stat_alias[:-2]
            else:
                stat, stat_name, stat_alias, reverseCheck, end_of_phrase = team.getTeamStat(stat_name)

            stats_list.append([stat, team_name, end_of_phrase])
        
        stats_list.sort(reverse=reverseCheck)
        self.printTeamStatsChart(stats_list, stat_alias)
        
    
        return stats_list
    
    def printTeamStatsChart(self, stats_list, stat_alias):
        max_team_name_length = max(len(stat[1]) for stat in stats_list)
        max_points_length = max(len(f"{stat[0]} {stat[2]}") for stat in stats_list)
        total_length = max_points_length + max_team_name_length + 10
            
            

        title = 'Team ' + stat_alias + ' Ranking Report'
        print(f"{'='*total_length}")
        print(f"{title}".center(total_length))
        print(f"{'='*total_length}")

        
        team_rank = 0
        
        for stat in stats_list:
            stat_print = f"{stat[0]} {stat[2]}"
            team_rank += 1
            team_name = stat[1]
            print(f"{team_rank:2}. {team_name.ljust(max_team_name_length)}: {stat_print.rjust(max_points_length)}")
            print(f"{'-'*total_length}")

        print()

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

    def printPlayersByAvgPoints(self):
        players_to_remove = []
        for player_key, player in self._rostered_players.items():
            if not hasattr(player, 'avg_points'):
                print(f"Invalid player: {player}, Type: {type(player)}")
                players_to_remove.append(player_key)

        for player_key in players_to_remove:
            del self._rostered_players[player_key]

        sorted_rostered_players = sorted(self._rostered_players, key=lambda player: player.avg_points, reverse=True)

        for index, player in enumerate(sorted_rostered_players):
            print(f"{index + 1}. {player.name} ({player.position}): [{player.avg_points} avg pts] - ({player.team})")

    def printPlayersByPoints(self):
        for player in self._rostered_players:
            if not hasattr(player, 'points'):
                print(f"Invalid player: {player.name}, Type: {type(player)}")

        sorted_rostered_players = sorted(self._rostered_players, key=lambda player: player.points, reverse=True)

        for index, player in enumerate(sorted_rostered_players):
            print(dir(player))
            print(f"{index + 1}. {player.name} ({player.position}): [{player.points} pts] - ({player.team})")
        
            




def createLeague():
    # Initialize all necessary variables to be passed into League constructor
    _season_points = League._get_Season_Points()
    _points_for = _season_points[0]
    _points_against = _season_points[1]
    _points_diff = _season_points[2]
    _free_agents = League._construct_Players(League._get_Available_Players(), 'FA')
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
    
    

    