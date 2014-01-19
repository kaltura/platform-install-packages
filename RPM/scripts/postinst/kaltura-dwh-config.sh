#!/bin/bash - 
#===============================================================================
#          FILE: kaltura-dwh-config.sh
#         USAGE: ./kaltura-dwh-config.sh 
#   DESCRIPTION: configure the server as a DWH node. 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy (), <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 01/02/14 09:25:54 EST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error

if [ ! -r /opt/kaltura/app/base-config.lock ];then
	`dirname $0`/kaltura-base-config.sh
else
	echo "base-config skipped as /opt/kaltura/app/base-config.lock was found. Remove the lock to reconfigure."
fi
ln -sf $APP_DIR/configurations/cron/dwh /etc/cron.d/kaltura-dwh
