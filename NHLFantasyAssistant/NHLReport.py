from MyLeague import MyLeague
league_object = MyLeague.createLeague()

def main():
    # league_object.printSeasonMatchupResults()
    # print()
    # league_object.LeagueStandings() 
    # print()
    # league_object.DivisionStandings(1)
    # print()
    # league_object.DivisionStandings(2)
    # print()
    # league_object.LeagueDraftResults()
    # print()
    # league_object.printAllBestTeamStat()
    # print()
    # league_object.printTeamRosters()  
    # print()
    # league_object.printTeamByPoints()
    # print()
    # league_object.printTeamByAvgPoints() 
    # print()
    # league_object.printDraftedTeam()
    # print()
    # league_object.printPlayersByAvgPoints()
    # print()
    # league_object.leagueDraftPowerRankings()
    # print()
    # league_object.leagueCurrPowerRankings()
    # print()
    
    league_object.streakReport(team="free_agents", min_threshold=1.4)
    print()
    league_object.streakReport(team="Dillon's Dubs")
    print()
    # league_object.streakReport(team="Shortcake Miniture Schnauzers", streak_type=["cool", "injured_or_minor_league"], min_threshold=1.4)
    
    
main()