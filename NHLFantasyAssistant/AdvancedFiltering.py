import pandas as pd
lines_df = pd.read_csv("lines.csv")
teams_df = pd.read_csv("teams.csv")
lines_df.drop(columns=["lineId", "season"], inplace=True)

lines_df["TOI/G"] = round(lines_df["icetime"] / lines_df["games_played"], 2)
lines_df = lines_df.sort_values('TOI/G', ascending=False)

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
    
topIceTimeForwardLines()
topIceTimeDefenseLines()

# for col in lines_df.columns:
#     print(col)