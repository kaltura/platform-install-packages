#!/bin/sh

NAME="live-analytics-driver"
SPARK_MASTER_HOST=@SPARK_MASTER_HOST@
SPARK_MASTER_PORT=@SPARK_MASTER_PORT@
SPARK_DEFAULT_PARALLELISM=2
SPARK_CORES_MAX=1
SPARK_MEMORY=2g
PID_FILE="/opt/kaltura/var/run/live-analytics-driver/$NAME.pid"
nodetool enablethrift

. /etc/rc.d/init.d/functions
case "$1" in
    start)
        if [ -r "$PID_FILE" ];then
                PID=`cat $PID_FILE`
        fi
        if kill -0 $PID 2>/dev/null;then
                echo "$NAME is already running ($PID)"
                exit 0
        fi
        echo -n "Starting $NAME: "
        nohup /opt/spark-1.2.2-bin-hadoop2.4/bin/spark-submit --class com.kaltura.Live.MainDriver --master local[2] --driver-class-path "/opt/kaltura/lib/*" --conf spark.driver.memory=$SPARK_MEMORY --conf spark.default.parallelism=$SPARK_DEFAULT_PARALLELISM /opt/kaltura/lib/live-analytics-driver.jar >> /opt/kaltura/log/$NAME.log 2>&1 &
        PID="$!"
        retval=$?
        if [ $retval -eq 0 ] ;then echo "$PID" > $PID_FILE;fi
        echo "OK ($PID)"
        ;;
    stop)
        echo -n "Shutdown $NAME: "
        if [ -r "$PID_FILE" ];then
                PID=`cat $PID_FILE`
        fi
        kill "$PID" 2>/dev/null
        retval=$?
        if [ $retval -eq 0 ] ;then rm -f $PID_FILE;fi
        for t in `seq 40`; do $0 status > /dev/null 2>&1 && sleep 0.5 || break; done
        STATUS=`$0 status -p $PID_FILE`
        if [[ $STATUS == "$NAME is stopped" ]]; then
            echo "OK"
        else
            echo "ERROR: could not stop $NAME:  $STATUS"
            exit 1
        fi
        ;;
    reload|restart)
        $0 stop
        $0 start
        ;;
    status)
        status -p $PID_FILE "$NAME"
        exit $?
        ;;
    *)
        echo "Usage: `basename $0` start|stop|status|restart|reload"
        exit 1
esac
