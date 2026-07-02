from pyspark.sql import SparkSession
from etl import Transformer, ETLProcessor

PRIMARY_CSV = '/opt/spark/work-dir/results.csv'
SECONDARY_CSV_1 = '/opt/spark/work-dir/gdp_dataset.csv'
SECONDARY_CSV_2 = '/opt/spark/work-dir/international_liquidity.csv'

def load_matches():
    spark = SparkSession.builder.appName("FifaWorldCup").config("spark.jars", "/opt/spark/jars/postgresql-42.7.10.jar").getOrCreate()

    jdbc_options = {
    "url": spark.conf.get("spark.postgresql.capstone-db-2.url"),
    "user": spark.conf.get("spark.postgresql.world_cup.user"),
    "password": spark.conf.get("spark.postgresql.world_cup.password"),
    "driver": "org.postgresql.Driver",
}

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
    spark.stop()

def load_countries():
    spark = SparkSession.builder.appName("FifaWorldCup").config("spark.jars", "/opt/spark/jars/postgresql-42.7.10.jar").getOrCreate()

    jdbc_options = {
    "url": spark.conf.get("spark.postgresql.capstone-db-2.url"),
    "user": spark.conf.get("spark.postgresql.world_cup.user"),
    "password": spark.conf.get("spark.postgresql.world_cup.password"),
    "driver": "org.postgresql.Driver",
}

    transformer = Transformer()

    processor = ETLProcessor(
        PRIMARY_CSV, 
        SECONDARY_CSV_1, 
        SECONDARY_CSV_2,
        transformer, 
        jdbc_options,
        spark

    )

    processor.countries_table_to_db()
    spark.stop()

def load_economic_status():
    spark = SparkSession.builder.appName("FifaWorldCup").config("spark.jars", "/opt/spark/jars/postgresql-42.7.10.jar").getOrCreate()

    jdbc_options = {
    "url": spark.conf.get("spark.postgresql.capstone-db-2.url"),
    "user": spark.conf.get("spark.postgresql.world_cup.user"),
    "password": spark.conf.get("spark.postgresql.world_cup.password"),
    "driver": "org.postgresql.Driver",
}

    transformer = Transformer()

    processor = ETLProcessor(
        PRIMARY_CSV, 
        SECONDARY_CSV_1, 
        SECONDARY_CSV_2,
        transformer, 
        jdbc_options,
        spark

    )

    processor.economic_status_table_to_db()
    spark.stop()


def load_winners():
    spark = SparkSession.builder.appName("FifaWorldCup").config("spark.jars", "/opt/spark/jars/postgresql-42.7.10.jar").getOrCreate()

    jdbc_options = {
    "url": spark.conf.get("spark.postgresql.capstone-db-2.url"),
    "user": spark.conf.get("spark.postgresql.world_cup.user"),
    "password": spark.conf.get("spark.postgresql.world_cup.password"),
    "driver": "org.postgresql.Driver",
}

    transformer = Transformer()

    processor = ETLProcessor(
        PRIMARY_CSV, 
        SECONDARY_CSV_1, 
        SECONDARY_CSV_2,
        transformer, 
        jdbc_options,
        spark

    )

    processor.winners_table_to_db()
    spark.stop()

def load_losers():
    spark = SparkSession.builder.appName("FifaWorldCup").config("spark.jars", "/opt/spark/jars/postgresql-42.7.10.jar").getOrCreate()

    jdbc_options = {
    "url": spark.conf.get("spark.postgresql.capstone-db-2.url"),
    "user": spark.conf.get("spark.postgresql.world_cup.user"),
    "password": spark.conf.get("spark.postgresql.world_cup.password"),
    "driver": "org.postgresql.Driver",
}

    transformer = Transformer()

    processor = ETLProcessor(
        PRIMARY_CSV, 
        SECONDARY_CSV_1, 
        SECONDARY_CSV_2,
        transformer, 
        jdbc_options,
        spark

    )

    processor.losers_table_to_db()
    spark.stop()

if __name__ == "__main__":
    load_matches()
    load_countries()
    load_economic_status()
    load_winners()
    load_losers()