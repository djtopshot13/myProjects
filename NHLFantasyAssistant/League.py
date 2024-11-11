from espn_api.hockey import League
import Team

my_league_id = 1705592891
curr_year = 2025 
SWID = "73AF0A56-8B05-4B4C-8291-A431308556FD"
espn_s2_cookie = "AEAVePfqAj5sDj5KBoDdTQ7y7U5IcQaWswzMsomuzV%2B7u46Q29tOY56LRtFJucWWRyOD5FDujuOHqSG1LLa7NFXOJpW3jop3hgfmFglevS90tpTgw8tNRQLzznnrevnaIc5FZ8xE6b71AeemRUYSMnU1nT85QOi28kPbUd%2FN1WV45DPhzlbMb0YnUyXGba5HNLt17B7qiJWTIA0OlsPU50RsJ0meAG0YtMyP%2BUUvdg6GoddBkRS7tmy52bZ7kijTQW5eyARkXXTTfI5ymUCrbCDCgd%2BsIcolYdmjEbpIjg7KmA%3D%3D"

my_nhl_league = League(league_id=my_league_id, year=curr_year, espn_s2=espn_s2_cookie, swid=SWID, fetch_league=True)

curr_week = my_nhl_league.currentMatchupPeriod
# print(f"This is the current week: {curr_week}")
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
    for i in range(1, curr_week):
        printWeekMatchupResults(i)
            
# print("Full Season Matchup Scoreboard\n")
# printSeasonMatchupResults()
# print("\nWeek 3 Matchup Results\n")
# printWeekMatchupResults(3)

league_teams = my_nhl_league.teams
team_data = []
for i in range(1, len(league_teams) + 1):
        team_data.append(my_nhl_league.get_team_data(i))


def getSeasonPointsAgainst():
    points_against = {team.team_name: 0 for team in my_nhl_league.teams}  
    
    for i in range(1, my_nhl_league.current_week + 1):
        curr_matchups = my_nhl_league.box_scores(i)
        
        # Loop through the matchups and add points against for each team
        for matchup in curr_matchups:
            points_against[matchup.home_team.team_name] += matchup.away_score
            points_against[matchup.away_team.team_name] += matchup.home_score

    points_against = {team: round(score, 1) for team, score in points_against.items()}
    return points_against


def getSeasonPointsFor():
    points_for = {team.team_name: 0 for team in my_nhl_league.teams}

    for i in range(1, my_nhl_league.current_week + 1):
        curr_matchups = my_nhl_league.box_scores(i)

        for matchup in curr_matchups:
            points_for[matchup.home_team.team_name] += matchup.home_score
            points_for[matchup.away_team.team_name] += matchup.away_score

    points_for = {team: round(score, 1) for team, score in points_for.items()}
    return points_for

def getSeasonPointDifferential():
    diff = {team.team_name: 0 for team in my_nhl_league.teams}
    points_for = getSeasonPointsFor() 
    points_against = getSeasonPointsAgainst()

    for team in my_nhl_league.teams:
        diff[team.team_name] = round(points_for[team.team_name] - points_against[team.team_name], 1)
    return diff

# OG version got replaced and revamped

# def getSeasonPointsFor():
    
#     team_point_list = []
    
#     for team in team_data:
#         team_points = 0
#         # print(team.team_name)
#         # print(f"Div ID:  {team.division_id} Team ID:  {team.team_id}\n")
        
#         team_points += round(team.stats['BLK'] / 2, 1)
#         team_points += round(team.stats['W'] * 4)
#         team_points += round(team.stats['SV'] / 5, 1) 
#         team_points -= round(team.stats['GA'] * 2) 
#         team_points += round(team.stats['PPP'] / 2, 1)
#         team_points += round(team.stats['SO'] * 3)
#         team_points += round(team.stats['SHP'] / 2, 1)
#         team_points += round(team.stats['OTL'])
#         team_points += round(team.stats['G'] * 2)
#         team_points += round(team.stats['A'])
#         team_points += round(team.stats['SOG'] / 10, 1)
#         team_points += round(team.stats['HIT'] / 10, 1)
#         team_points = format("%.1f" % team_points)

#         team_dict_points = {team.team_name : team_points}
#         team_point_list.append(team_dict_points)
        
#     print(team_point_list)
#     return team_point_list
         

# displaySeasonPointsFor()
#     team_object_list.append(Team(team.team_name, team.roster, team_points, team.points_against, team.wins, team.losses))

def initializeTeamObjects(team_points_for, team_points_against, team_points_diff):
    team_object_dict = {}
    for team_info in my_nhl_league.teams:
        team = Team.Team(team_info.division_id, team_info.team_id, team_info.team_name, team_info.roster, team_points_for.get(team_info.team_name, 0), team_points_against.get(team_info.team_name, 0),team_points_diff.get(team_info.team_name, 0), team_info.wins, team_info.losses, team_info.stats)
        team_object_dict [team_info.team_name] = team

    return team_object_dict

def displayAllFreeAgents():
    FREE_AGENCY_SIZE = 1500 # Some extra padding since actual num is 1404 players
    available_players = my_nhl_league.free_agents(my_nhl_league.current_week, FREE_AGENCY_SIZE)
    print(f"FREE AGENTS\n"
          "----------------------------")
    for player in available_players:
        print(f"{player.name}({player.position}): {player.proTeam}")

def TeamDraftGrade():
     draftPicks = my_nhl_league.draft
     # do something with draftPicks to maybe store drafted players by team in dictionaries
     # then figure out grading score with remaining players
     print(draftPicks)

def LeagueStandings(team_object_list):
    standings = my_nhl_league.standings()
    print(f"League Standings\n"
          "------------------------------------")
    for i in range(len(standings)):
        team_object = team_object_list[standings[i].team_name]
        print(f"{i+1}. {team_object.displayTeamRecord()}\n"
              "------------------------------------")
        
# def TeamRecord(team_object_dict):
#     for team in my_nhl_league:
#         team_object_dict[team.team_name].displayTeamRecord()

def TeamRecord(team_object):
    team_object.displayTeamRecord()
        
def main():
    # printSeasonMatchupResults()
    # displayAllFreeAgents()
    seasonPointsFor = getSeasonPointsFor()
    seasonPointsAgainst = getSeasonPointsAgainst()
    seasonPointsDiff = getSeasonPointDifferential()
    team_object_dict = initializeTeamObjects(seasonPointsFor, seasonPointsAgainst, seasonPointsDiff)
    LeagueStandings(team_object_dict)

main()