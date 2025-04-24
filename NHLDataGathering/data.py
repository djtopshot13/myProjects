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
