from datetime import date

class Constants:
    def __init__(self):
        self.intl_teams = [
            "Canada",
            "USA",
            "Finland",
            "Sweden"
        ]
        self.team_abbrev = {
            "Luuky Pooky": "LUUK",
            "Dallin's Daring Team": "DDT",
            "Shortcake Miniture Schnauzers": "SMS",
            "Live Laff Love": "GKG", 
            "Hockey": "CCT", 
            "Kings Shmings": "JEF", 
            "Dillon's Dubs": "DD", 
            "Mind Goblinz": "GBL"
        }
        self.pro_team_abbrev = {
            "Anaheim Ducks": "ANA",
            "Boston Bruins": "BOS", 
            "Buffalo Sabres": "BUF",
            "Calgary Flames": "CGY",
            "Carolina Hurricanes": "CAR",
            "Chicago Blackhawks": "CHI", 
            "Colorado Avalanche": "COL",
            "Columbus Blue Jackets": "CLS",
            "Dallas Stars": "DAL",
            "Detroit Red Wings": "DET",
            "Edmonton Oilers": "EDM",
            "Florida Panthers": "FLA",
            "Los Angeles Kings": "LAK",
            "Minnesota Wild": "MIN",
            "Montr\u00e9al Canadiens": "MTL",
            "Nashville Predators": "NSH",
            "New Jersey Devils": "NJD",
            "New York Islanders": "NYI",
            "New York Rangers": "NYR", 
            "Ottawa Senators": "OTT",
            "Philadelphia Flyers": "PHI",
            "Pittsburgh Penguins": "PIT",
            "San Jose Sharks": "SJS",
            "Seattle Kraken": "SEA",
            "St. Louis Blues": "STL",
            "Tampa Bay Lightning": "TBL",
            "Toronto Maple Leafs": "TOR",
            "Utah Hockey Club": "UTA",
            "Vancouver Canucks": "VAN", 
            "Vegas Golden Knights": "VGK", 
            "Washington Capitals": "WSH", 
            "Winnipeg Jets": "WPG",
            "Unknown Team": "???"
        }

        self.curr_year = date.today().year
        self.curr_month = date.today().month
        self.curr_day = date.today().day
        self.__feb_days = 29 if self.curr_year % 4 == 0 else 28

        self.numToMonth = {
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May", 
            6: "June",
            7: "July", 
            8: "August", 
            9: "September",
            10: "October",
            11: "November",
            12: "December"
        }
        

        self.monthToNumOfDays = {
            "January": 31,
            "February": self.__feb_days,
            "March": 31,
            "April": 30,
            "May": 31, 
            "June": 30,
            "July": 31, 
            "August": 31, 
            "September": 30,
            "October": 31,
            "November": 30,
            "December": 31
        }


        self.pro_team_abbrev_keys = list(self.pro_team_abbrev.keys())
        self.pro_team_abbrev_vals = list(self.pro_team_abbrev.values())
        for i in range(len(self.pro_team_abbrev)):
            self.pro_team_abbrev.update({self.pro_team_abbrev_vals[i]: self.pro_team_abbrev_keys[i]}) # have dict be reversible

        self.code_filter = ["all", "hot", "consistent", "cold", "warm", "cool", "heating_up", "cooling_down", "injured_or_minor_league"]
        self.position_keys = ["all", "skater", "forward", "defenseman", "goalie"]

    def date_to_string(self, year, month, day):
        return str(year).join("-").join(str(month)).join("-").join(str(day))