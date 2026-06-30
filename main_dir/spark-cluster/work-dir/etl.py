from pyspark.sql import SparkSession
from pyspark.sql.functions import (
col, 
split,
regexp_replace, 
to_date,

)
import pyspark.sql.functions as F
import logging


logging.basicConfig(level=20)
logger = logging.getLogger(__name__)

class Transformer:
# Matches table 
   def make_match_table(self, df):
       match_df = df.withColumn('match_date', F.col('date').cast("date")).withColumn(
           'country_1', F.col('home_team')).withColumn('country_2', F.col('away_team')).withColumn(
               'country_1_score', F.col('home_score').try_cast('integer')
           ).withColumn('country_2_score', F.col('away_score').try_cast('integer')).withColumn(
               'winning_team', F.when(F.col('home_score') > F.col('away_score'),
                                      F.col('home_team')).when(F.col('away_score') > F.col('home_score'),
                                                               F.col('away_team')).otherwise(F.lit('N/A'))
           ).withColumn('losing_team', F.when(F.col('home_score') < F.col('away_score'),
                                              F.col('home_team')).when(F.col('away_score') < F.col('home_score'),
                                                                       F.col('away_team')).otherwise(F.lit('N/A')))
       match_df = match_df.drop('date', 'home_team', 'away_team', 'home_score', 'away_score', 'tournament','city', 'country', 'neutral')
       match_df = match_df.fillna(0, subset=['country_1_score', 'country_2_score'])
       logger.info(f"Matches table: {match_df.show()}")
       return match_df

# Countries table 
   def make_countries_table(self, df):
       countries_df = (df.select(F.col('country_1').alias('country_name')).union(df.select(F.col('country_2').alias('country_name'))).groupBy(
           'country_name').agg(F.count('*').alias('total_matches_played')))
       winners_df = (df.select(F.col('winning_team').alias('country_name')).groupBy('country_name').agg(F.count('country_name').alias('total_matches_won')))
       losers_df = (df.select(F.col('losing_team').alias('country_name')).groupBy('country_name').agg(F.count('country_name').alias('total_matches_lost')))
       goals_df = (df.select(F.col('country_1').alias('country_name'), F.col('country_1_score').alias('goals_scored'))
                   .union(df.select(F.col('country_2').alias('country_name'), F.col('country_2_score').alias('goals_scored'))
                          .groupBy('country_name').agg(F.sum('goals_scored').alias('total_goals_scored'))))
       countries_df = (countries_df.join(winners_df, 'country_name', 'left').join(losers_df, 'country_name', 'left').join(goals_df, 'country_name', 'left'))
       countries_df = countries_df.dropDuplicates()
       logger.info(f"Countries table: {countries_df.show()}")
       return countries_df
   
# Economic status table 
   def make_economic_status_table(self, df, df_2):
       economic_status_df = (df.withColumn('total_gdp', F.col('gdppc') * F.col('population')).groupBy('country')
                             .agg(F.avg('total_gdp').alias('avg_total_gdp'),
                                  F.avg('population').alias('avg_population')))
       economic_status_df = economic_status_df.drop('year', 'gdppc', 'pop')
       economic_status_df = (economic_status_df.join(df_2, on='country', how='left'))
       logger.info(f"Economic status table: {economic_status_df.show()}")
       return economic_status_df
   
# Winners table  
   def make_winners_table(self, df, df_2):
       match_winners_df = (df.withColumn('match_id', F.col('match_id')).withColumn('winning_country', F.col('winning_team')))
       match_winners_df = match_winners_df.withColumnRenamed('winning_country', 'country_name')
       df_2 = df_2.select(F.col('country_id'),F.col('country_name'))
       match_winners_df = (match_winners_df.join(df_2, on='country_name', how='left'))
       match_winners_df = match_winners_df.drop('country_name')
       logger.info(f"Match winners table: {match_winners_df.show()}")
       return match_winners_df
   
# Losers table  
   def make_losers_table(self, df, df_2):
       match_losers_df = (df.withColumn('match_id', F.col('match_id')).withColumn('losing_country', F.col('losing_team')))
       match_losers_df = match_losers_df.withColumnRenamed('losing_country', 'country_name')
       df_2 = df_2.select(F.col('country_id'), F.col('country_name'))
       match_losers_df = match_losers_df.join(df_2, on='country_name', how='left')
       match_losers_df = match_losers_df.drop('country_name')
       logger.info(f"Match losers table: {match_losers_df.show()}")
       return match_losers_df

class ETLProcessor:
    def __init__(
            self, 
            primary_csv_path: str, 
            secondary_csv_path_1: str, 
            secondary_csv_path_2: str, 
            transformer: Transformer, 
            jdbc_options: dict, 
            spark,
    ):
        self._primary_csv_path = primary_csv_path
        self._secondary_csv_path_1 = secondary_csv_path_1
        self._secondary_csv_path_2 = secondary_csv_path_2
        self._transformer = transformer
        self._jdbc_options = jdbc_options
        self._spark = spark
        
    # Extract from primary CSV
    def extract_from_primary_csv(self):
        world_cup_df = self._spark.read.csv(self._primary_csv_path, header=True, inferSchema=True)
        world_cup_df = (world_cup_df.filter(F.col('tournament') == 'FIFA World Cup')
                        .select(F.col('date'),
                        F.col('home_team'),
                        F.col('away_team'),
                        F.col('home_score'),
                        F.col('away_score'),
                        F.col('tournament')))
        logger.info(f"World Cup dataframe: {world_cup_df.printSchema()}")
        return world_cup_df
    
    # Extract from secondary CSV 1
    def extract_from_secondary_csv_1(self):
        gdp_df = self._spark.read.csv(self._secondary_csv_path_1, header=True, inferSchema=True)
        gdp_df = (gdp_df.withColumn('country', F.col('country'))
                  .withColumn('year', F.col('year'))
                  .withColumn('gdppc', F.col('gdppc'))
                  .withColumn('pop', F.col('pop')))
        logger.info(f"GDP dataframe: {gdp_df.printSchema()}")
        return gdp_df
    
    # Extract from secondary CSV 2
    def extract_from_secondary_csv_2(self):
        international_liquidity_df = self._spark.read.csv(self._secondary_csv_path_2, header=True, inferSchema=True)
        years = [str(year) for year in range(1930, 2022)]
        international_liquidity_df = (international_liquidity_df.withColumn('country', F.col('COUNTRY'))
                                      .selectExpr('country', 
                                                  f"""
                                                  stack({len(years)},
                                                  {','.join([f"'{year}', `{year}`" for year in years])}
                                                  ) as (year, international_liquidity)"""))
        logger.info(f"International Liquidity dataframe: {international_liquidity_df.show()}")
        liquidity_avg_df = (international_liquidity_df.withColumn('international_liquidity',
                                                                  F.col('international_liquidity').cast('float')).groupBy('country')
                                                                  .avg(F.avg('international_liquidity').alias('avg_international_liquidity')))
        logger.info(f"Liquidity average dataframe: {liquidity_avg_df.schema()}")
        return liquidity_avg_df

    # Load to db
    def load_to_db(self, df, table_name):
        df.write.format("jdbc").options(**self._jdbc_options, dbtable=table_name).mode("append").save()
        logger.info(f"{df} loaded to {table_name} in database: {df.printSchema()}")
    
    # Load from db
    def load_from_db(self, query):
        df = self._spark.read.format("jdbc").options(**self._jdbc_options, dbtable=query).load()
        return df 

    # Load matches table to db
    def match_table_to_db(self):
        df = self.extract_from_primary_csv()
        matches_df = self._transformer.make_match_table(df)
        self.load_to_db(matches_df, 'world_cup.matches')
    
    # Load countries table to db
    def countries_table_to_db(self):
        df = self.extract_from_primary_csv()
        df = self._transformer.make_match_table(df)
        countries_df = self._transformer.make_countries_table(df)
        self.load_to_db(countries_df, 'countries')
    
    # Load economic status table to db
    def economic_status_table_to_db(self):
        df = self.extract_from_secondary_csv_1()
        df_2 = self.extract_from_secondary_csv_2()
        countries_df = self.load_from_db("""SELECT country_name, country_id FROM countries""")
        economic_status_df = self._transformer.make_economic_status_table(df, df_2)
        economic_status_df = economic_status_df.withColumnRenamed('country', 'country_name')
        economic_status_df = economic_status_df.join(countries_df, on='country_name', how='left')
        self.load_to_db(economic_status_df, 'economic_status')
    
    # Load winners table to db
    def winners_table_to_db(self):
        source_df = self.extract_from_primary_csv()
        df = self._transformer.make_match_table(df)
        df_2 = self._transformer.make_countries_table(source_df)
        match_winners_df = self._transformer.make_winners_table(df, df_2)
        self.load_to_db(match_winners_df, 'winners')
    
    # Load losers table to db
    def losers_table_to_db(self):
        source_df = self.extract_from_primary_csv()
        df = self._transformer.make_match_table(df)
        df_2 = self._transformer.make_countries_table(source_df)
        match_losers_df = self._transformer.make_losers_table(df, df_2)
        self.load_to_db(match_losers_df, 'losers')
