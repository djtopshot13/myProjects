from espn_api.hockey import League as ESPNLeague
import Team

my_league_id = 1705592891
curr_year = 2025 
SWID = "73AF0A56-8B05-4B4C-8291-A431308556FD"
espn_s2_cookie = "AEAVePfqAj5sDj5KBoDdTQ7y7U5IcQaWswzMsomuzV%2B7u46Q29tOY56LRtFJucWWRyOD5FDujuOHqSG1LLa7NFXOJpW3jop3hgfmFglevS90tpTgw8tNRQLzznnrevnaIc5FZ8xE6b71AeemRUYSMnU1nT85QOi28kPbUd%2FN1WV45DPhzlbMb0YnUyXGba5HNLt17B7qiJWTIA0OlsPU50RsJ0meAG0YtMyP%2BUUvdg6GoddBkRS7tmy52bZ7kijTQW5eyARkXXTTfI5ymUCrbCDCgd%2BsIcolYdmjEbpIjg7KmA%3D%3D"

my_nhl_league = ESPNLeague(league_id=my_league_id, year=curr_year, espn_s2=espn_s2_cookie, swid=SWID, fetch_league=True)

def _get_Season_Points():
    _points_against = {team.team_name: 0 for team in my_nhl_league.teams}
    _points_for = {team.team_name: 0 for team in my_nhl_league.teams}
    _points_diff = {team.team_name: 0 for team in my_nhl_league.teams}

    for i in range(1, my_nhl_league.currentMatchupPeriod):
        curr_matchups = my_nhl_league.box_scores(i)

        for matchup in curr_matchups:
            _points_against[matchup.home_team.team_name] += matchup.away_score
            _points_against[matchup.away_team.team_name] += matchup.home_score

            _points_for[matchup.away_team.team_name] += matchup.away_score            
            _points_for[matchup.home_team.team_name] += matchup.home_score
        
        _points_against = {team: round(score, 1) for team, score in _points_against.items()}
        _points_for = {team: round(score, 1) for team, score in _points_for.items()}

        for team in my_nhl_league.teams:
            _points_diff[team.team_name] = round(_points_for[team.team_name] - _points_against[team.team_name], 1)

        return _points_against, _points_for, _points_diff
        
            
            
# def _get_Season_Points_Against():
#     points_against = {team.team_name: 0 for team in my_nhl_league.teams}  
    
#     for i in range(1, my_nhl_league.currentMatchupPeriod + 1):
#         curr_matchups = my_nhl_league.box_scores(i)
        
#         # Loop through the matchups and add points against for each team
#         for matchup in curr_matchups:
#             points_against[matchup.home_team.team_name] += matchup.away_score
#             points_against[matchup.away_team.team_name] += matchup.home_score

#     points_against = {team: round(score, 1) for team, score in points_against.items()}
#     return points_against


# def _get_Season_Points_For():
#     points_for = {team.team_name: 0 for team in my_nhl_league.teams}

#     for i in range(1, my_nhl_league.currentMatchupPeriod):
#         curr_matchups = my_nhl_league.box_scores(i)

#         for matchup in curr_matchups:
#             points_for[matchup.home_team.team_name] += matchup.home_score
#             points_for[matchup.away_team.team_name] += matchup.away_score

#     points_for = {team: round(score, 1) for team, score in points_for.items()}
#     return points_for

# def _get_Season_Point_Differential(_points_for, _points_against):
#     diff = {team.team_name: 0 for team in my_nhl_league.teams}
#     for team in my_nhl_league.teams:
#         diff[team.team_name] = round(_points_for[team.team_name] - _points_against[team.team_name], 1)
#     return diff
def _get_Box_Scores():
    matchups = my_nhl_league.box_scores(1, my_nhl_league.currentMatchupPeriod)
    print(matchups)
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
        team = Team.Team(team_info.division_id, team_info.team_id, team_info.team_name,
                        team_info.roster, team_points_for.get(team_info.team_name, 0), 
                        team_points_against.get(team_info.team_name, 0),team_points_diff.get(team_info.team_name, 0),
                        team_info.wins, team_info.losses, _draft_dict[team_info.team_name], team_info.stats)
        
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

new_league = League(_initialize_Team_Objects(_get_Season_Points()[0], _get_Season_Points()[1], _get_Season_Points()[2], _get_Draft_Dict()),
                    _get_Box_Scores(), _get_Draft_Dict(), _get_Available_Players(), _get_Recent_Activity(), _get_Player_Map(),
                      _get_League_Standings(), _get_Curr_Matchup_Period(), _get_League_Settings())

def TeamDraftGrade():
    return   
    # do something with draftPicks to maybe store drafted players by team in dictionaries
    # then figure out grading score with remaining players

def printWeekMatchupResults(weekNum):
    print(f"\nWeek {weekNum} Winners: \n")
    curr_matchups = my_nhl_league.box_scores(weekNum)
    for matchup in curr_matchups:
        if (matchup.winner == "HOME"):
                winning_team = matchup.home_team.team_name
                winning_score = matchup.home_score
                losing_team = matchup.away_team.team_name
                losing_score = matchup.away_score
        else:
            winning_team = matchup.away_team.team_name
            winning_score = matchup.away_score  
            losing_team = matchup.home_team.team_name
            losing_score = matchup.home_score
        score_deficit = round(winning_score - losing_score, 1)
        print(f"{winning_team}({winning_score} pts) won against {losing_team}({losing_score} pts) by {score_deficit} pts \n")


def printSeasonMatchupResults():
    for i in range(1, my_nhl_league.currentMatchupPeriod):
        printWeekMatchupResults(i)

def LeagueStandings(teams):
    standings = my_nhl_league.standings()
    print(f"League Standings\n"
          "------------------------------------")
    for i in range(len(standings)):
        team = teams[standings[i].team_name]
        print(f"{i+1}. {team.displayTeamRecord()}\n"
              "------------------------------------")
    print("\n")

def LeagueDraftResults(draft_dict):
    DRAFT_ROUNDS = 22
    msg = ""
    DRAFT_ORDER = ["Luuky Pooky", "Dallin's Daring Team", "Shortcake Miniture Schnauzers", "Live Laff Love", "Hockey", "Kings Shmings", "Dillon's Dubs", "Mind Goblinz"]
    for i in range(DRAFT_ROUNDS):
        if i % 2 == 0:
            msg += f"Round {i + 1} Draft Results \n-------------------------\n"
            for j in range(len(my_nhl_league.teams)):
                msg += f"{draft_dict[DRAFT_ORDER[j]][i]} ({DRAFT_ORDER[j]}) \n"
                if (j == 7):
                    msg += "\n"
        else:
            msg += f"Round {i + 1} Draft Results \n-------------------------\n"
            for k in range(len(my_nhl_league.teams) - 1, -1, -1):
                msg += f"{draft_dict[DRAFT_ORDER[k]][i]} ({DRAFT_ORDER[k]}) \n"
                if k == 0:
                    msg += "\n"

    print(msg)

def TeamRecord(team):
    team.displayTeamRecord()
        
def main():
    printSeasonMatchupResults()
    LeagueStandings(new_league.teams) 
    LeagueDraftResults(new_league.draft)

main()


