from pyspark.sql import SparkSession
from pyspark.sql.types import *
import pyspark.sql.functions as f


def getSchema(spark, file):
    schema = spark.read \
        .option("multiline", "true") \
        .json(file) \
        .schema
    return schema


def readKafkaStream(spark, schema, bootstrap, topic):
    kafkaDf = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", bootstrap) \
        .option("subscribe", topic) \
        .load() \
        .select(f.from_json(f.col("value").cast("string"),schema).alias("data")) \
        .filter(f.col("data.lang").isin(['ja','ar','ko','th','ur','und','zh','in','tr','tl','hi']) == False)
    return kafkaDf


def extractDf(df):
    expr = ">(.*?)<"
    extractDf = df \
        .withColumn("src", f.regexp_extract(f.col("data.source"), expr, 1)) \
        .select(f.col("data.id").alias("twtid"),
                f.col("data.timestamp_ms").alias("twttimestamp"),
                f.col("data.lang").alias("twtlang"),
                f.col("src").alias("twtsource"), 
                f.explode("data.entities.hashtags").alias("hashtags")
            )
    return extractDf


def flattenDf(df):
    ht_schema  = StructType(
            [
                StructField('text', StringType(), True),
                StructField('indices', StringType(), True)
            ]
        )
    flatDf = df \
        .withColumn("ht", f.from_json("hashtags", ht_schema)) \
        .withColumn("twtdate", f.from_unixtime(f.col("twttimestamp").substr(1,10), format='yyyy-MM-dd')) \
        .drop("hashtags") \
        .select(f.col("twtid"),
            f.col("twtdate"),
            f.col("twtlang"),
            f.col("twtsource"),
            f.col("ht.text").alias("twthashtag")
            )
    return flatDf


def aggregateDf(df):
    aggDf = df \
        .groupby('twtlang', 'twtdate', 'twtsource','twthashtag') \
        .agg(f.count('twtid').alias('twtcount'))
    return aggDf


def writeCassandra(writeDf, epochId):
    writeDf.write \
        .format("org.apache.spark.sql.cassandra") \
        .options(table="ht_count", keyspace="tweets_ks") \
        .mode("append") \
        .save()


def runQuery(df):
    query = df.writeStream \
        .outputMode("update") \
        .foreachBatch(writeCassandra) \
        .start()
    
    query.awaitTermination()
    query.stop()


def main():
    spark = SparkSession.builder.getOrCreate()
    schema = getSchema(spark, "/home/app/sample_tweet.json")
    kafkaDf = readKafkaStream(spark, schema, "tweets-kafka:9092", "tweets")
    aggDf = aggregateDf(flattenDf(extractDf(kafkaDf)))
    runQuery(aggDf)



if __name__ == "__main__":
    main()
