import authentification as auth
import pymongo
from pyspark.sql import functions as F
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StringType, StructType, StructField, FloatType, IntegerType, DateType, TimestampType
import time


time.sleep(10)

ip_server = "localhost:9092"
topic_name = "electricity_production"
user = auth.mongodb_user
password = auth.mongodb_password
uri = f"mongodb://{user}:{password}@mongo:27017"

class WriteRowMongo:
    def open(self, partition_id, epoch_id):
        self.myclient = pymongo.MongoClient(uri)
        self.mydb = self.myclient["electricity_prod"]
        self.mycol = self.mydb["streaming_data"]
        return True

    def process(self, row):
        self.mycol.insert_one(row.asDict())

    def close(self, error):
        self.myclient.close()
        return True

if __name__ == "__main__":

    # initialize sparkSession & sparkContext
    spark = (SparkSession
        .builder
        .master('spark://spark:7077')
        .config("spark.mongodb.input.uri", uri)
        .config("spark.mongodb.output.uri", uri)
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2")
        .appName("electricity_prod_conso")
        .getOrCreate())
    sc = spark.sparkContext.setLogLevel("ERROR")

    # Schema definition & data selection
    schema = StructType([
        StructField("code_insee_region", StringType(), True),
        StructField("libelle_region", StringType(), True),
        StructField("nature", StringType(), True),
        #StructField("date", DateType(), True),
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
        .option("kafka.bootstrap.servers", ip_server)
        .option("subscribe", topic_name)
        .load()
        .withColumn("value", from_json(col("value").cast("string"), schema))
        .select(col('value.*'))
        )

    # query = (df
    #         .writeStream
    #         .queryName("tests_prod_electricite")
    #         .outputMode("append")
    #         .format("console")
    #         .start()
    #         .awaitTermination())
    
    query = (df
            .writeStream
            .foreach(WriteRowMongo())
            .start()
            .awaitTermination())
