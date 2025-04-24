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

# r = requests.get(f"https://api.nhle.com/stats/rest/en/team/summary?sort=teamFullName&cayenneExp=seasonId=20242025%20and%20gameTypeId=2")
# team_stats = r.json()

# df = pd.json_normalize(team_stats["data"])
# df = df.drop(columns=["ties"])


# cols = df.columns.to_list()
# cols[0], cols[18] = cols[18], cols[0]
# df = df[cols]
# df.to_csv("NHLTeamsBasicStats.csv", index=False)
# headers = {
#     'User-Agent': 'my-app/1.0',
#     'Accept': 'text/csv',
# }
# for i in range(1, 1313):
#     game_id = f"{i:04}"
#     url = f"https://moneypuck.com/moneypuck/gameData/20242025/202402{game_id}.csv"
#     response = requests.get(url, headers=headers)
#     if response.status_code != 200:
#         print(f"Failed to retrieve data for game ID: 202402{game_id}, Status Code: {response.status_code}")
#         continue
#     game_data = response.json()
#     game_df = pd.json_normalize(game_data)
#     game_df.to_csv(f"PBP/202402{game_id}.csv", index=False)
#     print(f"Game 202402{game_id} data saved.")

"""
Games 
October: 0001-0167 
November: 0168-0387
December: 0388-601
January: 602-825
February: 826-947
March: 948-1181
April: 1182-1312
"""


def download_csv_files(BASE_URL, DOWNLOAD_DIR):
    import os
    from bs4 import BeautifulSoup  # For parsing HTML

    # Configuration
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "text/csv"  # Prioritize CSV responses
    }

    # Ensure download directory exists
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    # Step 1: Get page content
    response = requests.get(BASE_URL, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to retrieve the page, status code: {response.status_code}")
        exit()
    soup = BeautifulSoup(response.text, "html.parser")
    if soup is None:
        print("Failed to retrieve the page content.")
        exit()


    # Step 2: Find CSV links
    csv_links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and ("download" in href.lower() or href.endswith(".csv")):
            csv_links.append(href)

    # Step 3: Download files
    for link in csv_links:
        # Handle relative URLs
        if not link.startswith("http"):
            link = f"{BASE_URL}/{link.lstrip('/')}"
        
        try:
            response = requests.get(link, headers=HEADERS)
            response.raise_for_status()  # Check for HTTP errors
            
            # Generate filename from URL
            filename = os.path.join(
                DOWNLOAD_DIR,
                os.path.basename(link).split("?")[0]  # Remove URL parameters
            )
            
            # Save file
            with open(filename, "wb") as f:
                f.write(response.content)
            
            print(f"Downloaded: {filename}")
        
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {link}: {e}")

def json_files_to_csv(BASE_URL, DOWNLOAD_DIR):
    import os
    import json
    import datetime

    # Configuration
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json"  # Prioritize JSON responses
    }

    # Ensure download directory exists
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    # Step 1: Get page content
    response = requests.get(BASE_URL, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to retrieve the page, status code: {response.status_code}")
        exit()

    # Step 2: Parse JSON data
    try:
        json_data = response.json()
    except json.JSONDecodeError:
        print("Failed to decode JSON data.")
        exit()

    # Step 3: Save JSON data to file
    # filename = os.path.join(DOWNLOAD_DIR, "data.json")
    # with open(filename, "w") as f:
    #     json.dump(json_data, f, indent=4)

    # print(f"Downloaded JSON data to {filename}")

    schedule_df = pd.json_normalize(json_data)
    schedule_df = schedule_df.sort_values(by=["id"])
    schedule_df.rename(columns={"h": "homeAbbrev", "a": "awayAbbrev"}, inplace=True)
    schedule_df['est'] = pd.to_datetime(schedule_df['est'], format='%Y%m%d').dt.strftime('%Y %B %d')
    schedule_df = schedule_df[["id", "homeAbbrev", "awayAbbrev", "est"]]
    schedule_df.to_csv(os.path.join(DOWNLOAD_DIR, f"{season}.csv"), index=False)

season = "20072008"
BASE_URL =f"https://www.moneypuck.com/moneypuck/OldSeasonScheduleJson/{season}PL02.json"
DOWNLOAD_DIR = "NHLSeasonSchedule"
json_files_to_csv(BASE_URL, DOWNLOAD_DIR)