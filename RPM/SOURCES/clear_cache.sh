#!/bin/bash
. /etc/kaltura.d/system.ini

echo `date`

# Store PID of script:
# Match script without arguments
LCK_FILE=/tmp/`basename $0`.lck

if [ -f "${LCK_FILE}" ]; then

  # The file exists so read the PID
  # to see if it is still running
  MYPID=`head -n 1 $LCK_FILE`

  if [ -n "`ps -p ${MYPID} | grep ${MYPID}`" ]; then
    echo `basename $0` is already running [$MYPID].
    exit
  fi
fi

# Echo current PID into lock file
echo $$ > $LCK_FILE



if [ -d "/tmp/cache_v3-600" ];then
	echo "`date +%s` start clean v3 `date`" >> $LOG_DIR/clear_cache.log
	/usr/bin/ionice -c3 find /tmp/cache_v3-600 -type f -mmin +1440 -name "cache*" -delete
fi
if [ -d "/tmp/cache_v2" ];then
echo "`date +%s` end clean v2 `date`" >> $LOG_DIR/clear_cache.log
	/usr/bin/ionice -c3 find /tmp/cache_v2 -type f -mmin +1440 -name "cache*" -delete
fi
echo "`date +%s` end clean v2 `date`" >> $LOG_DIR/clear_cache.log
/usr/bin/ionice -c3 find /tmp -maxdepth 1 -type f -mmin +1440 -name "php*" -delete
echo "`date +%s` end clean php `date`" >> $LOG_DIR/clear_cache.log
