import os
import sys
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import requests
import pandas as pd
from Utils.DataScrub import DataScrub
from io import StringIO

class AdvancedStats:
    def __init__(self):
        self.url_base = "https://moneypuck.com/moneypuck/playerData/seasonSummary/2024/regular/"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        self.teams_df = self.dataFrameGenerator("teams.csv")
        self.lines_df = self.dataFrameGenerator("lines.csv")
        self.skaters_df = self.dataFrameGenerator("skaters.csv")
        self.goalies_df = self.dataFrameGenerator("goalies.csv")
        self.lines_df = DataScrub.clean_data(self.lines_df)
        self.best_teams_goals_for = self.teams_df.sort_values("goalsFor", ascending=False)
        self.worst_teams_goals_for = reversed(self.best_teams_goals_for)
        self.best_teams_exp_goals_for = self.teams_df.sort_values("xGoalsFor", ascending=False)
        self.worst_teams_exp_goals_for = reversed(self.best_teams_exp_goals_for)
        self.most_ice_time_lines = self.lines_df.sort_values('iceTimeRank', ascending=False)
        self.worst_ice_time_lines = reversed(self.most_ice_time_lines)
        self.best_teams_exp_goals_percentage = self.teams_df.sort_values("xGoalsPercentage", ascending=False)
        self.worst_teams_exp_goals_percentage = reversed(self.best_teams_exp_goals_percentage)
        self.writeToCSV()
        self.main()

    def _daily_write(self, filepath):
        if not os.path.exists(filepath):
            return True
        mod_time = os.path.getmtime(filepath)
        mod_date = time.localtime(mod_time)
        curr_time = time.localtime()

        return (mod_date.tm_year, mod_date.tm_mon, mod_date.tm_mday) != \
            (curr_time.tm_year, curr_time.tm_mon, curr_time.tm_mday)

    def writeToCSV(self):
        """Write CSVs only if they don't exist or weren't modified today"""
        csv_dir = "CSV"
        os.makedirs(csv_dir, exist_ok=True)
        files = [
            ("nhl_teams_data.csv", self.teams_df),
            ("nhl_lines_data.csv", self.lines_df), 
            ("nhl_skaters_data.csv", self.skaters_df),
            ("nhl_goalies_data.csv", self.goalies_df)
            ]
        for filename, df in files:
            filepath = os.path.join(csv_dir, filename)
            if self._daily_write(filepath):
                df.to_csv(filepath, index=False)
                print(f"Modified {filename}")
            else:
                print(f"Skipped {filename} (already modified today)")
            

    def dataFrameGenerator(self, suffix):
        full_url = self.url_base + suffix
        response = requests.get(full_url, headers=self.headers)
        if response.status_code == 200:
            csv_content = StringIO(response.text)
            df = pd.read_csv(csv_content)
            return df
        else: 
            print(f"Failed to retrieve data from {suffix} file. Status code: {response.status_code}")
    
    def statsPerGameConverter(self, df, stat_name):
        df[stat_name + "/Game"] = round(df[stat_name] / df["games_played"], 2)
        df = df.sort_values(stat_name + "/Game", ascending=False)
        return df

    def main(self):
        # self.lines_df["icetime/Game"] = round(self.lines_df["icetime"] / self.lines_df["games_played"], 2)
        # self.lines_df = self.lines_df.sort_values('icetime/G', ascending=False)
        # self.teams_df = self.teams_df.sort_values('xGoalsPercentage', ascending=False)
        self.lines_df.drop(columns=["lineId", "season"], inplace=True)


        self.topIceTimeForwardLines()
        self.topIceTimeDefenseLines()

        self.bestTeamAllExpGoalsForPercentage()
        self.bestTeam5on4ExpGoalsForPercentage()
        self.bestTeam5on5ExpGoalsForPercentage()
        self.bestTeam4on5ExpGoalsForPercentage()
        self.bestTeamOtherExpGoalsForPercentage()
        
        self.bestTeamAllExpGoalsFor()
        self.bestTeam5on4ExpGoalsFor()
        self.bestTeam5on5ExpGoalsFor()
        self.bestTeam4on5ExpGoalsFor()
        self.bestTeamOtherExpGoalsFor()

        self.mostGoalsFor()
        self.most5on4GoalsFor()
        self.most5on5GoalsFor()
        self.most4on5GoalsFor()
        self.mostOtherGoalsFor()


    def topIceTimeForwardLines(self):
        self.topIceTimeLines("line", 25)

    def topIceTimeDefenseLines(self):
        self.topIceTimeLines("pairing", 25)

    def topIceTimeLines(self, position, line_count):
        print(f"Top {line_count} {"Forwards" if position == "line" else "Defensemen"} with Most Ice Time\n\n")
        count = 0
        rank = 0
        last_stat = float('inf')
        for index, row in self.most_ice_time_lines.iterrows():
            if row['position'] == position:
                if count == line_count:
                    print()
                    break
                if row['iceTimeRank'] != last_stat:
                    rank = count + 1
                print(f"{rank}. {row['team']} {row['name']} {row['iceTimeRank']} iceTimeRank \n")
                last_stat = row['iceTimeRank']
                count += 1
            else: 
                continue

    def bestTeam5on5ExpGoalsForPercentage(self):
        self.bestTeamsOrdering("5on5", 10, "xGoalsPercentage")

    def bestTeam5on4ExpGoalsForPercentage(self):
        self.bestTeamsOrdering("5on4", 10, "xGoalsPercentage")

    def bestTeam4on5ExpGoalsForPercentage(self):
        self.bestTeamsOrdering("4on5", 10, "xGoalsPercentage")

    def bestTeamOtherExpGoalsForPercentage(self):
        self.bestTeamsOrdering("other", 10, "xGoalsPercentage")

    def bestTeamAllExpGoalsForPercentage(self):
        self.bestTeamsOrdering("all", 10, "xGoalsPercentage")

    # def bestTeamGoalsForPercentage(self, situation, team_count):
    #     # if situation != "other" and situation != "all":
    #     #     title = situation[0] + " " + situation[1:3].title() + " " + situation[3]
    #     # else:
    #     title = situation[0].upper() + situation[1:]
    #     print(f"Top {team_count} Scoring Teams in {title} Situations\n\n")
    #     count = 0
    #     for index, row in self.best_teams_goals_percentage.iterrows():
    #         if row["situation"] == situation:
    #             if count == team_count:
    #                 print()
    #                 break
    #             print(f"{count+1}. {row["name"]} {row["xGoalsPercentage"]}%\n")
    #             count += 1
    #         else:
                # continue

    def bestTeam5on5ExpGoalsFor(self):
        self.bestTeamsOrdering("5on5", 10, "xGoalsFor")

    def bestTeam5on4ExpGoalsFor(self):
        self.bestTeamsOrdering("5on4", 10, "xGoalsFor")

    def bestTeam4on5ExpGoalsFor(self):
        self.bestTeamsOrdering("4on5", 10, "xGoalsFor")

    def bestTeamOtherExpGoalsFor(self):
        self.bestTeamsOrdering("other", 10, "xGoalsFor")

    def bestTeamAllExpGoalsFor(self):
        self.bestTeamsOrdering("all", 10, "xGoalsFor")

    def mostGoalsFor(self):
        self.bestTeamsOrdering("all", 10, "goalsFor")

    def most5on4GoalsFor(self):
        self.bestTeamsOrdering("5on4", 10, "goalsFor")

    def most5on5GoalsFor(self):
        self.bestTeamsOrdering("5on5", 10, "goalsFor")

    def most4on5GoalsFor(self):
        self.bestTeamsOrdering("4on5", 10, "goalsFor")

    def mostOtherGoalsFor(self):
        self.bestTeamsOrdering("other", 10, "goalsFor")


    def bestTeamsOrdering(self, situation, team_count, stat_name):
        data_frame = self.teams_df.sort_values(stat_name, ascending=False)
        title = situation[0].upper() + situation[1:]
        print(f"Top {team_count} Teams {stat_name} in {title} Situations\n\n")
        count = 0
        rank = 0
        last_stat = float('inf')
        for index, row in data_frame.iterrows():
            if row["situation"] == situation:
                if count == team_count:
                    print()
                    break
                if row[stat_name] != last_stat:
                    rank = count + 1
                print(f"{rank}. {row["name"]} {row[stat_name]} {stat_name}\n")
                last_stat = row[stat_name]
                count += 1
            else:
                continue

AdvancedStats()