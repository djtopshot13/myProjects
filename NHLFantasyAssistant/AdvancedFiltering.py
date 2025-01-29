import pandas as pd
lines_df = pd.read_csv("CSV/lines.csv")
teams_df = pd.read_csv("CSV/teams.csv")
lines_df.drop(columns=["lineId", "season"], inplace=True)

lines_df["TOI/G"] = round(lines_df["icetime"] / lines_df["games_played"], 2)
lines_df = lines_df.sort_values('TOI/G', ascending=False)
teams_df["GF/G"] = round(teams_df["xGoalsFor"] / teams_df["games_played"], 2)
teams_goals_for = teams_df.sort_values("GF/G", ascending=False)
teams_df = teams_df.sort_values('xGoalsPercentage', ascending=False)


def topIceTimeForwardLines():
    topIceTimeLines("line", 25)

def topIceTimeDefenseLines():
    topIceTimeLines("pairing", 25)

def topIceTimeLines(position, line_count):
    print(f"Top {line_count} {"Forwards" if position == "line" else "Defensemen"} with Most Ice Time\n\n")
    count = 0
    for index, row in lines_df.iterrows():
        if row['position'] == position:
            if count == line_count:
                print()
                break
            print(f"{count+1}. {row['team']} {row['name']} {row['TOI/G']} TOI/G \n")
            count += 1
        else: 
            continue
    
# topIceTimeForwardLines()
# topIceTimeDefenseLines()

def bestTeam5on5GoalsForPercentage():
    bestTeamGoalsForPercentage("5on5", 10)

def bestTeam5on4GoalsForPercentage():
    bestTeamGoalsForPercentage("5on4", 10)

def bestTeam4on5GoalsForPercentage():
    bestTeamGoalsForPercentage("4on5", 10)

def bestTeamOtherGoalsForPercentage():
    bestTeamGoalsForPercentage("other", 10)

def bestTeamAllGoalsForPercentage():
    bestTeamGoalsForPercentage("all", 10)

def bestTeamGoalsForPercentage(situation, team_count):
    # if situation != "other" and situation != "all":
    #     title = situation[0] + " " + situation[1:3].title() + " " + situation[3]
    # else:
    title = situation[0].upper() + situation[1:]
    print(f"Top {team_count} Scoring Teams in {title} Situations\n\n")
    count = 0
    for index, row in teams_df.iterrows():
        if row["situation"] == situation:
            if count == team_count:
                print()
                break
            print(f"{count+1}. {row["name"]} {row["xGoalsPercentage"]}%\n")
            count += 1
        else:
            continue

def bestTeam5on5GoalsForPerGame():
    bestTeamGoalsForPerGame("5on5", 10)

def bestTeam5on4GoalsForPerGame():
    bestTeamGoalsForPerGame("5on4", 10)

def bestTeam4on5GoalsForPerGame():
    bestTeamGoalsForPerGame("4on5", 10)

def bestTeamOtherGoalsForPerGame():
    bestTeamGoalsForPerGame("other", 10)

def bestTeamAllGoalsForPerGame():
    bestTeamGoalsForPerGame("all", 10)

def bestTeamGoalsForPerGame(situation, team_count):
    # if situation != "other" and situation != "all":
    #     title = situation[0] + " " + situation[1:3].title() + " " + situation[3]
    # else:
    title = situation[0].upper() + situation[1:]
    print(f"Top {team_count} Scoring Teams in {title} Situations\n\n")
    count = 0
    for index, row in teams_goals_for.iterrows():
        if row["situation"] == situation:
            if count == team_count:
                print()
                break
            print(f"{count+1}. {row["name"]} {row["GF/G"]} GF/G\n")
            count += 1
        else:
            continue

# bestTeam5on4GoalsForPercentage()
# bestTeam5on5GoalsForPercentage()
# bestTeam4on5GoalsForPercentage()
# bestTeamOtherGoalsForPercentage()
# bestTeamAllGoalsForPercentage()

bestTeam5on4GoalsForPerGame()
bestTeam5on5GoalsForPerGame()
bestTeam4on5GoalsForPerGame()
bestTeamOtherGoalsForPerGame()
bestTeamAllGoalsForPerGame()