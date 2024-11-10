from espn_api.hockey import League
import Team

my_league_id = 1705592891
curr_year = 2025 
SWID = "73AF0A56-8B05-4B4C-8291-A431308556FD"
espn_s2_cookie = "AEAVePfqAj5sDj5KBoDdTQ7y7U5IcQaWswzMsomuzV%2B7u46Q29tOY56LRtFJucWWRyOD5FDujuOHqSG1LLa7NFXOJpW3jop3hgfmFglevS90tpTgw8tNRQLzznnrevnaIc5FZ8xE6b71AeemRUYSMnU1nT85QOi28kPbUd%2FN1WV45DPhzlbMb0YnUyXGba5HNLt17B7qiJWTIA0OlsPU50RsJ0meAG0YtMyP%2BUUvdg6GoddBkRS7tmy52bZ7kijTQW5eyARkXXTTfI5ymUCrbCDCgd%2BsIcolYdmjEbpIjg7KmA%3D%3D"

my_nhl_league = League(league_id=my_league_id, year=curr_year, espn_s2=espn_s2_cookie, swid=SWID, fetch_league=True)

curr_week = my_nhl_league.current_week - 32
# print(f"This is the current week: {curr_week}")
def printSeasonMatchupResults():
    for i in range(1, curr_week):
        print(f"Week {i} Winners: ")
        curr_matchups = my_nhl_league.box_scores(i)
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
    # league_teams = my_nhl_league.teams
# team_data = []
# team_object_list = []
# for i in range(1, len(league_teams) + 1):
#     team_data.append(my_nhl_league.get_team_data(i))
# for team in team_data:
#     team_object_list.append(Team(team.team_name, team.roster, team.points_for, team.points_against, team.wins, team.losses))
# print(team_object_list)

# print(dir(my_nhl_league))
printSeasonMatchupResults()
# available_players = my_nhl_league.free_agents(curr_week, 100)
# for player in available_players:
#     print(f"{player.name}({player.position}): {player.proTeam}")