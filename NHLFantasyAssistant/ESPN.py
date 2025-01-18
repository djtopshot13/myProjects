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

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def processRosterTable(table, position):
    player_rows = table.find_all('tr', class_='Table__TR Table__TR--lg Table__even')
    roster_data = []
    for player_count in range(len(player_rows)):
        data_cells = table.find_all('td', class_="Table__TD")
        
        start_index = player_count * 8
        player_href = data_cells[start_index + 1].find('a')['href']
        player_id = player_href.split("/")[-1]
        name = data_cells[start_index + 1].text.strip()
        for i in range(len(name)-1, -1, -1):
            if not name[i].isdigit():
                player_number = name[i+1:].strip()
                player_name = name[:i+1].strip()
                break
        player_age = data_cells[start_index + 2].text.strip()
        player_height = data_cells[start_index + 3].text.strip()
        player_weight = data_cells[start_index + 4].text.strip()
        player_shot = data_cells[start_index + 5].text.strip()
        player_birthplace = data_cells[start_index + 6].text.strip()
        player_birthdate = data_cells[start_index + 7].text.strip()
        player_position = position
        
        if len(data_cells) >= 8:
            player_info = {
                "name": player_name,
                "id": player_id,
                "number": player_number,
                "position": player_position,
                "age": player_age,
                "height": player_height,
                "weight": player_weight,
                "shot": player_shot,
                "birthplace": player_birthplace,
                "birthdate": player_birthdate,
                "href": player_href
        }
            roster_data.append(player_info)

    # # Add a delay of 5 seconds between requests
    # time.sleep(5)

    return roster_data

all_rosters = {}

for roster_url in team_rosters:
    try:
        response = requests.get(roster_url, headers=headers, allow_redirects=True)
        response.raise_for_status()
        html_content = response.text
        
        soup = BeautifulSoup(html_content, 'html.parser')
        # print(soup)
        
        # Extract team name from the URL
        team_name = roster_url.split('/')[-1].replace('-', ' ').title()
        stats_url = roster_url.replace("roster", "stats")
        all_rosters[team_name]["roster"] = []
        
        # Extract roster data using BeautifulSoup
        # This is a placeholder - you'll need to adjust based on the actual HTML structure
        center_table = soup.find("div", class_="ResponsiveTable Centers Roster__MixedTable")
        lw_table = soup.find("div", class_="ResponsiveTable Left Wings Roster__MixedTable")
        rw_table = soup.find("div", class_="ResponsiveTable Right Wings Roster__MixedTable")
        defense_table = soup.find("div", class_="ResponsiveTable Defense Roster__MixedTable")
        goalie_table = soup.find("div", class_="ResponsiveTable Goalies Roster__MixedTable")

        all_rosters[team_name]["roster"].extend(processRosterTable(center_table, "C"))
        all_rosters[team_name]["roster"].extend(processRosterTable(lw_table, "LW"))
        all_rosters[team_name]["roster"].extend(processRosterTable(rw_table, "RW"))
        all_rosters[team_name]["roster"].extend(processRosterTable(defense_table, "D"))
        all_rosters[team_name]["roster"].extend(processRosterTable(goalie_table, "G"))

        print(f"Successfully fetched roster for {team_name}")
        
        
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {roster_url}: {e}")
        continue

# Save all rosters to a single JSON file
with open("nhl_team_rosters.json", "w") as f:
    json.dump(all_rosters, f, indent=4)

print("All rosters saved to nhl_team_rosters.json")

