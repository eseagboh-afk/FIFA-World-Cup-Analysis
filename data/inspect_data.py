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

world_cup_performance = world_cup.count().groupby('home_team')
print(world_cup_performance.head(10))

