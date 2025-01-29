# **Design Documentation**
Pasted most of this over from the previously existing Fantasy Ideas.txt file. Hoping to move forward with more software dev techniques.

Organizational Structure:
    LeagueObject():
        TeamObjects():
        League variables
            PlayerObjects():
            Team variables
                Player variables


League Function Ideas:

DisplaySorted\[Stat\]Teams(boolean dec_order, String stat_name):
    Parameters:
        [boolean dec_order or !dec_order] -> (default = dec_order, ie highest at top, lowest at bottom)
        [String stat_name] -> (grab stat from Team object directory instance variable)
    Body:
        Sort based on dec_order value and assign stat_value -> Team directory at index stat_name
    Return:
        Print teams with team_name, stat_name, and stat_value based on dec_order 

LeaguePowerRankingBoard()
    Parameters: 

**** I need to create a constant file with constants like proTeam abbreviations for representing player objects (skater/goalie) and other functions too
**** Create a filter method that sorts team rosters based on player data possibly. Like health status or avg_points or by position or pro_team