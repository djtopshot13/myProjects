class Matchup:
    def __init__(self, curr_matchup_period, matchups, teams): # constructor method for Mathcup object to better reorganize more in depth statistics than espn
        self.curr_matchup_period = curr_matchup_period # pass values from myLeague in to get the proper data to run the methods in Mathcup class
        self.matchups = matchups
        self.teams = teams

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
    
    def weeklyStats(self, team_record_map):
        team_record_map["streak"] = {team: [] for team in self.teams}
      
        # for team in self.teams:
        #     prev_val = 0
        #     streak_count = 0  

        #     for index in range(matchup_period - 1, -1, -1):
        #         curr_val = team_record_map[team][index]
        #         if prev_val == curr_val:
        #             streak_count += 1

        #         elif prev_val == 0:
        #             prev_val = curr_val
        #             streak_count += 1

        #         else:
        #             team_record_map['streak'][team].append(prev_val + str(streak_count))
        #             break

        for team in self.teams:
            prev_val = 0
            streak_count = 0  

            for index in range(self.curr_matchup_period-1):
                curr_val = team_record_map[team][index]
                if prev_val == curr_val:
                    streak_count += 1

                elif prev_val == 0:
                    prev_val = curr_val
                    streak_count += 1

                else:
                    streak_count = 0
                    prev_val = curr_val
                    streak_count += 1
                    
                    
                team_record_map['streak'][team].append(prev_val + str(streak_count))

                

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
        
        for index in range(1, self.curr_matchup_period):
            key_val = 'Week ' + str(index)
            # highest_winning_scores.append([])
            # highest_winning_teams.append([])
            # lowest_winning_scores.append([])
            # lowest_winning_teams.append([])
            # highest_losing_scores.append([])
            # highest_losing_teams.append([])
            # lowest_losing_scores.append([])
            # lowest_losing_teams.append([])
            # largest_score_deficits.append([])
            # highest_deficit_teams.append([])
            # smallest_score_deficits.append([])
            # lowest_deficit_teams.append([])


            scores, teams = self.weekHighestAndLowestStats(key_val, True, self.winning_scores, index, highest_winning_scores, highest_winning_teams)
            highest_winning_scores = scores.copy()
            highest_winning_teams = teams.copy()

            scores, teams = self.weekHighestAndLowestStats(key_val, False, self.winning_scores, index, lowest_winning_scores, lowest_winning_teams)
            lowest_winning_scores = scores.copy()
            lowest_winning_teams = teams.copy()

            scores, teams = self.weekHighestAndLowestStats(key_val, True, self.losing_scores, index, highest_losing_scores, highest_losing_teams)
            highest_losing_scores = scores.copy()
            highest_losing_teams = teams.copy()

            scores, teams = self.weekHighestAndLowestStats(key_val, False, self.losing_scores, index, lowest_losing_scores, lowest_losing_teams)
            lowest_losing_scores = scores.copy()
            lowest_losing_teams = teams.copy()

            scores, teams = self.weekHighestAndLowestStats(key_val, True, self.score_deficits, index, largest_score_deficits, highest_deficit_teams)
            largest_score_deficits = scores.copy()
            highest_deficit_teams = teams.copy()

            scores, teams = self.weekHighestAndLowestStats(key_val, False, self.score_deficits, index, smallest_score_deficits, lowest_deficit_teams)
            smallest_score_deficits = scores.copy()
            lowest_deficit_teams = teams.copy()

        # print(highest_winning_teams)
        # print(highest_winning_scores)

        # print(lowest_winning_teams)
        # print(lowest_winning_scores)
        
        return team_record_map, highest_winning_scores, highest_winning_teams, lowest_winning_scores, lowest_winning_teams, highest_losing_scores, highest_losing_teams, lowest_losing_scores, lowest_losing_teams, largest_score_deficits, highest_deficit_teams, smallest_score_deficits, lowest_deficit_teams

    def weekHighestAndLowestStats(self, key_val, high, score_dict, index, scores, teams):
        max_val = max(score_dict[index-1]) 
        min_val = min(score_dict[index-1])
        if high:
            scores.append(max_val)
        else:
            scores.append(min_val)

        matchup_idx = score_dict[index-1].index(scores[index-1]) + 1
        match_val = 'Matchup ' + str(matchup_idx)
        winning_team = self.full_matchup_map[key_val][match_val][0]['winning_team']
        losing_team = self.full_matchup_map[key_val][match_val][1]['losing_team']

        if score_dict == self.winning_scores:
            teams.append(winning_team)
            
        elif score_dict == self.losing_scores:
            teams.append(losing_team)
        
        else: 
            teams.append((winning_team, losing_team))
        
        return scores, teams
    
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
    
    
    def seasonMatchupResults(self):
        for i in range(1, self.curr_matchup_period):
            self.weeklyMatchupResults(i)
    
    def weeklyMatchupResults(self, index):

        key_val = "Week " + str(index)
        output = ""
        title = f"{key_val} Matchup Results:"
        # print(f"{'='*total_length}")
        # print(f"{title}".center(total_length))
        # print(f"{'='*total_length}")
        print(f'\n{title} \n')

        highest_deficit = self.largest_score_deficits[index-1]
        highest_deficit_winning_team = self.highest_deficit_teams[index-1][0]
        highest_deficit_losing_team = self.highest_deficit_teams[index-1][1]
        lowest_deficit = self.smallest_score_deficits[index-1]
        lowest_deficit_winning_team = self.lowest_deficit_teams[index-1][0]
        lowest_deficit_losing_team = self.lowest_deficit_teams[index-1][1]

        

        for i in range(len(self.teams) // 2):
            match_val = "Matchup " + str(i+1)
            subtitle = f"{match_val} Results:"
            output += f'\n{subtitle}\n'
            winning_team = self.full_matchup_map[key_val][match_val][0]['winning_team']
            losing_team = self.full_matchup_map[key_val][match_val][1]['losing_team']
            winning_score = self.full_matchup_map[key_val][match_val][2]['winning_score']
            losing_score = self.full_matchup_map[key_val][match_val][3]['losing_score']
            score_deficit = self.full_matchup_map[key_val][match_val][4]['score_deficit']

            output += f"{winning_team}({self.team_record_map['streak'][winning_team][index-1]}) [{winning_score} pts] won against {losing_team}({self.team_record_map['streak'][losing_team][index-1]}) [{losing_score} pts] by {score_deficit} pts\n"

            if winning_team == self.highest_winning_teams[index-1]:
                highest_winning_team = winning_team + "**"
                highest_winning_score = self.winning_scores[index-1]
                highest_win_index = i
                # print(f"{winning_team} had the highest score of the week with a score of {highest_winning_score} pts")

                # print(f"{highest_winning_team if winning_team == highest_deficit_winning_team else highest_deficit_winning_team} got the win in the blowout match of the week which was by {highest_deficit} pts")

            if winning_team == self.lowest_winning_teams[index-1]:
                lowest_winning_team = winning_team + "++"
                lowest_winning_score = self.winning_scores[index-1]
                lowest_win_index = i
                # print(f"{lowest_winning_team} had the lowest winning score of the week with a score of {lowest_winning_score} pts")

                # print(f"{lowest_winning_team if winning_team == lowest_deficit_winning_team else lowest_deficit_winning_team} got the win in the tightest match of the week which was by {lowest_deficit} pts")


            if losing_team == self.highest_losing_teams[index-1]:
                highest_losing_team = losing_team + "--"
                highest_losing_score = self.losing_scores[index-1]
                highest_loss_index = i
                # print(f"{highest_losing_team} had the highest score of the week with a score of {highest_losing_score} pts")

                # print(f"{highest_losing_team if losing_team == lowest_deficit_losing_team else lowest_deficit_losing_team} took the loss in the tighest match of the week which was by {lowest_deficit} pts")

            if losing_team == self.lowest_losing_teams[index-1]:
                lowest_losing_team = losing_team + "~~"
                lowest_losing_score = self.losing_scores[index-1]
                lowest_loss_index = i
                # print(f"{lowest_losing_team} had the lowest winning score of the week with a score of {lowest_losing_score} pts")
                
                # print(f"{lowest_losing_team if losing_team == highest_deficit_losing_team else highest_deficit_losing_team} took the loss in the blowout match of the week which was by {highest_deficit} pts")
        
        print(f"{highest_winning_team} had the highest score of the week with a score of {highest_winning_score[highest_win_index]} pts")

        print(f"{highest_winning_team if highest_winning_team[:-2] == highest_deficit_winning_team else highest_deficit_winning_team} got the win in the blowout match of the week which was by {highest_deficit} pts\n") 
            
        print(f"{lowest_winning_team} had the lowest winning score of the week with a score of {lowest_winning_score[lowest_win_index]} pts")

        print(f"{lowest_winning_team if lowest_winning_team[:-2] == lowest_deficit_winning_team else lowest_deficit_winning_team} got the win in the tightest match of the week which was by {lowest_deficit} pts\n")

        print(f"{highest_losing_team} had the highest losing score of the week with a score of {highest_losing_score[highest_loss_index]} pts")

        print(f"{highest_losing_team if highest_losing_team[:-2] == lowest_deficit_losing_team else lowest_deficit_losing_team} took the loss in the tighest match of the week which was by {lowest_deficit} pts\n")

        print(f"{lowest_losing_team} had the lowest score of the week with a score of {lowest_losing_score[lowest_loss_index]} pts")
                
        print(f"{lowest_losing_team if lowest_losing_team[:-2] == highest_deficit_losing_team else highest_deficit_losing_team} took the loss in the blowout match of the week which was by {highest_deficit} pts\n")

        print(output)