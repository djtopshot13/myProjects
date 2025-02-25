- [**NHLFantasyAssistant Software Documentation**](#nhlfantasyassistant-software-documentation)
  - [**Purpose and Objectives**](#purpose-and-objectives)
  - [**Navigating the Repo**](#navigating-the-repo)
    - [**CSV**](#csv)
    - [**Documentation**](#documentation)
    - [**ESPNData**](#espndata)
    - [**MainObjects**](#mainobjects)
    - [**ToolObjects**](#toolobjects)
    - [**Utils**](#utils)
    - [**NHLReport.py**](#nhlreportpy)
>
# **NHLFantasyAssistant Software Documentation**
## **Purpose and Objectives**
- My main objective is to try and create a program that optimizes user performance within ESPN Fantasy NHL. 
- I have a rough draft project functioning that generates reports that the user can read to help their decision making.
- My end goal would be to use an LLM to parse these reports and generate possible decisions filtering from best to worst. 
- The LLM would help offer suggestions for making decisions with adding, dropping, trading, starting, and benching their players.
- I would love to make this into an app that displays the same ESPN Fantasy App with additional prompts and tools surrounding the normal app or an extension of some sort if that is not feasible.

## **Navigating the Repo** 
### **CSV**
- Within this folder are CSV files from MoneyPuck.com for this season. 
- The folders include data for each NHL team, line/pairing, skater, and goalie
- There is a data dictionary documentation file written by MoneyPuck included to assist with understanding the different CSV fields. 
- These files are being accessed by the AdvancedFiltering.py file within the Tool_Objects directory.
- The newest focus of the program is based on implementing code using this data.
### **Documentation**
- This is where all software documentation will be kept. 
- Currently includes Markdown files for the Requirements, Design, and Development Phases.
- Also has a Markdown file for listing Action Items as well, like a product backlog.
### **ESPNData**
- This holds some JSON files that are generated when running ESPN.py which utilizes the requests package.
- Includes all NHL teams with their data in nhl_teams.json.  
- Includes all NHL team rosters in nhl_team_rosters.json.
- Includes all NHL team standings in nhl_team_standings.json.
- ESPN.py parses the html at select web links for <u>espn.com</u> within the NHL category at least for nhl_teams.json.
- The main source of this data is now this api: <u>api-web.nhle.com</u>
- This portion is very underdeveloped and might be cut with future versions of the product.
- Need for this directory depends on how well the CSV and AdvancedFiltering.py file work together
### **MainObjects**
- Stores python files that deal directly with Fantasy Objects comprised of 1 Fantasy League -> Many Fantasy Teams -> Many Fantasy Players -> Either Goalie or Skater Objects. 
- There is a python file named the same as the class for each. Team.py is for Fantasy Teams, not NHL Pro Teams. 
- All methods are implemented through the League object and then passed to NHLReport to be ran based on what information is wanted. 
- Skater and Goalie inherit from the Player class and add instance variables based on positional statistic categories that generate their score each game. 
- There should eventually be more methods implemented within children classes like Team, Skater, Goalie, and Player to ease the coding stress laid on League.py.
### **ToolObjects**
- Stores python files that assist in ranking players/team rosters and gameplay analysis. 
- Matchup.py has methods that help determine the weekly highest and lowest scoring winning and losing teams and also the season best rankings as well.
- RosterGrade.py includes methods that can generate a loose ranking of Fantasy Teams within the league either at draft day or in the current state. Uses VORP to help calculate both methods.
- StreakTracker.py is probably my best tool thus far. Uses the 30 day, 15 day and 7 day stats per player and generates a streak analysis for each window to combine for a 3-fold analysis on the player. By using this, I can find players that play above their seasonal average points efficiently and filter by position, proTeam, fantasyTeam/free agent, and min/max threshold of points. 
- Hoping to make a Trade Analyzer tool at some point as well. 
### **Utils**
- This contains more base python files used by other python files, so that hard coding can be kept to just these modules.
- Constants.py has dictionaries for Fantasy Team names, proTeam abbreviations, and many more to come. 
- DataScrub.py is intended to fix some errors within CSV files, specifically lines.csv to change last names starting with Mc to capitalize the subsequent letter and then to change '-' separation between names to '/' separation.
- ESPNLeague.py is the bridge between ESPN's Fantasy API to my own version of the objects within my own League class. 
### **NHLReport.py**
- This is the main file that utilizes all methods to print outputs for the user to gain more fantasy analyses. 
- Could be rewritten to return values if an app or website were generated from these methods as well.