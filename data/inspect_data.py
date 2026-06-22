import pandas as pd 

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
print(winning_home_team.info())
print(winning_home_team.head(10))
winning_condition_away = world_cup['away_score'] > world_cup['home_score']
winning_away_team = world_cup[winning_condition_away]
winning_away_team['winning_country'] = world_cup['away_team']
print(winning_away_team.info())
print(winning_away_team.head(10))
cleaned_df = pd.concat([winning_away_team, winning_home_team], axis=0, ignore_index=True)
print(cleaned_df.info())
print(cleaned_df.tail(10))

