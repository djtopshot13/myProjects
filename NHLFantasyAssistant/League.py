from espn_api.hockey import League as ESPNLeague
from Team import Team
from Skater import Skater
from Goalie import Goalie

my_league_id = 1705592891
curr_year = 2025 
SWID = "73AF0A56-8B05-4B4C-8291-A431308556FD"
espn_s2_cookie = "AEAVePfqAj5sDj5KBoDdTQ7y7U5IcQaWswzMsomuzV%2B7u46Q29tOY56LRtFJucWWRyOD5FDujuOHqSG1LLa7NFXOJpW3jop3hgfmFglevS90tpTgw8tNRQLzznnrevnaIc5FZ8xE6b71AeemRUYSMnU1nT85QOi28kPbUd%2FN1WV45DPhzlbMb0YnUyXGba5HNLt17B7qiJWTIA0OlsPU50RsJ0meAG0YtMyP%2BUUvdg6GoddBkRS7tmy52bZ7kijTQW5eyARkXXTTfI5ymUCrbCDCgd%2BsIcolYdmjEbpIjg7KmA%3D%3D"


my_nhl_league = ESPNLeague(league_id=my_league_id, year=curr_year, espn_s2=espn_s2_cookie, swid=SWID, fetch_league=True)
def _construct_Players(players_list, player_type):
    new_players = []
      
    if player_type == 'FA':
        roster_availability = "Free Agent"
        team = ""

        for player in players_list:
            prev_year_proj = player.stats.get('Projected 2024', {}).get('total', {})
            prev_year_total = player.stats.get('Total 2024', {}).get('total', {})
            curr_year_proj = player.stats.get('Projected 2025', {}).get('total', {})
            curr_year_total = player.stats.get('Total 2025', {}).get('total', {})
            last_7_dict = player.stats.get('Last 7 2025', {}).get('total', {})
            last_15_dict = player.stats.get('Last 15 2025', {}).get('total', {})
            last_30_dict = player.stats.get('Last 30 2025', {}).get('total', {})
                        

            points = playerFantasyPointCalculator(player)
            health_status = player.injuryStatus

            prev_year_proj['PTS'] = points.get('Projected 2024', 0)
            prev_year_total['PTS'] = points.get('Total 2024', 0)
            curr_year_proj['PTS'] = points.get('Projected 2025', 0)
            curr_year_total['PTS'] = points.get('Total 2025', 0)
            last_7_dict['PTS'] = points.get('Last 7 2025', 0)
            last_15_dict['PTS'] = points.get('Last 15 2025', 0)
            last_30_dict['PTS'] = points.get('Last 30 2025', 0)

            if player.position[0] == 'G':
                games_played = curr_year_total.get('GS', 0)
                goals_against = curr_year_total.get('GA', 0)
                average_goals_against = curr_year_total.get('GAA', 0)
                shutouts = curr_year_total.get('SO', 0) 
                wins = curr_year_total.get('W', 0)
                losses = curr_year_total.get('L', 0)
                ot_losses = curr_year_total.get('OTL', 0)
                saves = curr_year_total.get('SV', 0)
                save_percentage = curr_year_total.get('SV%', 0)
                new_player = Goalie(player.name, team, player.proTeam, 'G', curr_year_total.get('PTS', 0), games_played, health_status, 
                                    roster_availability, prev_year_proj, prev_year_total, curr_year_proj, curr_year_total, last_7_dict, last_15_dict,
                                    last_30_dict, goals_against, average_goals_against, shutouts, wins, losses, ot_losses, saves, save_percentage)

            else:
                games_played = curr_year_total.get('GP', 0)
                skater_types = {'Center': 'C', 'Left Wing': 'LW', 'Right Wing': 'RW', 'Defense': 'D'}
                player_pos_initial = 'D' if player.position == 'Defense' else 'F'
                skater_position = skater_types[player.position]
                goals = curr_year_total.get('G', 0)
                assists = curr_year_total.get('A', 0)
                pp_points = curr_year_total.get('PPP', 0)
                sh_points = curr_year_total.get('SHP', 0)
                shots_on_goal = curr_year_total.get('SOG', 0)
                hits = curr_year_total.get('HIT', 0)
                blocked_shots = curr_year_total.get('BLK', 0)
                
                new_player = Skater(player.name, team, player.proTeam, player_pos_initial, curr_year_total.get('PTS', 0), games_played,
                        health_status, roster_availability, prev_year_proj, prev_year_total, curr_year_proj,  curr_year_total, last_7_dict,
                        last_15_dict, last_30_dict, skater_position, goals, assists, pp_points, sh_points, shots_on_goal, hits, blocked_shots)

            new_players.append(new_player)

    else:
        new_players = {team.team_name: [] for team in my_nhl_league.teams}
        for team, players in players_list.items():
            for player in players:

                roster_availability = "Rostered"

        
                prev_year_proj = player.stats.get('Projected 2024', {}).get('total', {})
                prev_year_total = player.stats.get('Total 2024', {}).get('total', {})
                curr_year_proj = player.stats.get('Projected 2025', {}).get('total', {})
                curr_year_total = player.stats.get('Total 2025', {}).get('total', {})
                last_7_dict = player.stats.get('Last 7 2025', {}).get('total', {})
                last_15_dict = player.stats.get('Last 15 2025', {}).get('total', {})
                last_30_dict = player.stats.get('Last 30 2025', {}).get('total', {})
                            

                points = playerFantasyPointCalculator(player)
                health_status = player.injuryStatus

                prev_year_proj['PTS'] = points.get('Projected 2024', 0)
                prev_year_total['PTS'] = points.get('Total 2024', 0)
                curr_year_proj['PTS'] = points.get('Projected 2025', 0)
                curr_year_total['PTS'] = points.get('Total 2025', 0)
                last_7_dict['PTS'] = points.get('Last 7 2025', 0)
                last_15_dict['PTS'] = points.get('Last 15 2025', 0)
                last_30_dict['PTS'] = points.get('Last 30 2025', 0)

                if player.position[0] == 'G':
                    games_played = curr_year_total.get('GS', 0)
                    goals_against = curr_year_total.get('GA', 0)
                    average_goals_against = curr_year_total.get('GAA', 0)
                    shutouts = curr_year_total.get('SO', 0) 
                    wins = curr_year_total.get('W', 0)
                    losses = curr_year_total.get('L', 0)
                    ot_losses = curr_year_total.get('OTL', 0)
                    saves = curr_year_total.get('SV', 0)
                    save_percentage = curr_year_total.get('SV%', 0)
                    new_player = Goalie(player.name, team, player.proTeam, 'G', curr_year_total.get('PTS', 0), games_played, health_status, 
                                        roster_availability, prev_year_proj, prev_year_total, curr_year_proj, curr_year_total, last_7_dict, last_15_dict,
                                        last_30_dict, goals_against, average_goals_against, shutouts, wins, losses, ot_losses, saves, save_percentage)

                else:
                    games_played = curr_year_total.get('GP', 0)
                    skater_types = {'Center': 'C', 'Left Wing': 'LW', 'Right Wing': 'RW', 'Defense': 'D'}
                    player_pos_initial = 'D' if player.position == 'Defense' else 'F'
                    skater_position = skater_types[player.position]
                    goals = curr_year_total.get('G', 0)
                    assists = curr_year_total.get('A', 0)
                    pp_points = curr_year_total.get('PPP', 0)
                    sh_points = curr_year_total.get('SHP', 0)
                    shots_on_goal = curr_year_total.get('SOG', 0)
                    hits = curr_year_total.get('HIT', 0)
                    blocked_shots = curr_year_total.get('BLK', 0)
                    
                    new_player = Skater(player.name, team, player.proTeam, player_pos_initial, curr_year_total.get('PTS', 0), games_played,
                            health_status, roster_availability, prev_year_proj, prev_year_total, curr_year_proj,  curr_year_total, last_7_dict,
                            last_15_dict, last_30_dict, skater_position, goals, assists, pp_points, sh_points, shots_on_goal, hits, blocked_shots)

                new_players[team].append(new_player)
    
    return new_players

def playerFantasyPointCalculator(player):
        headings = ['Projected 2024', 'Total 2024', 'Total 2025', 'Projected 2025', 'Last 7 2025', 'Last 15 2025', 'Last 30 2025']
        points_dict = {}
        for header in headings:
            if header in player.stats:
                points = goals_against = saves = wins = shutouts = overtime_losses = goals = assists = shots = hits = blocked_shots = pp_points = sh_points = 0
                if player.eligibleSlots[0][0] == 'G':
                    goals_against = player.stats[header].get('total', {}).get('GA', 0) * -2
                    saves = round(player.stats[header].get('total', {}).get('SV', 0) / 5, 1)
                    shutouts = player.stats[header].get('total', {}).get('SO', 0) * 3
                    wins = player.stats[header].get('total', {}).get('W', 0) * 4
                    overtime_losses = player.stats[header].get('total', {}).get('OTL', 0)
                else: 
                    goals = player.stats[header].get('total', {}).get('G', 0) * 2
                    assists = player.stats[header].get('total', {}).get('A', 0)
                    shots = round(player.stats[header].get('total', {}).get('SOG', 0) / 10, 1)
                    hits = round(player.stats[header].get('total', {}).get('HIT', 0) / 10, 1)
                    blocked_shots = round(player.stats[header].get('total', 0).get('BLK', 0) / 2, 1)
                    pp_points = round(player.stats[header].get('total', {}).get('PPP', 0) / 2, 1)
                    sh_points = round(player.stats[header].get('total', {}).get('SHP', 0) / 2, 1)
                
                points = goals_against + saves + shutouts + wins + overtime_losses + goals + assists + shots + hits + blocked_shots + pp_points + sh_points
                points_dict[header] = round(points, 1)
            else:
                continue
            
        return points_dict

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



def _get_Available_Players():
    FREE_AGENCY_SIZE = 1500 # Some extra padding since actual num is 1404 players
    available_players = my_nhl_league.free_agents(my_nhl_league.current_week, FREE_AGENCY_SIZE)
    return available_players

# def _get_Draft_Dict():
#     draft_dict = {team.team_name: [] for team in my_nhl_league.teams}
#     for pick in my_nhl_league.draft:
#         draft_dict[pick.team.team_name].append(pick.playerName)
#     return draft_dict

def _get_Drafted_Players(rostered_players, free_agents):
        draft_roster = {team.team_name: [] for team in my_nhl_league.teams}
        draft = my_nhl_league.draft
        for pick in draft:
            for players in rostered_players.values():
                for player in players:
                    if pick.playerName == "Sebastian Aho" and player.position == "Defense":
                        break
                    if pick.playerName == player.name:
                        player.team = pick.team.team_name
                        player.rosterAvailability = "Drafted"
                        
                        draft_roster[player.team].append(player)
                    
            for player in free_agents:
                if pick.playerName == "Sebastian Aho" and player.position == "Defense":
                    break
                if pick.playerName == player.name:
                    player.team = pick.team.team_name
                    player.rosterAvailability = "Drafted"
                    
                    draft_roster[player.team].append(player)
        return draft_roster

def _get_Rostered_Players():
    rostered_players = {team.team_name: [] for team in my_nhl_league.teams}
    for team in my_nhl_league.teams:
        for player in team.roster:
            rostered_players[team.team_name].append(player)

    return rostered_players
    
_roster_players = _construct_Players(_get_Rostered_Players(), "R")

def _initialize_Team_Objects(team_points_for, team_points_against, team_points_diff, _draft_dict):
    team_object_dict = {}
    for team_info in my_nhl_league.teams:
        team_info.stats['G&A'] = team_info.stats['16']
        del team_info.stats['16']
        team = Team(team_info.division_id, team_info.team_id, team_info.team_name,
                        _roster_players[team_info.team_name], team_points_for.get(team_info.team_name, 0), 
                        team_points_against.get(team_info.team_name, 0), team_points_diff.get(team_info.team_name, 0),
                        int(team_info.wins), int(team_info.losses), _draft_dict[team_info.team_name], team_info.stats)
        
        team_object_dict [team_info.team_name] = team

    return team_object_dict

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

        self._rostered_players = self._get_Rostered_Players()

    def _get_Rostered_Players(self):
        rostered_players = []
        for team in self.teams.values():
            for player in team.players:
                rostered_players.append(player)
        return rostered_players
    
    # def _get_Unrostered_Players(self):
    #     my_team = self.teams["Dillon's Dubs"]
    #     unrostered_players = _construct_Available_Players(_get_Available_Players())
    #     return unrostered_players
    
    
    

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
                    player = draft_dict[DRAFT_ORDER[j]][i]
                    team = DRAFT_ORDER[j]
                    msg += f"{player.name} ({team}) \n"
                    if (j == 7):
                        msg += "\n"
            else:
                msg += f"Round {i + 1} Draft Results \n-------------------------\n"
                for k in range(len(self.teams) - 1, -1, -1):
                    player = draft_dict[DRAFT_ORDER[k]][i]
                    team = DRAFT_ORDER[k]
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
        sorted_rostered_players = sorted(self._rostered_players, key=lambda player: player.avg_points, reverse=True)
        count = 0

        for player in sorted_rostered_players:
            count = count + 1
            print(f"{count}. {player.name} ({player.position}): [{player.avg_points} avg pts] - ({player.team})")

    def printPlayersByPoints(self):
        sorted_rostered_players = sorted(self._rostered_players, key=lambda player: player.avg_points, reverse=True)
        count = 0

        for player in sorted_rostered_players:
            count = count + 1
            print(f"{count}. {player.name} ({player.position}): [{player.points} pts] - ({player.team})")
        
            




def main():
    # Initialize all necessary variables to be passed into League constructor
    _season_points = _get_Season_Points()
    _points_for = _season_points[0]
    _points_against = _season_points[1]
    _points_diff = _season_points[2]
    _free_agents = _construct_Players(_get_Available_Players(), 'FA')
    _roster_players = _construct_Players(_get_Rostered_Players(), "R")
    _draft_dict = _get_Drafted_Players(_roster_players, _free_agents)
    _box_scores = _get_Box_Scores()
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
    # print()
    # new_league.printTeamByPoints()
    # print()
    # new_league.printTeamByAvgPoints() 
    # print()
    # new_league.printPlayersByAvgPoints()
    # print()
    new_league.printDraftedTeam()
    

main()

    