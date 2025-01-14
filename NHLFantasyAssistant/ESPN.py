import requests
import json
import time
from bs4 import BeautifulSoup

url = "https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/teams"
response = requests.get(url)
if response.status_code == 200:
    data = response.json()

    with open("nhl_teams.json", "w") as f:
        json.dump(data, f, indent=4)

    teams = data['sports'][0]["leagues"][0]["teams"]
    for team in teams:
        print(f"Team: {team["team"]['name']}, ID: {team["team"]['id']}")
else:
    print(f"Error: Unable to fetch data. Status code: {response.status_code}")

with open("nhl_teams.json", "r") as f:
    saved_data = json.load(f)

teams = saved_data["sports"][0]["leagues"][0]["teams"]

team_clubhouses, team_rosters, team_stats, team_schedules = [], [], [], []
for index in range(len(teams)):
    team = teams[index]["team"]
    team_abbrev = team["abbreviation"].lower()
    slug = team["slug"]
    links = {
        team_abbrev:
    {
        "clubhouse": f"https://www.espn.com/nhl/team/_/name/{team_abbrev}/{slug}",
        "roster": f"https://www.espn.com/nhl/team/roster/_/name/{team_abbrev}/{slug}",
        "stats": f"https://www.espn.com/nhl/team/stats/_/name/{team_abbrev}/{slug}",
        "schedule": f"https://www.espn.com/nhl/team/schedule/_/name/{team_abbrev}/{slug}"
    }
}
    team_clubhouses.append(links[team_abbrev]["clubhouse"])
    team_rosters.append(links[team_abbrev]["roster"])
    team_stats.append(links[team_abbrev]["stats"])
    team_schedules.append(links[team_abbrev]["schedule"])

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
# }

all_rosters = {}

for roster_url in team_rosters:
    try:
        response = requests.get(roster_url)
        response.raise_for_status()
        html_content = response.text
        
        soup = BeautifulSoup(html_content, 'html.parser')
        # print(soup)
        
        # Extract team name from the URL
        team_name = roster_url.split('/')[-1].replace('-', ' ').title()
        
        # Extract roster data using BeautifulSoup
        # This is a placeholder - you'll need to adjust based on the actual HTML structure
        players = soup.find_all('tr', class_='Table__TR Table__TR--lg Table__even')
        roster_data = [player.text for player in players]
        
        all_rosters[team_name] = roster_data
        
        print(f"Successfully fetched roster for {team_name}")
        
        # Add a delay of 10 seconds between requests
        time.sleep(5)
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {roster_url}: {e}")
        continue

# Save all rosters to a single JSON file
with open("nhl_team_rosters.json", "w") as f:
    json.dump(all_rosters, f, indent=4)

print("All rosters saved to nhl_team_rosters.json")