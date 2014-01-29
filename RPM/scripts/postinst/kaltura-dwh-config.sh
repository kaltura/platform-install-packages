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
RC_FILE=/etc/kaltura.d/system.ini
if [ ! -r "$RC_FILE" ];then
	echo "Could not find $RC_FILE so, exiting.."
	exit 2
fi
. $RC_FILE
TABLES=`echo "show tables" | mysql -h$DWH_HOST -u$SUPER_USER -p$SUPER_USER_PASSWD -P$DWH_PORT kalturadw 2> /dev/null`
if [ -z "$TABLES" ];then 
	echo "Deploying analytics warehouse DB, please be patient as this may take a while..."
	/opt/kaltura/dwh/setup/dwh_setup.sh -u$SUPER_USER -k /opt/kaltura/pentaho/pdi/ -d/opt/kaltura/dwh -h$DWH_HOST -P$DWH_PORT -p$SUPER_USER_PASSWD
else
cat << EOF
The Kaltura DWH DB seems to already be installed.
DB creation will be skipped.
EOF
fi
sed  's#\(@DWH_DIR@\)$#\1 -k /opt/kaltura/pentaho/pdi/kitchen.sh#g' $APP_DIR/configurations/cron/dwh.template >$APP_DIR/configurations/cron/dwh
sed -i -e "s#@DWH_DIR@#$BASE_DIR/dwh#g" -e "s#@APP_DIR@#$APP_DIR#g" -e "s#@LOG_DIR@#$LOG_DIR#g" $APP_DIR/configurations/cron/dwh
ln -sf $APP_DIR/configurations/cron/dwh /etc/cron.d/kaltura-dwh
echo "DWH configured."
