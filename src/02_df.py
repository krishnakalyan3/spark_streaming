from pyspark.sql import SparkSession
from pyspark.sql.types import StructType
from pyspark.sql.types import IntegerType, StringType, TimestampType
from pyspark.sql.types import StructField
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
        (split(lines.value, ' ')).getItem(0).alias("time"),
        (split(lines.value, ' ')).getItem(1).alias("moisture"),
        (split(lines.value, ' ')).getItem(2).alias("temp"),
        (split(lines.value, ' ')).getItem(3).alias("battery"),
        lines.timestamp
    )

    data_frame = data_frame.writeStream \
        .outputMode('append') \
        .format('console') \
        .start()

    data_frame.awaitTermination()

# $SPARK_HOME/bin/spark-submit 05_dataframe.py
