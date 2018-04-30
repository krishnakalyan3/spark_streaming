from pyspark.sql import SparkSession
from pyspark.sql.types import StructType
from pyspark.sql.types import IntegerType, StringType, TimestampType
from pyspark.sql.types import StructField
from pyspark.sql import functions as F
from pyspark.sql.functions import split


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
        (split(lines.value, ' ')).getItem(3).cast('double').alias("battery"),
        lines.timestamp
    )

    # Select
    df_select = data_frame.select(data_frame.time, data_frame.temp)

    # Filter
    df_filter = df_select.filter(df_select.temp < 0)

    # Use this with watermark
    # Group
    #df_group = df_select.groupBy(df_filter.time).sum()

    query = df_filter.writeStream \
        .outputMode('append') \
        .format('console') \
        .start()

    query.awaitTermination()

# $SPARK_HOME/bin/spark-submit 03_agg.py
