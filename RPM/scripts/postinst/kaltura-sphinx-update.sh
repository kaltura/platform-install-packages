#!/bin/bash - 
#===============================================================================
#          FILE: sphinx_update.sh
#         USAGE: ./sphinx_update.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy (), <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 11/10/14 12:37:31 EST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error

KALTURA_FUNCTIONS_RC=`dirname $0`/kaltura-functions.rc
if [ ! -r "$KALTURA_FUNCTIONS_RC" ];then
	OUT="Could not find $KALTURA_FUNCTIONS_RC so, exiting.."
	echo $OUT
	exit 3
fi
. $KALTURA_FUNCTIONS_RC
RC_FILE=/etc/kaltura.d/system.ini
if [ ! -r "$RC_FILE" ];then
	echo -e "${BRIGHT_RED}ERROR: could not find $RC_FILE so, exiting..${NORMAL}"
	exit 1 
fi
. $RC_FILE
if [ -r $APP_DIR/configurations/sphinx_conf_changed ];then
	if /etc/init.d/kaltura-sphinx status;then
		# disable Sphinx's monit monitoring
		rm $APP_DIR/configurations/monit/monit.d/enabled.sphinx.rc 
		/etc/init.d/kaltura-sphinx stop
	fi
	rm $BASE_DIR/sphinx/kaltura_*  $LOG_DIR/sphinx/data/binlog.*
	/etc/init.d/kaltura-sphinx start
	php $APP_DIR/deployment/base/scripts/populateSphinxEntries.php
	if [ $? -ne 0 ];then

		echo "Failed to run $APP_DIR/deployment/base/scripts/populateSphinxEntries.php.
	Please try to run it manually and look at the logs"
	fi
	rm $APP_DIR/configurations/sphinx_conf_changed
fi
