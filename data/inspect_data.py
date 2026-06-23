import pandas as pd 
import numpy as np 
from scipy import stats
from scipy.stats import mstats

PATH = 'results.csv'


df = pd.read_csv(PATH)
world_cup = df[df['tournament'] == 'FIFA World Cup']
pd.set_option('display.max_column', None)
# countries_list = df[['home_team']].drop_duplicates()
# print(countries_list.info())
# print(countries_list.head(15))

# print(world_cup.info())
# print(world_cup.head(10))

winning_condition_home = world_cup['home_score'] > world_cup['away_score']
winning_home_team = world_cup[winning_condition_home]
winning_home_team['winning_country'] = winning_home_team['home_team']
# print(winning_home_team.info())
# print(winning_home_team.head(10))
winning_condition_away = world_cup['away_score'] > world_cup['home_score']
winning_away_team = world_cup[winning_condition_away]
winning_away_team['winning_country'] = world_cup['away_team']
# print(winning_away_team.info())
# print(winning_away_team.head(10))
cleaned_df = pd.concat([winning_away_team, winning_home_team], axis=0, ignore_index=True)
# print(cleaned_df.info())
# print(cleaned_df.tail(10))

# Country with the most world cup (WC) match wins = Brazil 
winners = cleaned_df['winning_country']
most_wins = winners.mode()
# print(most_wins) 

# Country with the most WC match wins after Brazil = Germany
no_brazil_condition = cleaned_df['winning_country'] != 'Brazil'
no_brazil_df = cleaned_df[no_brazil_condition]
winners_second = no_brazil_df['winning_country']
most_wins_second = winners_second.mode()
# print(most_wins_second)

# Country with the most WC match wins after Brazil and Germany = Argentina
no_brazil_germany_condition = no_brazil_df['winning_country'] != 'Germany'
no_brazil_germany_df = no_brazil_df[no_brazil_germany_condition]
winners_third = no_brazil_germany_df['winning_country']
most_wins_third = winners_third.mode()
# print(most_wins_third)

# Country with the most WC match wins after Brazil, Germany, and Argentina = Italy
fourth_winning_condition = no_brazil_germany_df['winning_country'] != 'Argentina'
fourth_winning_df = no_brazil_germany_df[fourth_winning_condition]
winners_fourth = fourth_winning_df['winning_country']
most_wins_fourth = winners_fourth.mode()
# print(most_wins_fourth)


# Country with the most WC match wins after Brazil, Germany, Argentina, and Italy = France
fifth_winning_condition = fourth_winning_df['winning_country'] != 'Italy'
fifth_winning_df = fourth_winning_df[fifth_winning_condition]
winners_fifth = fifth_winning_df['winning_country']
most_wins_fifth = winners_fifth.mode()
# print(most_wins_fifth)

# 1. Country with the most WC goals = Hungary, 1982, Hungary v. El Salvador 10-1, Hungary
# print(cleaned_df.info())
stripped_df = cleaned_df[['date','home_team','away_team','home_score','away_score','winning_country']]
# print(stripped_df.info())
# print(stripped_df.head(10))
max_goals_home = stripped_df['home_score'].max()
max_goals_away = stripped_df['away_score'].max()
max_goals_home_condition = stripped_df['home_score'] == 10.0
max_goals_away_condition = stripped_df['away_score'] == 8.0
max_goals_home_df = stripped_df[max_goals_home_condition]
max_goals_away_df = stripped_df[max_goals_away_condition]
# print(max_goals_home_df.head())
# print(max_goals_away_df.head())
# print(max_goals_home)
# print(max_goals_away)

# 2. Country with the most WC goals, after Hungary = Yugoslavia, Uruguay, Sweden
# Yugoslavia v DR Congo, 1974 9-0 Yugoslavia
# Hungary v South Korea, 1954 9-0 Hungary
# Germany v Saudi Arabia, 2002 8-0 Germany
# Uruguay v Bolivia, 1950 8-0 Uruguay
# Sweden v Cuba, 1938 8-0 Sweden
# Germany v Turkey, 1954 7-0 Germany
# Italy v United States, 1934 7-1 Italy
# France v Paraguay, 1958 7-3 France
# Brazil v Sweden, 1950 7-1 Brazil
# Portugal v North Korea, 2010 7-1 Portugal
# Germany v Curaçao, 2026 7-1 Germany
# Spain v Costa Rica, 2022 7-0 Spain
# Spain v Bulgaria, 1998 6-1 Spain
# Russia v. Hungary, 1986 6-0 Russia
# France v Germany, 1958 6-3 France
# Canada v Qatar, 2026 6-0 Canada
# England v Iran, 2022 6-2 England
# Argentina v Mexico, 1930 6-3 Argentina
# England v Panama, 2018 6-1 England
# Germany v Mexico, 1978 6-0 Germany
# Argentina v Peru, 1978 6-0 Argentina

max_goals_home_second_condition = stripped_df['home_score'] < 10.0
max_goals_away_second_condition = stripped_df['home_score'] < 8.0
max_goals_home_df_second = stripped_df[max_goals_home_second_condition]
max_goals_away_df_second = stripped_df[max_goals_away_second_condition]
# print(max_goals_away_df_second.head())
# print(max_goals_home_df_second.head())

top_scores_home = stripped_df.sort_values(by='home_score', ascending=False)
top_scores_away = stripped_df.sort_values(by='away_score', ascending=False)
print(top_scores_home.head(40))
print(top_scores_home.tail(40))
print(top_scores_away.head(20))
print(top_scores_away.tail(20))
# Most goals: Hungary, Yugoslavia 



# Countries that have won the most WC matches
# 1. Brazil
# 2. Germany
# 3. Argentina
# 4. Italy
# 5. France



