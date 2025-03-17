import requests
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Utils.Constants import Constants

class ESPN:
    def __init__(self):
        self.constant_obj = Constants()
        self.base_url = "https://api-web.nhle.com/v1/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        self.nhl_teams, self.nhl_clubhouse_links, self.nhl_roster_links, self.nhl_stats_links, self.nhl_schedules_links = self.load_teams()
        # self.get_nhl_teams()
        self.get_nhl_team_rosters()
        self.get_nhl_team_standings()
        self.get_nhl_rem_schedule()
        self.get_nhl_schedule()
        # self.get_nhl_team_rosters()
        # self.get_nhl_team_standings()

    def get_nhl_teams(self):
        api_endpoint = self.base_url + "en/team"
        response = requests.get(api_endpoint, headers=self.headers)
        if response.status_code == 200:
            data = response.json
            with open("ESPNData/nhl_teams.json", "w") as f:
                json.dump(data, f, indent=4)



    def load_teams(self):
        url = "https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/teams"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for team_data in data["sports"][0]["leagues"][0]["teams"]:
                if team_data["team"]["name"] in self.constant_obj.intl_teams:
                    data["sports"][0]["leagues"][0]["teams"].remove(team_data)

            with open("ESPNData/nhl_teams.json", "w") as f:
                json.dump(data, f, indent=4)

            teams = data['sports'][0]["leagues"][0]["teams"]
            for team in teams:
                print(f"Team: {team["team"]['name']}, ID: {team["team"]['id']}")
        else:
            print(f"Error: Unable to fetch data. Status code: {response.status_code}")

        with open("ESPNData/nhl_teams.json", "r") as f:
            saved_data = json.load(f)

        teams = saved_data["sports"][0]["leagues"][0]["teams"]

        team_clubhouses, team_rosters, team_stats, team_schedules, teams_list = [], [], [], [], []
        for index in range(len(teams)):
            team = teams[index]["team"]
            teams_list.append(team['displayName'])
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

        return teams_list, team_clubhouses, team_rosters, team_stats, team_schedules

        

    # def process_roster_table(self, table, position):
    #     player_rows = table.find_all('tr', class_='Table__TR Table__TR--lg Table__even')
    #     roster_data = []
    #     for player_count in range(len(player_rows)):
    #         data_cells = table.find_all('td', class_="Table__TD")
            
    #         start_index = player_count * 8
    #         player_href = data_cells[start_index + 1].find('a')['href']
    #         player_id = player_href.split("/")[-1]
    #         name = data_cells[start_index + 1].text.strip()
    #         for i in range(len(name)-1, -1, -1):
    #             if not name[i].isdigit():
    #                 player_number = name[i+1:].strip()
    #                 player_name = name[:i+1].strip()
    #                 break
    #         player_age = data_cells[start_index + 2].text.strip()
    #         player_height = data_cells[start_index + 3].text.strip()
    #         player_weight = data_cells[start_index + 4].text.strip()
    #         player_shot = data_cells[start_index + 5].text.strip()
    #         player_birthplace = data_cells[start_index + 6].text.strip()
    #         player_birthdate = data_cells[start_index + 7].text.strip()
    #         player_position = position
            
    #         if len(data_cells) >= 8:
    #             player_info = {
    #                 "name": player_name,
    #                 "id": player_id,
    #                 "number": player_number,
    #                 "position": player_position,
    #                 "age": player_age,
    #                 "height": player_height,
    #                 "weight": player_weight,
    #                 "shot": player_shot,
    #                 "birthplace": player_birthplace,
    #                 "birthdate": player_birthdate,
    #                 "href": player_href
    #                 # "stats": self.get_nhl_player_stats(player_href)
    #         }
    #             roster_data.append(player_info)

        # # Add a delay of 5 seconds between requests
        # time.sleep(5)

        # return roster_data
    
    # def get_nhl_player_stats(self, player_link):
    #     response = requests.get(player_link, headers=self.headers, allow_redirects=True)
    #     response.raise_for_status()
    #     html_content = response.text
        
    #     player_soup = BeautifulSoup(html_content, 'html.parser')
    #     stats = player_soup

    
    # def get_nhl_team_rosters(self):
    #     all_rosters = {team: {} for team in self.nhl_teams} 

    #     for roster_url in self.nhl_roster_links:
    #         try:
    #             response = requests.get(roster_url, headers=self.headers, allow_redirects=True)
    #             response.raise_for_status()
    #             html_content = response.text
                
    #             soup = BeautifulSoup(html_content, 'html.parser')
    #             # print(soup)
                
    #             # Extract team name from the URL
    #             team_name = roster_url.split('/')[-1].replace('-', ' ').title()
    #             if team_name == "St Louis Blues":
    #                 team_name = "St. Louis Blues"

    #             all_rosters[team_name]["roster"] = []
                
    #             # Extract roster data using BeautifulSoup
    #             # This is a placeholder - you'll need to adjust based on the actual HTML structure
    #             center_table = soup.find("div", class_="ResponsiveTable Centers Roster__MixedTable")
    #             lw_table = soup.find("div", class_="ResponsiveTable Left Wings Roster__MixedTable")
    #             rw_table = soup.find("div", class_="ResponsiveTable Right Wings Roster__MixedTable")
    #             defense_table = soup.find("div", class_="ResponsiveTable Defense Roster__MixedTable")
    #             goalie_table = soup.find("div", class_="ResponsiveTable Goalies Roster__MixedTable")

    #             all_rosters[team_name]["roster"].extend(self.process_roster_table(center_table, "C"))
    #             all_rosters[team_name]["roster"].extend(self.process_roster_table(lw_table, "LW"))
    #             all_rosters[team_name]["roster"].extend(self.process_roster_table(rw_table, "RW"))
    #             all_rosters[team_name]["roster"].extend(self.process_roster_table(defense_table, "D"))
    #             all_rosters[team_name]["roster"].extend(self.process_roster_table(goalie_table, "G"))

    #             print(f"Successfully fetched roster for {team_name}")
                
                
                
    #         except requests.exceptions.RequestException as e:
    #             print(f"Error fetching {roster_url}: {e}")
    #             continue

    #     # Save all rosters to a single JSON file
    #     with open("ESPNData/nhl_team_rosters.json", "w") as f:
    #         json.dump(all_rosters, f, indent=4)

    #     print("All rosters saved to nhl_team_rosters.json")

    # def get_nhl_team_standings(self):
    #     # all_stats = {nhl_team: {"stats": []} for nhl_team in self.nhl_teams}
    #     standings_url = "https://www.espn.com/nhl/standings"
    #     try:
    #         response = requests.get(standings_url, headers=self.headers, allow_redirects=True)
    #         response.raise_for_status()
    #         html_content = response.text
        
    #         standings_soup = BeautifulSoup(html_content, 'html.parser')
    #         all_standings = {}

    #         atl_conf, atl_name, atl_div = self.get_nhl_division_standings(standings_soup, "Eastern Conference", div_id=0)
    #         all_standings.update({atl_conf: {atl_name: atl_div}})
    #         met_conf, met_name, met_div = self.get_nhl_division_standings(standings_soup, "Eastern Conference", div_id=1)
    #         all_standings.update({met_conf: {met_name: met_div}})

    #         cen_conf, cen_name, cen_div = self.get_nhl_division_standings(standings_soup, "Western Conference", div_id=2)
    #         all_standings.update({cen_conf: {cen_name: cen_div}})
    #         pac_conf, pac_name, pac_div = self.get_nhl_division_standings(standings_soup, "Western Conference", div_id=3)
    #         all_standings.update({pac_conf: {pac_name: pac_div}})

    #         with open("ESPNData/nhl_team_standings.json", "w") as f:
    #             json.dump(all_standings, f, indent=4)

    #         print("All standings saved to nhl_team_standings.json")
    #     except requests.exceptions.RequestException as e:
    #         print(f"Error fetching {standings_url}: {e}")

    # def get_nhl_division_standings(self, standings_soup, conf_string, div_id):
    #     conf_teams = standings_soup.find("div", class_ = "ResponsiveTable")[div_id]
    #     print(conf_teams)
    #     teams = conf_teams[0].find_all("tr")
    #     print(teams)
    #     conf_abbrev = conf_string.replace("ern Conference", "")
    #     div_name = teams[0].text.strip()

    #     size_range = (0, len(teams) // 2) if div_id == 0 else (len(teams) // 2, len(teams))
    #     for index in range(size_range[0], size_range[1]):
    #         div_count = 17 * index
            
    #         if div_count > 0:
    #             team_name = teams[div_count].text.strip()
    #             games_played = teams[div_count + 1].text.strip()
    #             wins = teams[div_count + 2].text.strip()
    #             losses = teams[div_count + 3].text.strip()
    #             ot_losses = teams[div_count + 4].text.strip()
    #             points = teams[div_count + 5].text.strip()
    #             reg_wins = teams[div_count + 6].text.strip()
    #             reg_ot_wins = teams[div_count + 7].text.strip()
    #             so_wins = teams[div_count + 8].text.strip()
    #             so_losses = teams[div_count + 9].text.strip()
    #             home_record = teams[div_count + 10].text.strip()
    #             away_record = teams[div_count + 11].text.strip()
    #             goals_for = teams[div_count + 12].text.strip()
    #             goals_against = teams[div_count + 13].text.strip()
    #             goal_diff = teams[div_count + 14].text.strip()
    #             last_10_games_played = teams[div_count + 15].text.strip()
    #             streak = teams[div_count + 16].text.strip()
                

    #         team_info = {
    #             team_name: 
    #             {
    #             "CONF": conf_abbrev,
    #             "DIV": div_name,
    #             "GP": games_played,
    #             "W": wins,
    #             "L": losses,
    #             "OTL": ot_losses,
    #             "P": points,
    #             "P%": points / (2 * games_played),
    #             "RW": reg_wins,
    #             "ROW": reg_ot_wins,
    #             "SOW": so_wins,
    #             "SOL": so_losses,
    #             "HOME": home_record,
    #             "AWAY": away_record,
    #             "GF": goals_for,
    #             "GA": goals_against,
    #             "DIFF": goal_diff,
    #             "L10": last_10_games_played,
    #             "STRK": streak,
    #             }
    #         }


    #     return conf_abbrev, div_name, team_info

    def get_nhl_team_standings(self):
        api_endpoint = self.base_url + "standings/now"
        response = requests.get(api_endpoint, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            self.populate_team_standings(data)

        
    def populate_team_standings(self, standings_data):
        # min_ga_pct = ("", float('inf'))
        
        for standing in standings_data["standings"]:
            del standing["l10Ties"], standing["roadTies"], standing['homeTies'], standing['ties']

            standing["OtLosses"] = standing["otLosses"]
            standing['goalsAgainst'] = standing['goalAgainst']
            standing['goalsFor'] = standing['goalFor']
            del standing["otLosses"], standing['goalAgainst'], standing['goalFor']
            standing["OtWins"] = standing["regulationPlusOtWins"] - standing["regulationWins"]
            standing["OtWinPctg"] = standing["OtWins"] / (standing["OtWins"] + standing["OtLosses"])
            standing["shootoutWinPctg"] = standing["shootoutWins"] / (standing["shootoutWins"] + standing["shootoutLosses"]) if standing["shootoutWins"] != 0 and standing["shootoutLosses"] != 0 else 0
            standing["roadPointPctg"] = standing['roadPoints'] / (standing['roadGamesPlayed'] * 2)
            standing["homePointPctg"] = standing["homePoints"] / (standing['homeGamesPlayed'] * 2)
            standing['goalsAgainstPctg'] = standing['goalsAgainst'] / standing['gamesPlayed']

        #   if standing["goalsAgainstPctg"] < min_ga_pct[1]:
        #         min_ga_pct = (standing["teamName"]["default"], standing["goalsAgainstPctg"])
        # print(min_ga_pct)

        with open("ESPNData/nhl_team_standings.json", "w") as f:
            json.dump(standings_data, f, indent=4)
        
    def get_nhl_team_rosters(self):
        data = {"nhlRosters": []}
        for name, abbrev in self.constant_obj.pro_team_abbrev.items():
            api_endpoint = self.base_url + f"roster/{abbrev}/current"
            response = requests.get(api_endpoint, headers=self.headers)
            if response.status_code == 200:
                data['nhlRosters'].append({name: response.json()})
                with open("ESPNData/nhl_team_rosters.json", "w") as f:
                    json.dump(data, f, indent=4)

    def get_nhl_rem_schedule(self):
        data = {"nhlSchedules": []}
        for name, abbrev in self.constant_obj.pro_team_abbrev.items():
            api_endpoint = self.base_url + f"club-schedule-season/{abbrev}/now"
            response = requests.get(api_endpoint, headers=self.headers)
            if response.status_code == 200:
                data['nhlSchedules'].append({name: response.json()})
                with open("ESPNData/nhl_team_schedules.json", "w") as f:
                    json.dump(data, f, indent=4)
                    
    def get_nhl_schedule(self):
        data = {"nhlSchedules": {}}
        api_endpoint = self.base_url + "schedule/now"
        response = requests.get(api_endpoint, headers=self.headers)
        if response.status_code == 200:
            data['nhlSchedules'] = response.json()
            with open("ESPNData/nhl_full_team_schedules.json", "w") as f:
                json.dump(data, f, indent=4)

ESPN_data = ESPN()