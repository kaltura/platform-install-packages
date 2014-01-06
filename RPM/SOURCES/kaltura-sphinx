#!/bin/sh
#
# sphinx searchd Free open-source SQL full-text search engine
#
# chkconfig:   - 20 80
# description: Starts and stops the sphinx searchd daemon that handles all search requests.

### BEGIN INIT INFO
# Provides: searchd
# Required-Start: $local_fs $network
# Required-Stop: $local_fs $network
# Default-Start:
# Default-Stop: 0 1 2 3 4 5 6
# Short-Description: start and stop sphinx searchd daemon
# Description: Sphinx is a free open-source SQL full-text search engine	 
### END INIT INFO

. /etc/kaltura.d/system.ini

# Source function library.
. $APP_DIR/infra/scripts/functions.rc
prog="searchd"
config="$APP_DIR/configurations/sphinx/kaltura.conf"
exec="$BASE_DIR/bin/sphinx/searchd"
pid_file="/opt/kaltura/sphinx/searchd.pid"


start() {
 	[ -x $exec ] || exit 5
 	[ -f $config ] || exit 6
 	echo -n $"Starting $prog: "
 	# if not running, start it up here, usually something like "daemon $exec"
 	su $OS_KALTURA_USER -c "$exec --config $config"
 	retval=$?
 	echo
 	return $retval
}

stop() {
 	echo -n $"Stopping $prog: "
 	# stop it here, often "killproc $prog"
 	$exec --config $config --stopwait
 	retval=$?
 	echo
 	[ $retval -eq 0 ]
 	return $retval
}

force_stop() {
 	echo -n $"Brute stopping $prog: "
 	# stop it here, often "killproc $prog"
 	#$exec --config $config --stopwait
 	PID=`cat $pid_file 2>/dev/null`
 	if kill -0 $PID 2> /dev/null;then
 		kill -9 $PID
 	fi
 	retval=$?
 	echo
 	[ $retval -eq 0 ]
 	return $retval
}

restart() {
 	stop
 	start
}

reload() {
 	restart
}

force_reload() {
 	restart
}

rh_status() {
 	# run checks to determine if the service is running or use generic status
 	status $prog
}

rh_status_q() {
 	rh_status >/dev/null 2>&1
}


case "$1" in
 	start)
 		rh_status_q && exit 0
 		$1
 		;;
 	stop)
 		rh_status_q || exit 0
 		$1
 		;;
 	force-stop)
 		rh_status_q || exit 0
 		force_stop
 		;;
 	restart)
 		$1
 		;;
 	reload)
 		rh_status_q || exit 7
 		$1
 		;;
 	force-reload)
 		force_reload
 		;;
 	status)
 		rh_status
 		;;
 	condrestart|try-restart)
 		rh_status_q || exit 0
 		restart
 		;;
 	*)
 		echo $"Usage: $0 {start|stop|force-stop|status|restart|condrestart|try-restart|reload|force-reload}"
 		exit 2
esac
exit $?
