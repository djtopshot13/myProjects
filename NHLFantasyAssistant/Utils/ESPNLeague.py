from espn_api.hockey import League as ESPNLeague
from MainObjects.Team import Team
from MainObjects.Skater import Skater
from MainObjects.Goalie import Goalie

my_league_id = 1705592891
curr_year = 2025 
SWID = "73AF0A56-8B05-4B4C-8291-A431308556FD"
espn_s2_cookie = "AEAVePfqAj5sDj5KBoDdTQ7y7U5IcQaWswzMsomuzV%2B7u46Q29tOY56LRtFJucWWRyOD5FDujuOHqSG1LLa7NFXOJpW3jop3hgfmFglevS90tpTgw8tNRQLzznnrevnaIc5FZ8xE6b71AeemRUYSMnU1nT85QOi28kPbUd%2FN1WV45DPhzlbMb0YnUyXGba5HNLt17B7qiJWTIA0OlsPU50RsJ0meAG0YtMyP%2BUUvdg6GoddBkRS7tmy52bZ7kijTQW5eyARkXXTTfI5ymUCrbCDCgd%2BsIcolYdmjEbpIjg7KmA%3D%3D"

# Order of full stats 'Total 2024', 'Total 2025', 'Last 7 2025', 'Last 30 2025', 'Last 15 2025', 'Projected 2025', 'Projected 2024'

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
                # print(player.stats)
                games_started = curr_year_total.get('GS', 0)
                games_played = curr_year_total.get('GP', 0)
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
                                    last_30_dict, games_started, goals_against, average_goals_against, shutouts, wins, losses, ot_losses, saves, save_percentage)

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

        
                
                prev_year_total = player.stats.get('Total 2024', {}).get('total', {})
                curr_year_total = player.stats.get('Total 2025', {}).get('total', {})
                last_7_dict = player.stats.get('Last 7 2025', {}).get('total', {})
                last_15_dict = player.stats.get('Last 15 2025', {}).get('total', {})
                last_30_dict = player.stats.get('Last 30 2025', {}).get('total', {})
                prev_year_proj = player.stats.get('Projected 2024', {}).get('total', {})
                curr_year_proj = player.stats.get('Projected 2025', {}).get('total', {})
                            

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
                    # print(curr_year_total)
                    games_played = curr_year_total.get('GP', 0)
                    games_started = curr_year_total.get('GS', 0)
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
                                        last_30_dict, games_started, goals_against, average_goals_against, shutouts, wins, losses, ot_losses, saves, save_percentage)

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
        headings = ['Total 2024', 'Total 2025', 'Last 7 2025', 'Last 15 2025', 'Last 30 2025', 'Projected 2024', 'Projected 2025']
        points_dict = {}
        for header in headings:
            if header in player.stats:
                
                points = goals_against = saves = wins = shutouts = overtime_losses = goals = assists = shots = hits = blocked_shots = pp_points = sh_points = 0
                if player.position[0] == 'G':
                    if player.stats[header].get('total', {}).keys():
                        if '30' in player.stats[header]['total'].keys():
                            player.stats[header]['total']['GP'] = player.stats[header]['total']['30']
                            del player.stats[header]['total']['30']
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
        # undrafted_players = []
        # drafted_players = []

        draft_roster = {team.team_name: [] for team in my_nhl_league.teams}
        draft = my_nhl_league.draft
        for pick in draft:
            for players in rostered_players.values():
                for player in players:
                    if pick.playerName == player.name:
                        player.team = pick.team.team_name
                        player.rosterAvailability = "Drafted"
                        
                        draft_roster[player.team].append(player)
                        # drafted_players.append(player)
                    
            for player in free_agents:
                if pick.playerName == player.name:
                    player.team = pick.team.team_name
                    player.rosterAvailability = "Drafted"
                    
                    draft_roster[player.team].append(player)
                    # drafted_players.append(player)

        # for players in rostered_players.values():
        #     for player in players:
        #         if player not in drafted_players:
        #             undrafted_players.append(player)

        # for player in free_agents:
        #     if player not in drafted_players:
        #         undrafted_players.append(player)
        draft_roster["Dillon's Dubs"].pop(10) # get rid of duplicate Sebastian Aho skater object
        print(draft_roster)
        return draft_roster

def _get_Rostered_Players():
    rostered_players = {team.team_name: [] for team in my_nhl_league.teams}
    for team in my_nhl_league.teams:
        for player in team.roster:
            rostered_players[team.team_name].append(player)

    return rostered_players
    

def _get_Free_Agents():
    _available_players = _construct_Players(_get_Available_Players(), "FA")
    return _available_players

_roster_players = _construct_Players(_get_Rostered_Players(), "R")

def _initialize_Team_Objects(team_points_for, team_points_against, team_points_diff, _draft_dict):
    team_object_dict = {}
    for team_info in my_nhl_league.teams:
        team_info.stats['G&A'] = team_info.stats['16']
        del team_info.stats['16']
        team = Team(team_info.division_id + 1, team_info.team_id + 1, team_info.team_name,
                        _roster_players[team_info.team_name], team_points_for.get(team_info.team_name, 0), 
                        team_points_against.get(team_info.team_name, 0), team_points_diff.get(team_info.team_name, 0),
                        int(team_info.wins), int(team_info.losses), _draft_dict[team_info.team_name], team_info.stats)
        
        team_object_dict [team_info.team_name] = team

    # team_object_dict ["Free Agents"] = Team(3, 10, 'Free Agents', _available_players, team_points_for.get('Free Agents', 0), team_points_against.get('Free Agents', 0), team_points_diff.get('Free Agents', 0), 0, 0, {}, {})

    return team_object_dict