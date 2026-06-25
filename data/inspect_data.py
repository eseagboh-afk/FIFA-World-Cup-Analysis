import pandas as pd 
import numpy as np 
from scipy import stats
from scipy.stats import mstats

PATH = 'results.csv'


df = pd.read_csv(PATH)
world_cup = df[df['tournament'] == 'FIFA World Cup']
pd.set_option('display.max_row', None)
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
# print(top_scores_home.head(40))
# print(top_scores_home.tail(40))
# print(top_scores_away.head(20))
# print(top_scores_away.tail(20))

stripped_df['losing_country'] = np.where(
    stripped_df['winning_country'] == stripped_df['home_team'],
    stripped_df['away_team'],
    stripped_df['home_team']
)
stripped_df['goals_scored_by_winner'] = np.where(
    stripped_df['winning_country'] == stripped_df['home_team'],
    stripped_df['home_score'],
    stripped_df['away_score']
)

stripped_df['goals_scored_by_loser'] = np.where(
    stripped_df['losing_country'] == stripped_df['home_team'],
    stripped_df['home_score'],
    stripped_df['away_score']
)
# print(stripped_df.info())
# print(stripped_df.head(10))

most_goals_winners_df = stripped_df.groupby('winning_country')['goals_scored_by_winner'].sum().sort_values(ascending=False).reset_index()
most_goals_losers_df = stripped_df.groupby('losing_country')['goals_scored_by_loser'].sum().sort_values(ascending=False).reset_index()
num_of_matches_played_losers_df = stripped_df.groupby('losing_country')['date'].count().reset_index()
num_of_matches_played_winners_df = stripped_df.groupby('winning_country')['date'].count().reset_index()
num_of_matches_played_winners_df.rename(columns={'winning_country':'country', 'date':'matches_won'}, inplace=True)
num_of_matches_played_losers_df.rename(columns={'losing_country':'country', 'date':'matches_lost'}, inplace=True)
num_of_matches = pd.merge(num_of_matches_played_winners_df, num_of_matches_played_losers_df, on='country')
num_of_matches['total_matches_played'] = num_of_matches['matches_won'] + num_of_matches['matches_lost']
# print(num_of_matches.info())
# print(num_of_matches.head(63))
# print(num_of_matches_played_losers_df.head(10))
# print(num_of_matches_played_winners_df.head(10))
# print(most_goals_winners_df.head(80))
# print(most_goals_losers_df.head(80))

# all_countries = stripped_df['winning_country'].drop_duplicates().to_list()
# all_countries = set(all_countries)
# print(all_countries)
# total = 0

# losing_countries = stripped_df['losing_country'].to_list()

#Countries that have conceded the most WC matches 
# match_loss_count = {country: losing_countries.count(country) for country in all_countries}
# sorted_match_loss_count = dict(sorted(match_loss_count.items(), key= lambda x:x[1], reverse=True))
# print(sorted_match_loss_count)

# print(stripped_df.info())

# print(num_of_matches.head(63).sort_values('total_matches_played', ascending=True))
# print(num_of_matches['total_matches_played'].mean())

# elite_teams = num_of_matches['total_matches_played'].quantile(0.90)
# print(elite_teams)


# Top 5 Countries that have won the most WC matches
# 1. Brazil
# 2. Germany
# 3. Argentina
# 4. Italy
# 5. France

# Top 5 Countries that have scored the most goals in WC matches
# 1. Brazil (226 goals)
# 2. Germany (218 goals)
# 3. Argentina (140 goals)
# 4. France (127 goals)
# 5. Italy (113 goals)

# As of Wednesday June 24th 2026, there have been a total of 152 WC matches

# Top 5 Countries that have played the most matches in WC history (This metric indicates
# that a team consistently qualifies for the WC and advances steadily through the tournament; 
# This metric includes the 2026 ongoing WC tournament)
# 1. Brazil (95 matches)
# 2. Germany (92 matches)
# 3. Argentina (72 matches)
# 4. Italy (62 matches)
# 5. France (60 matches)

# Top 5 Countries with the most WC match concessions (ATTENTION: more concessions means more matches played,
# this metric is measured out of at least 33 matches played;
# 33 matches played would mean the country has qualified consistently for the WC - at least 50% of WC tournaments
# and/or has consistently advanced past the group stage)
# 1. Mexico (28 matches lost out of 47)
# 2. Argentina (24 matches lost out of 72)
# 3. Germany (23 matches lost out of 92)
# 4. France (20 matches lost out of 60)
# 5. England (20 matches lost out of 53)

# Top 5 countries with the least WC match concessions in 90th percentile
# 1. Italy (17 matches lost out of 62)
# 2. Brazil (19 matches lost out of 95)
# 3. Spain (19 matches lost out of 50)
# 4. France (20 matches lost out of 60) 
# 5. England (20 matches lost out of 53) 

# Top 5 Countries with the least WC match concessions (ATTENTION: more concessions means more matches played,
# this metric is measured out of at least 23 matches played (the avg);)
# 1. Croatia (10 matches lost out of 23)
# 2. The Netherlands (11 matches lost out of 41)
# 3. Portugal (12 matches lost out of 29)
# 4. Yugoslavia (12 matches lost out of 26)
# 5. Austria (13 matches lost out of 26)

# num_of_matches_played_losers_df = num_of_matches_played_losers_df.rename(column={'losing_country':'country'})
# num_of_matches_played_winners_df = num_of_matches_played_winners_df.rename(column={'winning_country':'country'})
# print(num_of_matches_played_losers_df.head(85))
# print(num_of_matches_played_winners_df.head(63))

# Top 5 countries that have played the least WC matches in WC history (This metric indicates
# that a team does not consistently qualify for the WC and/or does not advance steadily through the tournament; 
# This metric includes the 2026 ongoing WC tournament)
# 1. Cuba (2 matches played)
# 2. Slovakia (3 matches played)
# 3. Jamaica (3 matches played)
# 4. Wales (4 matches played)
# 5. Czech Republic (4 matches played)

# Top 6 countries with the least WC match concessions (ATTENTION: Looking at 6 because of the inclusion of 
# German DR in this list (a now obsolete country), less concessions often means less matches played,
# this metric is qualified by number of matches played;
# Less than 22 matches played would mean the country has either NOT qualified for every WC, excluding 2026, or has NOT advanced past the group stage)
# 1. Cuba (1 match lost out of 2)
# 2. Ukraine (2 matches lost out of 4)
# 3. Slovakia (2 matches lost out of 3)
# 4. German DR - Soviet Communist state of East Germany, obsolete post 1990 (2 matches lost out of 4)
# 5. Jamaica (2 matches lost out of 3)
# 6. Czech Republic (3 matches lost out of 4)

# Avg number of matches played approx 23

# * Top performing countries and their 2026 World Cup team demographics:
#     - Brazil
#         * Clubs of starting 11 of their first World Cup match: 
#         * Weekly salary of starting 11
#     - Italy
#         * Clubs of starting 11
#         * Weekly salary of starting 11
#     - Argentina
#         * Clubs of starting 11
#         * Weekly salary of starting 11
#      - France
#         * Clubs of starting 11
#         * Weekly salary of starting 11
#      - Germany
#         * Clubs of starting 11
#         * Weekly salary of starting 11


PATH_GDP = 'gdp_dataset.csv'
gdp_df = pd.read_csv(PATH_GDP)

# print(gdp_df.info())

# Brazil
brazil = gdp_df['countrycode'] == 'BRA'
brazil_gdp = gdp_df[brazil]
year = brazil_gdp['year'] > 1930 
brazil_gdp = brazil_gdp[year]
# print(brazil_gdp.info())

avg_gdp_brazil = brazil_gdp['gdppc'].mean()
avg_pop_brazil = brazil_gdp['pop'].mean()
print(avg_gdp_brazil)

# Italy
italy = gdp_df['countrycode'] == 'ITA'
italy_gdp = gdp_df[italy]
year = italy_gdp['year'] > 1930 
italy_gdp = italy_gdp[year]
# print(italy_gdp.info())

avg_gdp_italy = italy_gdp['gdppc'].mean()
avg_pop_italy = italy_gdp['pop'].mean()
print(avg_gdp_italy)

# Argentina
argentina = gdp_df['countrycode'] == 'ARG'
argentina_gdp = gdp_df[argentina]
year = argentina_gdp['year'] > 1930 
argentina_gdp = argentina_gdp[year]
avg_gdp_argentina = argentina_gdp['gdppc'].mean()
avg_pop_argentina = argentina_gdp['pop'].mean()

# France
france = gdp_df['countrycode'] == 'FRA'
france_gdp = gdp_df[france]
year = france_gdp['year'] > 1930 
france_gdp = france_gdp[year]
avg_gdp_france = france_gdp['gdppc'].mean()
avg_pop_france = france_gdp['pop'].mean()

# Germany
germany = gdp_df['countrycode'] == 'DEU'
germany_gdp = gdp_df[germany]
year = germany_gdp['year'] > 1930 
germany_gdp = germany_gdp[year]
avg_gdp_germany = germany_gdp['gdppc'].mean()
avg_pop_germany = germany_gdp['pop'].mean()
germany_gdp_total = avg_gdp_germany * avg_pop_germany

# China
china = gdp_df['countrycode'] == 'HKG'
china_gdp = gdp_df[china]
year = china_gdp['year'] > 1930 
china_gdp = china_gdp[year]
avg_gdp_china = china_gdp['gdppc'].mean()
avg_pop_china = china_gdp['pop'].mean()

# Israel
israel = gdp_df['countrycode'] == 'ISR'
israel_gdp = gdp_df[israel]
year = israel_gdp['year'] > 1930 
israel_gdp = israel_gdp[year]
avg_gdp_israel = israel_gdp['gdppc'].mean()
avg_pop_israel = israel_gdp['pop'].mean()

# Angola
angola = gdp_df['countrycode'] == 'AGO'
angola_gdp = gdp_df[angola]
year = angola_gdp['year'] > 1930 
angola_gdp = angola_gdp[year]
avg_gdp_angola = angola_gdp['gdppc'].mean()
avg_pop_angola = angola_gdp['pop'].mean()

# Slovenia
slovenia = gdp_df['countrycode'] == 'SVN'
slovenia_gdp = gdp_df[slovenia]
year = slovenia_gdp['year'] > 1930 
slovenia_gdp = slovenia_gdp[year]
avg_gdp_slovenia = slovenia_gdp['gdppc'].mean()
avg_pop_slovenia = slovenia_gdp['pop'].mean()


# Jordan
jordan = gdp_df['countrycode'] == 'JOR'
jordan_gdp = gdp_df[jordan]
year = jordan_gdp['year'] > 1930 
jordan_gdp = jordan_gdp[year]
avg_gdp_jordan = jordan_gdp['gdppc'].mean()
avg_pop_jordan = jordan_gdp['pop'].mean()

def total_gdp(avg_gdppc, avg_pop):
    total = avg_gdppc * avg_pop
    return total 


# Average GDPPCs
print(f"Brazil:{avg_gdp_brazil}\nItaly:{avg_gdp_italy}\n Argentina:{avg_gdp_argentina}\n France:{avg_gdp_france}\n Germany:{avg_gdp_germany}")

# Average total gdp
# Brazil
# print(f"Brazil total gdp: {total_gdp(avg_gdp_brazil, avg_pop_brazil)}")
# # Italy
# print(f"Italy total gdp: {total_gdp(avg_gdp_italy, avg_pop_italy)}")
# # Argentina 
# print(f"Argentina total gdp: {total_gdp(avg_gdp_argentina, avg_pop_argentina)}")
# # France 
# print(f"France total gdp: {total_gdp(avg_gdp_france, avg_pop_france)}")
# # Germany
# print(f"Germany total gdp: {total_gdp(avg_gdp_germany, avg_pop_germany)}")
# # China
# print(f"China total gdp: {total_gdp(avg_gdp_china, avg_pop_china)}")
# # Israel 
# print(f"Israel total gdp: {total_gdp(avg_gdp_israel, avg_pop_israel)}")
# # Angola
# print(f"Angola total gdp: {total_gdp(avg_gdp_angola, avg_pop_angola)}")
# # Slovenia
# print(f"Slovenia total gdp: {total_gdp(avg_gdp_slovenia, avg_pop_slovenia)}")
# # Jordan
# print(f"Jordan total gdp: {total_gdp(avg_gdp_jordan, avg_pop_jordan)}")

PATH_LIQUIDITY_INTERNATIONAL = 'international_liquidity.csv'
li_df = pd.read_csv(PATH_LIQUIDITY_INTERNATIONAL)
# print(li_df.info())
print(li_df.head(5))

# Codes
# Brazil: BRA.TRGMV_REVS.USD.A
# Italy: ITA.TRGMV_REVS.XDR.A
# Argentina: ARG.TRGMV_REVS.USD.A
# France: FRA.TRGMV_REVS.USD.A
# Germany: DEU.TRGMV_REVS.XDR.A
# China: HKG.TRGMV_REVS.USD.A
# Israel: ISR.TRGMV_REVS.XDR.A
# Angola: AGO.TRGMV_REVS.USD.A
# Slovenia: SVN.TRGMV_REVS.XDR.A
# Jordan: JOR.TRGMV_REVS.USD.A

wanted_countries = ['BRA.TRGMV_REVS.USD.A', 'ITA.TRGMV_REVS.XDR.A', 
                    'ARG.TRGMV_REVS.USD.A', 'FRA.TRGMV_REVS.USD.A',
                    'DEU.TRGMV_REVS.XDR.A', 'HKG.TRGMV_REVS.USD.A', 'ISR.TRGMV_REVS.XDR.A',
                    'AGO.TRGMV_REVS.USD.A', 'SVN.TRGMV_REVS.XDR.A', 'JOR.TRGMV_REVS.USD.A']

all_countries = li_df['SERIES_CODE'].to_list()
unwanted = []

for country in all_countries:
    if country not in wanted_countries:
        unwanted.append(country)

# li_df = li_df.drop(unwanted, axis=0)

new_li_df = li_df[li_df['SERIES_CODE'].isin(wanted_countries)]
print(new_li_df.head())
