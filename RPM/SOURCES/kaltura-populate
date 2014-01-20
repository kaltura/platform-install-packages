#!/bin/bash
. /etc/kaltura.d/system.ini

echo `date`

#
# populateMgr		This shell script takes care of starting and stopping a Kaltura Sphinx Populate Service
#
# chkconfig: 2345 13 87
# description: Kaltura Sphinx Populate

# Source function library.
#. /etc/rc.d/init.d/functions

# Directory containing the populate php files 
SCRIPTDIR=$APP_DIR/plugins/sphinx_search/scripts

SCRIPTEXE=populateFromLog.php

if [ $# -ne 1 ]; then
	echo "Usage: $0 [start|stop|restart|status]"
	exit 1 	
fi

LOCKFILE="$LOG_DIR/populate.pid"

echo_success() {
	[ "$BOOTUP" = "color" ] && $MOVE_TO_COL
	echo -n "["
	[ "$BOOTUP" = "color" ] && $SETCOLOR_SUCCESS
	echo -n $"	OK	"
	[ "$BOOTUP" = "color" ] && $SETCOLOR_NORMAL
	echo -n "]"
	echo -ne "\r"
	return 0
}

echo_failure() {
	[ "$BOOTUP" = "color" ] && $MOVE_TO_COL
	echo -n "["
	[ "$BOOTUP" = "color" ] && $SETCOLOR_FAILURE
	echo -n $"FAILED"
	[ "$BOOTUP" = "color" ] && $SETCOLOR_NORMAL
	echo -n "]"
	echo -ne "\r"
	return 0
}


start() {
	if [ -f $BASE_DIR/maintenance ]; then
		echo "Server is on maintenance mode - populateMgr will not start!"
		exit 1
	fi
	
	echo -n $"Starting:"
	KP=$(pgrep -P 1 -f $SCRIPTEXE)
	if ! kill -0 `cat $LOCKFILE 2>/dev/null` 2>/dev/null; then 
		echo_failure
		echo
		if [ "X$KP" != "X" ]; then
			echo "Service populate already running"
			return 0
		else
			echo "Service populate isn't running but stale lock file exists"
			echo "Removing stale lock file at $LOCKFILE"
			rm -f $LOCKFILE
			start_scheduler
			return 0
		fi
	else
		if [ "X$KP" != "X" ]; then
			echo "Populate is running as $KP without a $LOCKFILE"
			exit 0
		fi		
		start_scheduler
		return 0
	fi
}

start_scheduler() {
	echo "$PHP_BIN $SCRIPTEXE >> $LOG_DIR/kaltura_populate.log 2>&1 &"
	cd $SCRIPTDIR
	su $OS_KALTURA_USER -c "$PHP_BIN $SCRIPTEXE >> $LOG_DIR/kaltura_populate.log 2>&1 &"
	if [ "$?" -eq 0 ]; then
		echo_success
		echo
	else
		echo_failure
		echo
	fi
}

show_status() {
	KP=$(pgrep -P 1 -f $SCRIPTEXE) 
	if [ "X$KP" != "X" ]; then
	echo "Populate is running as $KP ..."
	return 0
	else
		echo "Service populate isn't running"
		return 3
	fi
}

stop() {
	echo -n $"Shutting down:"
	KP=`pgrep -P 1 -f $SCRIPTEXE|xargs`
	if [ -n "$KP" ]; then
		# hack, returnds the PIDS as string and tells kill to kill all at once
		for pid in "$KP"
		do
			kill -9 $pid
		done
		echo_success
		echo
		RC=0
	else
		echo_failure
		echo
		echo "Service populate not running"
		RC=0
	fi
	rm -f $LOCKFILE
	return $RC
}

case "$1" in
	start)
		start
		;;
	stop)
		stop
		;;
	status)
		show_status
		;;
	restart)
		stop
		start
		;;
	*)
		echo "Usage: [start|stop|restart|status]"
		exit 0
		;;
esac
exit 0

