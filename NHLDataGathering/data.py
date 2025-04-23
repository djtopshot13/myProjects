# Initial Data Gathering Testing with NHL API using POSTMAN and NHL.com endpoints

import requests
import pandas as pd

# r = requests.get("https://api.nhle.com/stats/rest/en/franchise?sort=fullName&include=lastSeason.id&include=firstSeason.id")
# team_data = r.json()

# df = pd.json_normalize(team_data['data'])
# df = df[df["lastSeason.id"].isnull()]
# df = df.drop(columns=["lastSeason", "lastSeason.id"])
# df = df.rename(columns={"teamCommonName": "TeamName", "teamPlaceName": "City", "firstSeason.id": "FirstSeasonID", "id": "ID", "fullName": "FullName"})
# cols = df.columns.to_list()
# cols[2], cols[3] = cols[3], cols[2]
# df = df[cols]

r = requests.get(f"https://api.nhle.com/stats/rest/en/team/summary?sort=teamFullName&cayenneExp=seasonId=20242025%20and%20gameTypeId=2")
team_stats = r.json()

df = pd.json_normalize(team_stats["data"])
df = df.drop(columns=["ties"])


cols = df.columns.to_list()
cols[0], cols[18] = cols[18], cols[0]
df = df[cols]
df.to_csv("NHLTeamsBasicStats.csv", index=False)

