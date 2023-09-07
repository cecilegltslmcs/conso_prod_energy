import time
from pyspark.sql import functions as F
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StringType, StructType, StructField, FloatType, IntegerType, TimestampType
from WriteRowMongo import WriteRowMongo
from dotenv import load_dotenv
import os

load_dotenv()

time.sleep(10)

# create variables used for stream & identification
IP_SERVER = "kafka:9092"
TOPIC_NAME = "electricity_production"
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
URI = f"mongodb://{USER}:{PASSWORD}@{HOST}:{PORT}"

if __name__ == "__main__":
    # initialize sparkSession & sparkContext
    spark = (SparkSession
             .builder
             .master('spark://spark:7077')
             .config("spark.mongodb.input.uri", URI)
             .config("spark.mongodb.output.uri", URI)
             .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2")
             .appName("energy_prod_conso")
             .getOrCreate())
    sc = spark.sparkContext.setLogLevel("ERROR")

    # Schema definition
    schema = StructType([
        StructField("code_insee_region", StringType(), True),
        StructField("libelle_region", StringType(), True),
        StructField("nature", StringType(), True),
        StructField("heure", TimestampType(), True),
        StructField("consommation", IntegerType(), True),
        StructField("thermique", IntegerType(), True),
        StructField("nucleaire", IntegerType(), True),
        StructField("eolien", IntegerType(), True),
        StructField("solaire", IntegerType(), True),
        StructField("hydraulique", IntegerType(), True),
        StructField("pompage", IntegerType(), True),
        StructField("bioenergies", IntegerType(), True),
        StructField("ech_physiques", IntegerType(), True),
        StructField("stockage_batterie", IntegerType(), True),
        StructField("destockage_batterie", IntegerType(), True),
        StructField("eolien_terrestre", IntegerType(), True),
        StructField("eolien_offshore", IntegerType(), True),
        StructField("flux_physiques_d_auvergne_rhone_alpes_vers_nouvelle_aquitaine", FloatType(), True),
        StructField("flux_physiques_de_bourgogne_franche_comte_vers_nouvelle_aquitaine", FloatType(), True),
        StructField("flux_physiques_de_bretagne_vers_nouvelle_aquitaine", FloatType(), True),
        StructField("flux_physiques_de_centre_val_de_loire_vers_nouvelle_aquitaine", FloatType(), True),
        StructField("flux_physiques_de_grand_est_vers_nouvelle_aquitaine", FloatType(), True),
        StructField("flux_physiques_de_hauts_de_france_vers_nouvelle_aquitaine", FloatType(), True),
        StructField("flux_physiques_d_ile_de_france_vers_nouvelle_aquitaine", FloatType(), True),
        StructField("flux_physiques_de_normandie_vers_nouvelle_aquitaine", FloatType(), True),
        StructField("flux_physiques_de_nouvelle_aquitaine_vers_nouvelle_aquitaine", FloatType(), True),
        StructField("flux_physiques_d_occitanie_vers_nouvelle_aquitaine", FloatType(), True),
        StructField("flux_physiques_de_pays_de_la_loire_vers_nouvelle_aquitaine", FloatType(), True),
        StructField("flux_physiques_de_paca_vers_nouvelle_aquitaine", FloatType(), True),
        StructField("flux_physiques_de_nouvelle_aquitaine_vers_auvergne_rhone_alpes", FloatType(), True),
        StructField("flux_physiques_de_nouvelle_aquitaine_vers_bourgogne_franche_comte", FloatType(), True),
        StructField("flux_physiques_de_nouvelle_aquitaine_vers_bretagne", FloatType(), True),
        StructField("flux_physiques_de_nouvelle_aquitaine_vers_centre_val_de_loire", FloatType(), True),
        StructField("flux_physiques_de_nouvelle_aquitaine_vers_grand_est", FloatType(), True),
        StructField("flux_physiques_de_nouvelle_aquitaine_vers_hauts_de_france", FloatType(), True),
        StructField("flux_physiques_de_nouvelle_aquitaine_vers_ile_de_france", FloatType(), True),
        StructField("flux_physiques_de_nouvelle_aquitaine_vers_normandie", FloatType(), True),
        StructField("flux_physiques_de_nouvelle_aquitaine_vers_nouvelle_aquitaine", FloatType(), True),
        StructField("flux_physiques_de_nouvelle_aquitaine_vers_occitanie", FloatType(), True),
        StructField("flux_physiques_de_nouvelle_aquitaine_vers_pays_de_la_loire", FloatType(), True),
        StructField("flux_physiques_de_nouvelle_aquitaine_vers_paca", FloatType(), True),
        StructField("flux_physiques_allemagne_vers_nouvelle_aquitaine", FloatType(), True),
        StructField("flux_physiques_belgique_vers_nouvelle_aquitaine", FloatType(), True),
        StructField("flux_physiques_espagne_vers_nouvelle_aquitaine", FloatType(), True),
        StructField("flux_physiques_italie_vers_nouvelle_aquitaine", FloatType(), True),
        StructField("flux_physiques_luxembourg_vers_nouvelle_aquitaine", FloatType(), True),
        StructField("flux_physiques_royaume_uni_vers_nouvelle_aquitaine", FloatType(), True),
        StructField("flux_physiques_suisse_vers_nouvelle_aquitaine", FloatType(), True),
        StructField("flux_physiques_de_nouvelle_aquitaine_vers_allemagne", FloatType(), True),
        StructField("flux_physiques_de_nouvelle_aquitaine_vers_belgique", FloatType(), True),
        StructField("flux_physiques_de_nouvelle_aquitaine_vers_espagne", FloatType(), True),
        StructField("flux_physiques_de_nouvelle_aquitaine_vers_italie", FloatType(), True),
        StructField("flux_physiques_de_nouvelle_aquitaine_vers_luxembourg", FloatType(), True),
        StructField("flux_physiques_de_nouvelle_aquitaine_vers_royaume_uni", FloatType(), True),
        StructField("flux_physiques_de_nouvelle_aquitaine_vers_suisse", FloatType(), True),
        StructField("tco_thermique", FloatType(), True),
        StructField("tch_thermique", FloatType(), True),
        StructField("tco_nucleaire", FloatType(), True),
        StructField("tch_nucleaire", FloatType(), True),
        StructField("tco_eolien", FloatType(), True),
        StructField("tch_eolien", FloatType(), True),
        StructField("tco_solaire", FloatType(), True),
        StructField("tch_solaire", FloatType(), True),
        StructField("tco_hydraulique", FloatType(), True),
        StructField("tch_hydraulique", FloatType(), True),
        StructField("tco_bioenergies", FloatType(), True),
        StructField("tch_bioenergies", FloatType(), True),
    ])

    # read Kafka stream
    df = (spark
          .readStream
          .format("kafka")
          .option("kafka.bootstrap.servers", IP_SERVER)
          .option("subscribe", TOPIC_NAME)
          .load()
          .withColumn("value", from_json(col("value").cast("string"), schema))
          .select(col('value.*'))
          )

    # remove not used columns
    df = df.drop(*('ech_physiques',
                   'stockage_batterie',
                   'destockage_batterie',
                   'eolien_terrestre',
                   'eolien_offshore',
                   'flux_physiques_d_auvergne_rhone_alpes_vers_nouvelle_aquitaine',
                   'flux_physiques_de_bourgogne_franche_comte_vers_nouvelle_aquitaine',
                   'flux_physiques_de_bretagne_vers_nouvelle_aquitaine',
                   'flux_physiques_de_centre_val_de_loire_vers_nouvelle_aquitaine',
                   'flux_physiques_de_grand_est_vers_nouvelle_aquitaine',
                   'flux_physiques_de_hauts_de_france_vers_nouvelle_aquitaine',
                   'flux_physiques_d_ile_de_france_vers_nouvelle_aquitaine',
                   'flux_physiques_de_normandie_vers_nouvelle_aquitaine',
                   'flux_physiques_de_nouvelle_aquitaine_vers_nouvelle_aquitaine',
                   'flux_physiques_d_occitanie_vers_nouvelle_aquitaine',
                   'flux_physiques_de_pays_de_la_loire_vers_nouvelle_aquitaine',
                   'flux_physiques_de_paca_vers_nouvelle_aquitaine',
                   'flux_physiques_de_nouvelle_aquitaine_vers_auvergne_rhone_alpes',
                   'flux_physiques_de_nouvelle_aquitaine_vers_bourgogne_franche_comte',
                   'flux_physiques_de_nouvelle_aquitaine_vers_bretagne',
                   'flux_physiques_de_nouvelle_aquitaine_vers_centre_val_de_loire',
                   'flux_physiques_de_nouvelle_aquitaine_vers_grand_est',
                   'flux_physiques_de_nouvelle_aquitaine_vers_hauts_de_france',
                   'flux_physiques_de_nouvelle_aquitaine_vers_ile_de_france',
                   'flux_physiques_de_nouvelle_aquitaine_vers_normandie',
                   'flux_physiques_de_nouvelle_aquitaine_vers_nouvelle_aquitaine',
                   'flux_physiques_de_nouvelle_aquitaine_vers_occitanie',
                   'flux_physiques_de_nouvelle_aquitaine_vers_pays_de_la_loire',
                   'flux_physiques_de_nouvelle_aquitaine_vers_paca',
                   'flux_physiques_allemagne_vers_nouvelle_aquitaine',
                   'flux_physiques_belgique_vers_nouvelle_aquitaine',
                   'flux_physiques_espagne_vers_nouvelle_aquitaine',
                   'flux_physiques_italie_vers_nouvelle_aquitaine',
                   'flux_physiques_luxembourg_vers_nouvelle_aquitaine',
                   'flux_physiques_royaume_uni_vers_nouvelle_aquitaine',
                   'flux_physiques_suisse_vers_nouvelle_aquitaine',
                   'flux_physiques_de_nouvelle_aquitaine_vers_allemagne',
                   'flux_physiques_de_nouvelle_aquitaine_vers_belgique',
                   'flux_physiques_de_nouvelle_aquitaine_vers_espagne',
                   'flux_physiques_de_nouvelle_aquitaine_vers_italie',
                   'flux_physiques_de_nouvelle_aquitaine_vers_luxembourg',
                   'flux_physiques_de_nouvelle_aquitaine_vers_royaume_uni',
                   'flux_physiques_de_nouvelle_aquitaine_vers_suisse'))

    # modifying na by 0
    df = df.na.fill(value=0)

    df = df.dropDuplicates()

    # create new variables related to production informations
    df = (df.withColumn("production", df.thermique + df.nucleaire + df.eolien
                        + df.solaire + df.pompage + df.bioenergies))

    df = df.withColumn("pct_thermique", (df.thermique / df.production) * 100)
    df = df.withColumn("pct_nucleaire", (df.nucleaire / df.production) * 100)
    df = df.withColumn("pct_eolien", (df.eolien / df.production) * 100)
    df = df.withColumn("pct_solaire", (df.solaire / df.production) * 100)
    df = df.withColumn("pct_pompage", (df.pompage / df.production) * 100)
    df = df.withColumn("pct_bioenergies", (df.bioenergies / df.production) * 100)

    # create variable to calculate difference between prod & consumption
    df = df.withColumn("diff", (df.consommation - df.production))

    # write into MongoDB
    query = (df
             .writeStream
             .foreach(WriteRowMongo())
             .start()
             .awaitTermination())
