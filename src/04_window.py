from pyspark.sql import SparkSession
from pyspark.sql.types import StructType
from pyspark.sql.types import IntegerType, StringType, TimestampType
from pyspark.sql.types import StructField
from pyspark.sql import functions as F
from pyspark.sql.functions import split
from pyspark.sql.functions import window


if __name__ == "__main__":
    spark = SparkSession\
        .builder\
        .appName("StructuredNetworkWordCountWindowed")\
        .getOrCreate()

    # Create DataFrame representing the stream of input lines from connection to host:port
    lines = spark\
        .readStream \
        .format('socket')\
        .option('host', 'localhost')\
        .option('port', 9999)\
        .option('includeTimestamp', 'true')\
        .load()

    data_frame = lines.select(
        (split(lines.value, ' ')).getItem(0).cast('integer').alias("time"),
        (split(lines.value, ' ')).getItem(1).cast('double').alias("moisture"),
        (split(lines.value, ' ')).getItem(2).cast('float').alias("temp"),
        (split(lines.value, ' ')).getItem(3).cast('float').alias("battery"),
        lines.timestamp
    )

    # Window
    df_window1 = data_frame \
        .groupBy(
         window(data_frame.timestamp, "30 second", "15 second"),
         data_frame.time,
         data_frame.temp
        ).count()

    # Watermark
    df_window = data_frame \
        .withWatermark("timestamp", "1 minutes") \
        .groupBy(data_frame.time).agg({'temp': 'avg'})

    query = df_window.writeStream \
        .outputMode('complete') \
        .format('console') \
        .start()

    query.awaitTermination()

# $SPARK_HOME/bin/spark-submit 04_window.py
