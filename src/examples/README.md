# Spark Streaming Tutorial

Steps to build spark from source 

```
git clone https://github.com/apache/spark
cd spark
build/mvn -DskipTests clean package

# Run an example
./bin/run-example SparkPi

# Install Pyspark
cd python; python3.6 setup.py sdist
```

Steps to install in python

```
conda install -c conda-forge pyspark
```

Before running the examples run below

```
./simulation.py |nc -lk 9999
```

Examples we cover in this folder
- [Basics](https://git.zoi.de/krishna.kalyan/experiments/blob/master/spark-streaming/01_basics.py)
- [Data Frames](https://git.zoi.de/krishna.kalyan/experiments/blob/master/spark-streaming/02_df.py)
- [Aggregation](https://git.zoi.de/krishna.kalyan/experiments/blob/master/spark-streaming/03_agg.py)
- [Windowing, Sliding interval and Watermarking](https://git.zoi.de/krishna.kalyan/experiments/blob/master/spark-streaming/04_iot_running_count.py)
- [Joins](https://git.zoi.de/krishna.kalyan/experiments/blob/master/spark-streaming/05_joins.py)
- [Checkpoints](https://git.zoi.de/krishna.kalyan/experiments/blob/master/spark-streaming/06_checkpoint.py)
