#!/bin/bash -e 
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
	echo "base-config completed successfully, if you ever want to re-configure your system (e.g. change DB hostname) run the following script:
# rm /opt/kaltura/app/base-config.lock
# $BASE_DIR/bin/kaltura-base-config.sh
"
fi
ln -sf $APP_DIR/configurations/cron/dwh /etc/cron.d/kaltura-dwh
echo "DWH configured."
