#!/bin/bash

SPARK_MASTER_HOST=@SPARK_MASTER_HOST@
SPARK_MASTER_PORT=@SPARK_MASTER_PORT@
JARFILENAME="live-analytics-driver"
SPARK_DEFAULT_PARALLELISM=2
SPARK_CORES_MAX=1

nohup java -cp :/opt/kaltura/lib/*:/opt/spark-1.2.2-bin-hadoop2.4/conf:/opt/spark-1.2.2-bin-hadoop2.4/lib/spark-assembly-1.2.2-hadoop2.4.0.jar -Xms512m -Xmx512m org.apache.spark.deploy.SparkSubmit --class com.kaltura.Live.MainDriver --master local[2] --driver-class-path /opt/kaltura/lib/* --conf spark.driver.memory=2g --conf spark.default.parallelism=2 /opt/kaltura/lib/live-analytics-driver.jar >> /opt/kaltura/log/$JARFILENAME.log 2>&1 &

#nohup spark-submit --class com.kaltura.Live.MainDriver --master local[2] --deploy-mode cluster --driver-class-path "/opt/kaltura/lib/*" --conf spark.default.parallelism=${SPARK_DEFAULT_PARALLELISM} --conf spark.cores.max=${SPARK_CORES_MAX} --supervise   /opt/kaltura/lib/${JARFILENAME}.jar
#echo $$ > /opt/kaltura/var/run/$JARFILENAME.pid
