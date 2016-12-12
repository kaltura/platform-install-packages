#!/bin/bash

SPARK_MASTER_HOST=@SPARK_MASTER_HOST@
SPARK_MASTER_PORT=@SPARK_MASTER_PORT@
JARFILENAME="live-analytics-driver"
SPARK_DEFAULT_PARALLELISM=2
SPARK_CORES_MAX=1

nohup spark-submit --class com.kaltura.Live.MainDriver --master local[2] --deploy-mode cluster --driver-class-path "/opt/kaltura/lib/*" --conf spark.default.parallelism=${SPARK_DEFAULT_PARALLELISM} --conf spark.cores.max=${SPARK_CORES_MAX} --supervise   /opt/kaltura/lib/${JARFILENAME}.jar
echo $$ > /opt/kaltura/var/run/$JARFILENAME.pid
