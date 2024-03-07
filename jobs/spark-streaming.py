from time import sleep
import openai
from config.config import config
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, when
from pyspark.sql.functions import udf
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType, StringType, IntegerType


def get_sentiment_freq(text) -> str:
    if text:
        openai.api_key = config["openai"]["api_key"]
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": {text},
                },
            ]
        )
        return chat.choices[0].message["content"]
    return "Empty"


def start_spark_stream(spark):
    topic = "review"
    while True:
        try:
            stream_df = spark.readStream.format("socket").option("host", "0.0.0.0").option("port", 9999).load()

            schema = StructType([
                StructField("Sno", IntegerType()),
                StructField("book_name", StringType()),
                StructField("review_title", StringType()),
                StructField("reviewer", StringType()),
                StructField("review_rating", IntegerType()),
                StructField("reviewer_description", StringType())
            ])

            stream_df = stream_df.select(from_json(col("value"), schema).alias("data")).select("data.*")

            sentiment_udf = udf(get_sentiment_freq, StringType())
            stream_df = stream_df.withColumn("review", when(col("reviewer_description").isNotNull(),
                                                            sentiment_udf(col("reviewer_description"))).otherwise(None))

            kafka_df = stream_df.selectExpr("CAST(book_name as STRING) AS key", "to_json(struct(*)) AS value")

            query = (kafka_df.writeStream
                     .format("kafka")
                     .option("kafka.bootstrap.servers", config["kafka"]["bootstrap.servers"])
                     .option("kafka.security.protocol", config["kafka"]["security.protocol"])
                     .option("kafka.sasl.mechanism", config["kafka"]["sasl.mechanisms"])
                     .option("kafka.sasl.jaas.config",
                             'org.apache.kafka.common.security.plain.PlainLoginModule required username="{username}" '
                             'password="{password}";'.format(
                                 username=config["kafka"]["sasl.username"],
                                 password=config["kafka"]["sasl.password"]))
                     .option('checkpointLocation', '/tmp/checkpoint')
                     .option("topic", topic)
                     .start()
                     .awaitTermination())

        except Exception as e:
            print(f"Error Occurred: {e}. Retrying in 10 seconds.")
            sleep(10)


if __name__ == "__main__":
    # Create Spark session
    spark_conn = SparkSession.builder.appName("SentimentAnalysisETL").getOrCreate()

    # Start the Spark Streaming job
    start_spark_stream(spark_conn)
