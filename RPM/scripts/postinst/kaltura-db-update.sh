#!/bin/bash - 
#===============================================================================
#          FILE: kaltura-db-update.sh
#         USAGE: ./kaltura-db-update.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: David Bezemer, <themmai@gmail.com>
#  ORGANIZATION: Learnlab
#       CREATED: 03/02/14 16:22:40 EST
#      REVISION:  ---
#===============================================================================
#set -o nounset                              # Treat unset variables as an error

RC=0

if [ -r "/opt/kaltura/app/configurations/system.ini" -a -r /opt/kaltura/app/deployment/sql_updates ];then
		. /opt/kaltura/app/configurations/system.ini
		for SQL in `cat $APP_DIR/deployment/sql_updates`;do
		# if we have the .done file, then some updates already happened
		# need to check if our current one is in the done list, if so, skip it.
				if [ -r  $APP_DIR/deployment/sql_updates.done ];then
						if grep -q $SQL $APP_DIR/deployment/sql_updates.done;then
								continue
						fi
				fi
				if [ -z "$DB_PORT" ];then
					DB1_PORT=3306
				fi
				OUT="$OUT || `mysql kaltura -h $DB1_HOST -u $DB1_USER -P $DB1_PORT -p$DB1_PASS < $SQL  2>&1`"
				RC=$?
		done
		if [ $RC -eq 0 ];then
				cat $APP_DIR/deployment/sql_updates >> $APP_DIR/deployment/sql_updates.done
				rm $APP_DIR/deployment/sql_updates
		fi
fi

if [ -f $APP_DIR/deployment/sql_updates ];then
	echo "Error occurred during DB update:
	$OUT
	"
else
	echo "Manual DB updates finished with RC $RC"
fi
