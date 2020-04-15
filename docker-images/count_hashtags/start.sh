#!/bin/bash
/usr/local/bin/spark-submit \
--packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.5,datastax:spark-cassandra-connector:2.4.0-s_2.11 \
--conf spark.cassandra.connection.host=tweets-db-cassandra \
--conf spark.cassandra.auth.username=admin \
--conf spark.cassandra.auth.password=tweets \
/home/app/count_hashtags.py
