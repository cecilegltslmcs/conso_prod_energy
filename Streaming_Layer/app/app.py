from pyspark.sql import functions as F
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
#from pyspark.sql.types import StringType, StructType, StructField, FloatType, IntegerType
#import time

ip_server = "localhost:9092"
topic_name = "electricity_production"

if __name__ == "__main__":

    # initialize sparkSession & sparkContext
    spark = (SparkSession
        .builder
        .appName("electricityProduction")
        .getOrCreate())
    sc = spark.sparkContext.setLogLevel("ERROR")

    # read Kafka stream
    df = (spark
        .readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", ip_server)
        .option("subscribe", topic_name)
        .load()
        )

    
    
    query = (df
            .writeStream
            .queryName("tests_prod_electricite")
            .outputMode("append")
            .format("console")
            .start()
            .awaitTermination())