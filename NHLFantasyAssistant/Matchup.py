class Matchup:
    def __init__(self, curr_matchup_period, matchups, teams): # constructor method for Mathcup object to better reorganize more in depth statistics than espn
        self.curr_matchup_period = curr_matchup_period # pass values from myLeague in to get the proper data to run the methods in Mathcup class
        self.matchups = matchups
        self.teams = teams
        self.team_names = list(teams.keys())
        self.best_stat_dict = {"**": {"": float("-inf")}, "++": {"": float("inf")}, "--": {"": float("-inf")}, "~~": {"": float("inf")}, "HSD": {"score_deficit": float("-inf")}, "LSD": {"score_deficit": float("inf")}}
        self.team_scores = {team: [] for _ in range(self.curr_matchup_period) for team in self.team_names}

        # use Matchup methods to set up more instance variables for ease of coding
        self.full_matchup_map, self.__first_map, self.winning_teams, self.losing_teams, self.winning_scores, self.losing_scores, self.score_deficits = self.matchupGenerator()
        self.team_record_map, self.highest_winning_scores, self.highest_winning_teams, self.lowest_winning_scores, self.lowest_winning_teams, self.highest_losing_scores, self.highest_losing_teams, self.lowest_losing_scores, self.lowest_losing_teams, self.largest_score_deficits, self.highest_deficit_teams, self.smallest_score_deficits, self.lowest_deficit_teams = self.weeklyStats(self.__first_map)

    # initializes full_matchup_map, team_record_map, winning_teams, losing_teams, winning_scores, losing_scores, and score_deficits
    def matchupGenerator(self):
        full_matchup_map = {} # this becomes a nested dictionary with keys of Week Number and Matchup Number, with a list of single-value dictionaries

        # this becomes a dictionary with team names for keys and their wins and losses indexed by week number - 1 in a list
        # there is also a dictionary called streak which has dictionaries by team name, these inner dicts contain lists with win/loss streak at that week num - 1
        team_record_map = {team: [] for team in self.teams}
        
        # These are all 2D arrays indexed by week num - 1 and matchup num - 1 respectively,
        winning_teams = [[] for _ in range(1, self.curr_matchup_period)] # team names as values inside the list for winners of matchup
        losing_teams = [[] for _ in range(1, self.curr_matchup_period)] # team names as values inside the list for losers of matchup
        winning_scores = [[] for _ in range(1, self.curr_matchup_period)] # team scores as values inside the list for winners of matchup
        losing_scores = [[] for _ in range(1, self.curr_matchup_period)] # team scores as values inside the list for losers of matchup
        score_deficits = [[] for _ in range(1, self.curr_matchup_period)] # score difference between winning and losing team of mathcup as values inside the list

        
        
        for i in range(1, self.curr_matchup_period):
            key_val = 'Week ' + str(i)
            full_matchup_map[key_val] = {}

            winning_teams, winning_scores, losing_teams, losing_scores, score_deficits = self.weekMatchupInitializer(i, winning_teams, winning_scores, losing_teams, losing_scores, score_deficits)

            for j in range(len(self.teams) // 2):
                match_val = 'Matchup ' + str(j+1)
                full_matchup_map[key_val][match_val] = {}

                winning_teams_map = {'winning_team': winning_teams[i-1][j]}
                losing_teams_map = {'losing_team': losing_teams[i-1][j]}
                winning_scores_map = {'winning_score': winning_scores[i-1][j]}
                losing_scores_map = {'losing_score': losing_scores[i-1][j]}
                score_deficits_map = {'score_deficit': score_deficits[i-1][j]}
                
                

                team_record_map[winning_teams[i-1][j]].append('W')
                team_record_map[losing_teams[i-1][j]].append('L')

                full_matchup_map[key_val][match_val] = winning_teams_map, losing_teams_map, winning_scores_map, losing_scores_map, score_deficits_map
        
        return full_matchup_map, team_record_map, winning_teams, losing_teams, winning_scores, losing_scores, score_deficits
    # this method finalizes the team_record_map with the streaks included in it for each team as well
    # returns the values for the matchup stats by largest and smallest individual scores and largest and smallest score deficits for both winning and losing teams
    # takes in the self.__first_map as team_record_map for the first draft version that will be added to
    def weeklyStats(self, team_record_map):
        team_record_map["streak"] = {team: [] for team in self.teams} # initialize new dictionary 'streak' with key values of team names and empty lists as values

        # this nested for loop is what sets up the formation of the rest of the team_record_map
        # the value is the streak for each team in week order, so the proper streak is the last value.
        # this allows for accessing the streak at the time and context of that week and not just the current streak

        for team in self.teams: # use the team objects since they are a key in both subdictionaries of team_record_map
            prev_val = 0 # prev_val will be used to check if a streak is continued or broken
            streak_count = 0 # streak_count keeps track of how many losses or wins in a row

            for index in range(1, self.curr_matchup_period): # iterate over the number of completed matchups which is one less than the curr_matchup_period
                curr_val = team_record_map[team][index-1] # figure out whether the team won or lost at week (index) using the team dicitionary
                if prev_val == curr_val: # if the previous value is equal to the current value               
                    streak_count += 1 # we want to add to the streak count and leave the previous value as is

                elif prev_val == 0: # this is the check when going through for the first time in the inner loop
                    prev_val = curr_val # set the previous value to the current value for the next loop to use the previous conditional
                    streak_count += 1 # add to the streak count for it to be 1 in this case

                else: # this conditional is met when the previous value does not equal the current value
                    streak_count = 0 # reset the streak_count to 0 
                    prev_val = curr_val # set previous value equal to current value since it is different now
                    streak_count += 1 # add 1 to the streak count since this is the first one of this count
                    
                # all conditionals end with saving the previous value + the streak count (eg 'W' + 1 -> W1)    
                team_record_map['streak'][team].append(prev_val + str(streak_count))

                
        # initialize all depth scoring and team categories as empty lists to be filled
        highest_winning_scores = []
        highest_winning_teams = []
        lowest_winning_scores = []
        lowest_winning_teams = []
        highest_losing_scores = []
        highest_losing_teams = []
        lowest_losing_scores = []
        lowest_losing_teams = []
        largest_score_deficits = []
        highest_deficit_teams = []
        smallest_score_deficits = []
        lowest_deficit_teams = []
        
        # we iterate over the number of weeks since we're looking for standout stats from all 4 matchups, not just each matchup separately
        for index in range(1, self.curr_matchup_period):
            key_val = 'Week ' + str(index) # set up key_val for passing and using by self.full_matchup_map

            # set up the 6 different case callings of the helper function which consists of using the 3 different score_lists
            # winning, losing, and score_deficit are the 3, and then choosing either high or low stats for a total of 6 

            # set up for highest and winning stats, copy scores and teams into previous empty scores list and empty teams list respectively
            scores, teams = self.weekHighestAndLowestStats(key_val, True, self.winning_scores, index, highest_winning_scores, highest_winning_teams)
            highest_winning_scores = scores.copy()
            highest_winning_teams = teams.copy()
            
            # set up for lowest and winning stats
            scores, teams = self.weekHighestAndLowestStats(key_val, False, self.winning_scores, index, lowest_winning_scores, lowest_winning_teams)
            lowest_winning_scores = scores.copy()
            lowest_winning_teams = teams.copy()

            # set up for highest and losing stats, copy scores and teams into previous empty scores list and empty teams list respectively
            scores, teams = self.weekHighestAndLowestStats(key_val, True, self.losing_scores, index, highest_losing_scores, highest_losing_teams)
            highest_losing_scores = scores.copy()
            highest_losing_teams = teams.copy()

            # set up for lowest and losing stats, copy scores and teams into previous empty scores list and empty teams list respectively
            scores, teams = self.weekHighestAndLowestStats(key_val, False, self.losing_scores, index, lowest_losing_scores, lowest_losing_teams)
            lowest_losing_scores = scores.copy()
            lowest_losing_teams = teams.copy()

            # set up for highest and score deficit stats, copy scores and teams into previous empty scores list and empty teams list respectively
            scores, teams = self.weekHighestAndLowestStats(key_val, True, self.score_deficits, index, largest_score_deficits, highest_deficit_teams)
            largest_score_deficits = scores.copy()
            highest_deficit_teams = teams.copy()

            # set up for lowest and score deficit stats, copy scores and teams into previous empty scores list and empty teams list respectively
            scores, teams = self.weekHighestAndLowestStats(key_val, False, self.score_deficits, index, smallest_score_deficits, lowest_deficit_teams)
            smallest_score_deficits = scores.copy()
            lowest_deficit_teams = teams.copy()

        # return the team_record_map and the 12 lists that come from the 6 helper function calls that each return 2 lists for 13 total values returned
        return team_record_map, highest_winning_scores, highest_winning_teams, lowest_winning_scores, lowest_winning_teams, highest_losing_scores, highest_losing_teams, lowest_losing_scores, lowest_losing_teams, largest_score_deficits, highest_deficit_teams, smallest_score_deficits, lowest_deficit_teams


    # Helper function to weeklyStats that finds the max score if high is true, uses key_val and index to lookup values, passes a specific list (eg score_deficits), and empty arrays to store associated score and team values
    def weekHighestAndLowestStats(self, key_val, high, score_list, index, scores, teams):
        # initialize the values that will be used by method
        max_val = max(score_list[index-1]) 
        min_val = min(score_list[index-1])
        # if search is for highest score stats then save max_val to scores
        if high:
            scores.append(max_val)
        # otherwise save min_val to scores
        else:
            scores.append(min_val)
        # values used by all parameters
        matchup_idx = score_list[index-1].index(scores[index-1]) + 1 # figure out which matchup the desired value is located
        match_val = 'Matchup ' + str(matchup_idx) # create match_val for looking up value in full_matchup_map
        winning_team = self.full_matchup_map[key_val][match_val][0]['winning_team'] # set up winning_team with full_matchup_map
        losing_team = self.full_matchup_map[key_val][match_val][1]['losing_team'] # set up losing_team with full_matchup_map

        # sort of a conditional tree like switch statement checking what score_list I'm using
        if score_list == self.winning_scores: # if we're using winning_scores for score_list
            teams.append(winning_team) # then save winning_team to teams
            
        elif score_list == self.losing_scores: # otherwise if we're using losing_scores for score_list
            teams.append(losing_team) # then save losing_team to teams
        
        else: # this should just take care of the last case which is the score_deficits for score_list
            teams.append((winning_team, losing_team)) # we want both teams, so save both as a single tuple value
        
        return scores, teams # return the saved scores and saved teams lists 
    
    def weekMatchupInitializer(self, weekNum, winning_teams, winning_scores, losing_teams, losing_scores, score_deficits):
        for i in range(len(self.teams) // 2): 
            matchups = self.matchups[weekNum]# Iterate over the number of matches per week which should be 4 in this 8 team league
            curr_matchup = matchups[i] # use the week matchups and iterate from 0-3 to get all 4 matchups
            # set if else case to determine winning team based on being home or away since that's how the matchup object is set up
            # if home team wins
            if (curr_matchup.home_score > curr_matchup.away_score):
                # winning team and winning score -> home team name and home team score
                # losing team and losing score -> away team name and away team score
                winning_team = curr_matchup.home_team.team_name
                winning_score = curr_matchup.home_score
                losing_team = curr_matchup.away_team.team_name
                losing_score = curr_matchup.away_score
                

            # else away team wins
            else:
                # winning team and winning score -> away team name and away team score
                # losing team and losing score -> home team name and home team score
                winning_team = curr_matchup.away_team.team_name
                winning_score = curr_matchup.away_score  
                losing_team = curr_matchup.home_team.team_name
                losing_score = curr_matchup.home_score

            # set up point margin by getting the difference between winning and losing score rounded to 1 decimal place
            score_deficit = round(winning_score - losing_score, 1)

            winning_teams[weekNum-1].append(winning_team)
            winning_scores[weekNum-1].append(winning_score)
            losing_teams[weekNum-1].append(losing_team)
            losing_scores[weekNum-1].append(losing_score)
            score_deficits[weekNum-1].append(score_deficit)

        return winning_teams, winning_scores, losing_teams, losing_scores, score_deficits
    
    # This is pretty simple code for now. Just iterate over the matchup version method for all completed weeks in the season
    # **Work on getting max and min stats of the season by taking max of the depth stats lists that come from the weeklyStats method (eg max(self.largest_score_deficits))
    def seasonMatchupResults(self):
        for i in range(1, self.curr_matchup_period): # iterate over all completed matchups
            self.weeklyMatchupResults(i) # pass in the index for the week number, and call the weekly matchup function

        
        season_highest_winning_team = list(self.best_stat_dict["**"].keys())[0]
        season_highest_winning_score, highest_winning_week = list(self.best_stat_dict["**"].values())[:2]
        season_lowest_winning_team = list(self.best_stat_dict["++"].keys())[0]
        season_lowest_winning_score, lowest_winning_week = list(self.best_stat_dict["++"].values())[:2]
        season_highest_losing_team = list(self.best_stat_dict["--"].keys())[0]
        season_highest_losing_score, highest_losing_week = list(self.best_stat_dict["--"].values())[:2]
        season_lowest_losing_team  = list(self.best_stat_dict["~~"].keys())[0]
        season_lowest_losing_score, lowest_losing_week = list(self.best_stat_dict["~~"].values())[:2]
        season_highest_deficit_winning_team, season_highest_deficit_losing_team  = list(self.best_stat_dict["HSD"].keys())[1:3]
        season_highest_deficit, season_highest_deficit_winning_score, season_highest_deficit_losing_score, highest_deficit_week = list(self.best_stat_dict["HSD"].values())
        season_lowest_deficit_winning_team, season_lowest_deficit_losing_team  = list(self.best_stat_dict["LSD"].keys())[1:3]
        season_lowest_deficit, season_lowest_deficit_winning_score, season_lowest_deficit_losing_score, lowest_deficit_week = list(self.best_stat_dict["LSD"].values())

        print(f"\n\nSeason Highlights:\n\n")
        print(f"In {highest_deficit_week}, {season_highest_deficit_winning_team} [{season_highest_deficit_winning_score} pts] had the largest score deficit win in the league with {season_highest_deficit} pts against {season_highest_deficit_losing_team} [{season_highest_deficit_losing_score}]\n\n")
        print(f"In {lowest_deficit_week}, {season_lowest_deficit_winning_team} [{season_lowest_deficit_winning_score} pts] had the smallest score deficit win in the league with {season_lowest_deficit} pts against {season_lowest_deficit_losing_team} [{season_lowest_deficit_losing_score}]\n\n")
        print(f"In {highest_winning_week}, {season_highest_winning_team} had the highest score in the league of {season_highest_winning_score} pts\n\n")
        print(f"In {lowest_winning_week}, {season_lowest_winning_team} had the lowest winning score in the league of {season_lowest_winning_score} pts\n\n")
        print(f"In {highest_losing_week}, {season_highest_losing_team} had the highest losing score in the league of {season_highest_losing_score} pts\n\n")
        print(f"In {lowest_losing_week}, {season_lowest_losing_team} had the lowest score in the league of {season_lowest_losing_score} pts\n\n")

    
    # this method is pretty much finalized in the functionality, it might need help getting formatted for better readability
    # prints desired output and is a void type return
    # **maybe change this to return a string and organize what I want to go first 
    def weeklyMatchupResults(self, index):
        key_val = "Week " + str(index) # set up key_val with parameter index to help
        output = "" # set up output string to save results without immediately printing for better organization
        title = f"{key_val} Results:" # set up main title 
        # print(f"{'='*total_length}")
        # print(f"{title}".center(total_length))
        # print(f"{'='*total_length}")
        print(f'\n{title} \n') # print title each function call first

        # grab deficit values at location index to get the proper depth stats of the week
        highest_deficit = self.largest_score_deficits[index-1]
        highest_deficit_winning_team = self.highest_deficit_teams[index-1][0] # winning_team is first in tuple, so index 0
        highest_deficit_losing_team = self.highest_deficit_teams[index-1][1] # losing_team is second in tuple, so index 1
        lowest_deficit = self.smallest_score_deficits[index-1]
        lowest_deficit_winning_team = self.lowest_deficit_teams[index-1][0] # winning_team is first in tuple, so index 0
        lowest_deficit_losing_team = self.lowest_deficit_teams[index-1][1] # losing_team is second in tuple, so index 1

        # set up grabbing the streak for highest and lowest deficit teams both winning and losing for edge case in output
        highest_deficit_winning_team_streak = self.team_record_map['streak'][highest_deficit_winning_team][index-1]
        highest_deficit_losing_team_streak = self.team_record_map['streak'][highest_deficit_losing_team][index-1]
        lowest_deficit_winning_team_streak = self.team_record_map['streak'][lowest_deficit_winning_team][index-1]
        lowest_deficit_losing_team_streak = self.team_record_map['streak'][lowest_deficit_losing_team][index-1]
        

        for i in range(len(self.teams) // 2): # iterate over number of matchups or the number of teams split in half
            match_val = "Matchup " + str(i+1) # set up match_val for using full_matchup_map
            subtitle = f"{match_val} Results:" # this prints at top of every inner loop
            output += f'\n{subtitle}\n' # add the subtitle to the output string
            winning_team = self.full_matchup_map[key_val][match_val][0]['winning_team'] # get the winning_team from the full_matchup_map
            losing_team = self.full_matchup_map[key_val][match_val][1]['losing_team']# get the losing_team from the full_matchup_map
            winning_score = self.full_matchup_map[key_val][match_val][2]['winning_score'] # get the winning_score from the full_matchup_map
            losing_score = self.full_matchup_map[key_val][match_val][3]['losing_score'] # get the losing_score from the full_matchup_map
            score_deficit = self.full_matchup_map[key_val][match_val][4]['score_deficit'] # get the score_deficit from the full_matchup_map
            winning_team_streak = self.team_record_map['streak'][winning_team][index-1] # get the winning_team streak using the team_record_map
            losing_team_streak = self.team_record_map['streak'][losing_team][index-1] # get the losing_team streak using the team_record_map

            # this is the basic output for each matchup added to the output string
            output += f"{winning_team} ({winning_team_streak}) [{winning_score} pts] won against {losing_team} ({losing_team_streak}) [{losing_score} pts] by {score_deficit} pts\n"

            # add extra symbols to display teams that had the highest and lowest individual scores for both winning and losing teams
            # ** for the highest winning score team, ++ for the lowest winning score team, -- for the highest losing score team, and ~~ for the lowest losing score team

            # here is the code for the highest winning score team
            if winning_team == self.highest_winning_teams[index-1]:
                if winning_score > list(self.best_stat_dict["**"].values())[0]:
                    self.best_stat_dict["**"] = {
                        winning_team: winning_score,
                        "Week": key_val
                        } # tuple of week and matchup number for mapping to correct team for display purposes
                highest_winning_team = winning_team + "**" # update team name with associated suffix symbol 
                highest_winning_score = winning_score # grab winning score at same index
                highest_winning_team_streak = winning_team_streak


            # here is the code for the lowest winning score team
            if winning_team == self.lowest_winning_teams[index-1]:
                if winning_score < list(self.best_stat_dict["++"].values())[0]:
                    self.best_stat_dict["++"] = {
                        winning_team: winning_score,
                        "Week": key_val
                        }
                lowest_winning_team = winning_team + "++" # update team name with associated suffix symbol 
                lowest_winning_score = winning_score # grab winning score at same index
                lowest_winning_team_streak = winning_team_streak
            


            # here is the code for the highest losing score team
            if losing_team == self.highest_losing_teams[index-1]:
                if losing_score > list(self.best_stat_dict["--"].values())[0]:
                    self.best_stat_dict["--"] = {
                        losing_team: losing_score,
                        "Week": key_val
                        }
                highest_losing_team = losing_team + "--" # update team name with associated suffix symbol 
                highest_losing_score = losing_score # grab losing score at same index
                highest_losing_team_streak = losing_team_streak
                
            # here is the code for the lowest losing score team
            if losing_team == self.lowest_losing_teams[index-1]:
                if losing_score < list(self.best_stat_dict["~~"].values())[0]:
                    self.best_stat_dict["~~"] = {
                        losing_team: losing_score,
                        "Week": key_val
                        }
                lowest_losing_team = losing_team + "~~" # update team name with associated suffix symbol 
                lowest_losing_score = losing_score # grab losing score at same index
                lowest_losing_team_streak = losing_team_streak

            if winning_team == highest_deficit_winning_team:
                if highest_deficit > list(self.best_stat_dict["HSD"].values())[0]:
                    self.best_stat_dict["HSD"] = {
                        "score_deficit": highest_deficit,
                        winning_team: winning_score, 
                        losing_team: losing_score,
                        "Week": key_val,
                    }

            if winning_team == lowest_deficit_winning_team:
                if lowest_deficit < list(self.best_stat_dict["LSD"].values())[0]:
                    self.best_stat_dict["LSD"] = {
                        "score_deficit": lowest_deficit,
                        winning_team: winning_score, 
                        losing_team: losing_score,
                        "Week": key_val,
                    }
        # print statements I want to go right after the title as depth highlights of the week 
        # there are 2 print statements for each depth stat of either highest or lowest and winning or losing
        # The first print statement is individual score with team name, team streak and then the score using the saved index inside the conditional
        # The second print statement is the team with either highest or lowest deficit
        # high winning and low losing and high deficit checks, while low winning and high losing are low deficit checks
        # if the previous team is also the deficit team then use that, otherwise use the edge case defined earlier and the deficit team itself 
        print(f"{highest_winning_team} ({highest_winning_team_streak}) had the highest score of the week with a score of {highest_winning_score} pts")
        high_winner_print = f"{highest_winning_team} ({highest_winning_team_streak})"
        if highest_winning_team[:-2] != highest_deficit_winning_team: 
            high_winner_print = f"{highest_deficit_winning_team} ({highest_deficit_winning_team_streak})"
        print(f"{high_winner_print} got the win in the blowout match of the week which was by {highest_deficit} pts\n")

        print(f"{lowest_winning_team} ({lowest_winning_team_streak}) had the lowest winning score of the week with a score of {lowest_winning_score} pts")
        # print(f"{lowest_winning_team({winning_team_streak}) if lowest_winning_team[:-2] == lowest_deficit_winning_team else lowest_deficit_winning_team({lowest_deficit_winning_team_streak})} got the win in the tightest match of the week which was by {lowest_deficit} pts\n")
        low_winner_print = f"{lowest_winning_team} ({lowest_winning_team_streak})"
        if lowest_winning_team[:-2] != lowest_deficit_winning_team: 
            low_winner_print = f"{lowest_deficit_winning_team} ({lowest_deficit_winning_team_streak})"
        print(f"{low_winner_print} got the win in the tightest match of the week which was by {lowest_deficit} pts\n")

        print(f"{highest_losing_team} ({highest_losing_team_streak}) had the highest losing score of the week with a score of {highest_losing_score} pts")
        # print(f"{highest_losing_team({losing_team_streak}) if highest_losing_team[:-2] == lowest_deficit_losing_team else lowest_deficit_losing_team({lowest_deficit_losing_team_streak})} took the loss in the tighest match of the week which was by {lowest_deficit} pts\n")
        high_loser_print = f"{highest_losing_team} ({highest_losing_team_streak})"
        if highest_losing_team[:-2] != lowest_deficit_losing_team: 
            high_loser_print = f"{lowest_deficit_losing_team} ({lowest_deficit_losing_team_streak})"
        print(f"{high_loser_print} took the loss in the tightest match of the week which was by {lowest_deficit} pts\n")

        print(f"{lowest_losing_team} ({lowest_losing_team_streak}) had the lowest score of the week with a score of {lowest_losing_score} pts")
        # print(f"{lowest_losing_team({losing_team_streak}) if lowest_losing_team[:-2] == highest_deficit_losing_team else highest_deficit_losing_team({highest_deficit_losing_team_streak})} took the loss in the blowout match of the week which was by {highest_deficit} pts\n")
        low_loser_print = f"{lowest_losing_team} ({lowest_losing_team_streak})"
        if lowest_losing_team[:-2] != highest_deficit_losing_team: 
            low_loser_print = f"{highest_deficit_losing_team} ({highest_deficit_losing_team_streak})"
        print(f"{low_loser_print} took the loss in the blowout match of the week which was by {highest_deficit} pts\n")

        print(output) # print this output string at the end with all the matchup information underneath the depth stat highlights