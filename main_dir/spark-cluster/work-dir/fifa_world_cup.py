from pyspark.sql import SparkSession
from etl import Transformer, ETLProcessor


spark = SparkSession.builder.appName("FifaWorldCup").config("spark.jars", "/opt/spark/jars/postgresql-42.7.10.jar").getOrCreate()


jdbc_options = {
    "url": spark.conf.get("spark.postgresql.capstone-db-2.url"),
    "user": spark.conf.get("spark.postgresql.world_cup.user"),
    "password": spark.conf.get("spark.postgresql.world_cup.password"),
    "driver": "org.postgresql.Driver",
}

PRIMARY_CSV = '/opt/spark/work-dir/input/results.csv'
SECONDARY_CSV_1 = '/opt/spark/work-dir/input/gdp_dataset.csv'
SECONDARY_CSV_2 = '/opt/spark/work-dir/input/international_liquidity.csv'

transformer = Transformer()

processor = ETLProcessor(
    PRIMARY_CSV, 
    SECONDARY_CSV_1, 
    SECONDARY_CSV_2,
    transformer, 
    jdbc_options,
    spark

)

processor.match_table_to_db()
processor.countries_table_to_db()
processor.economic_status_table_to_db()
processor.winners_table_to_db()
processor.losers_table_to_db()

spark.stop()
