from espn_api.hockey import League as ESPNLeague
from Team import Team

my_league_id = 1705592891
curr_year = 2025 
SWID = "73AF0A56-8B05-4B4C-8291-A431308556FD"
espn_s2_cookie = "AEAVePfqAj5sDj5KBoDdTQ7y7U5IcQaWswzMsomuzV%2B7u46Q29tOY56LRtFJucWWRyOD5FDujuOHqSG1LLa7NFXOJpW3jop3hgfmFglevS90tpTgw8tNRQLzznnrevnaIc5FZ8xE6b71AeemRUYSMnU1nT85QOi28kPbUd%2FN1WV45DPhzlbMb0YnUyXGba5HNLt17B7qiJWTIA0OlsPU50RsJ0meAG0YtMyP%2BUUvdg6GoddBkRS7tmy52bZ7kijTQW5eyARkXXTTfI5ymUCrbCDCgd%2BsIcolYdmjEbpIjg7KmA%3D%3D"

my_nhl_league = ESPNLeague(league_id=my_league_id, year=curr_year, espn_s2=espn_s2_cookie, swid=SWID, fetch_league=True)

def _get_Season_Points():
    _points_against = {team.team_name: 0 for team in my_nhl_league.teams}
    _points_for = {team.team_name: 0 for team in my_nhl_league.teams}
    _points_diff = {team.team_name: 0 for team in my_nhl_league.teams}

    for i in range(1, my_nhl_league.currentMatchupPeriod + 1):
        curr_matchups = my_nhl_league.box_scores(i)

        for matchup in curr_matchups:
            _points_against[matchup.home_team.team_name] += matchup.away_score
            _points_against[matchup.away_team.team_name] += matchup.home_score

            _points_for[matchup.away_team.team_name] += matchup.away_score            
            _points_for[matchup.home_team.team_name] += matchup.home_score

            _points_diff[matchup.home_team.team_name] += round(matchup.home_score - matchup.away_score, 1)
            _points_diff[matchup.away_team.team_name] += round(matchup.away_score - matchup.home_score, 1)
        

    for i in range(len(my_nhl_league.teams)):
        _points_against = {team: round(score, 1) for team, score in _points_against.items()}
        _points_for = {team: round(score, 1) for team, score in _points_for.items()}
        _points_diff = {team: round(score, 1) for team, score in _points_diff.items()}

        return _points_for, _points_against, _points_diff
        
def _get_Box_Scores():
    matchups = []
    for i in range(21):
        matchups.append(my_nhl_league.box_scores(i))
    return matchups

def _get_Recent_Activity():
    recent_activity = my_nhl_league.recent_activity()
    return recent_activity

def _get_League_Standings():
    standings = my_nhl_league.standings()
    return standings

def _get_League_Settings():
    settings = my_nhl_league.settings
    return settings

def _get_Player_Map():
    player_map = my_nhl_league.player_map
    return player_map

def _get_Curr_Matchup_Period():
    curr_matchup_period = my_nhl_league.currentMatchupPeriod
    return curr_matchup_period

def _initialize_Team_Objects(team_points_for, team_points_against, team_points_diff, _draft_dict):
    team_object_dict = {}
    for team_info in my_nhl_league.teams:
        team_info.stats['G&A'] = team_info.stats['16']
        del team_info.stats['16']
        team = Team(team_info.division_id, team_info.team_id, team_info.team_name,
                        team_info.roster, team_points_for.get(team_info.team_name, 0), 
                        team_points_against.get(team_info.team_name, 0), team_points_diff.get(team_info.team_name, 0),
                        int(team_info.wins), int(team_info.losses), _draft_dict[team_info.team_name], team_info.stats)
        
        team_object_dict [team_info.team_name] = team

    return team_object_dict

def _get_Available_Players():
    FREE_AGENCY_SIZE = 1500 # Some extra padding since actual num is 1404 players
    available_players = my_nhl_league.free_agents(my_nhl_league.current_week, FREE_AGENCY_SIZE)
    return available_players

def _get_Draft_Dict():
    draft_dict = {team.team_name: [] for team in my_nhl_league.teams}
    for pick in my_nhl_league.draft:
        draft_dict[pick.team.team_name].append(pick.playerName)
    return draft_dict

class League:
    def __init__(self, teams, matchups, draft, free_agents, recent_activity, player_map, standings, curr_matchup_period, settings):
        self.teams = teams
        self.matchups = matchups
        self.draft = draft
        self.free_agents = free_agents
        self.recent_activity = recent_activity
        self.player_map = player_map
        self.standings = standings
        self.curr_matchup_period = curr_matchup_period
        self.settings = settings

    def LeagueDraftGrade(self):
        return
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
        msg = ""
        DRAFT_ORDER = ["Luuky Pooky", "Dallin's Daring Team", "Shortcake Miniture Schnauzers",
                    "Live Laff Love", "Hockey", "Kings Shmings", "Dillon's Dubs", "Mind Goblinz"]
        for i in range(DRAFT_ROUNDS):
            if i % 2 == 0:
                msg += f"Round {i + 1} Draft Results \n-------------------------\n"
                for j in range(len(self.teams)):
                    msg += f"{draft_dict[DRAFT_ORDER[j]][i]} ({DRAFT_ORDER[j]}) \n"
                    if (j == 7):
                        msg += "\n"
            else:
                msg += f"Round {i + 1} Draft Results \n-------------------------\n"
                for k in range(len(self.teams) - 1, -1, -1):
                    msg += f"{draft_dict[DRAFT_ORDER[k]][i]} ({DRAFT_ORDER[k]}) \n"
                    if k == 0:
                        msg += "\n"

        print(msg)

    def LeagueRecord(self):
        for team in self.teams.values():
            self.titleFormat(team)
            team.displayTeamRecord()
            print()

    # Debug the points for, points against, and point diff stuff. Also, something is wrong with pluralization of output on some as well.

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
            team.displayAvgPointsSortedRoster()
            print()
            
    def printTeamByAvgPoints(self):
        for team in self.teams.values():
            self.titleFormat(team)
            team.displayAvgPointsSortedRoster()
            print()        

    def titleFormat(self, team):
        title_length = len(team.name) + 5
        print(f"{team.name}".center(title_length))
        print(f"{"="*title_length}")

    def printPlayersByAvgPoints(self):
        rostered_players = []
        for team in self.teams.values():
            for player in team.new_players:
                rostered_players.append(player)
        sorted_rostered_players = sorted(rostered_players, key=lambda player: player.avg_points, reverse=True)

        count = 0
        for player in sorted_rostered_players:
            count = count + 1
            print(f"{count}. {player.name} ({player.position}): [{player.avg_points}] - ({player.team})")
        
            




def main():
    # Initialize all necessary variables to be passed into League constructor
    _season_points = _get_Season_Points()
    _points_for = _season_points[0]
    _points_against = _season_points[1]
    _points_diff = _season_points[2]
    _draft_dict = _get_Draft_Dict()
    _box_scores = _get_Box_Scores()
    _free_agents = _get_Available_Players()
    _recent_activity = _get_Recent_Activity()
    _player_map = _get_Player_Map()
    _league_standings = _get_League_Standings()
    _curr_matchup_period = _get_Curr_Matchup_Period()
    _league_settings =_get_League_Settings()

    new_league = League(_initialize_Team_Objects(_points_for, _points_against, _points_diff, _draft_dict),
                    _box_scores, _draft_dict, _free_agents, _recent_activity, _player_map,
                    _league_standings, _curr_matchup_period, _league_settings)
    
    # new_league.printSeasonMatchupResults()
    # print()
    # new_league.LeagueStandings() 
    # print()
    # new_league.LeagueDraftResults()
    # print()
    # new_league.printAllBestTeamStat()
    # new_league.printTeamRosters()  
    # new_league.printTeamByPoints()
    # new_league.printTeamByAvgPoints() 
    new_league.printPlayersByAvgPoints()
    

main()

    