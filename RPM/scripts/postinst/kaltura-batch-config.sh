#!/bin/bash - 
#===============================================================================
#          FILE: kaltura-batch-config.sh
#         USAGE: ./kaltura-batch-config.sh 
#   DESCRIPTION: configure server as a batch node.
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 01/02/14 09:23:34 EST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error
KALTURA_FUNCTIONS_RC=`dirname $0`/kaltura-functions.rc
if [ ! -r "$KALTURA_FUNCTIONS_RC" ];then
	OUT="ERROR: Could not find $KALTURA_FUNCTIONS_RC so, exiting.."
	echo -e $OUT
	exit 3
fi
. $KALTURA_FUNCTIONS_RC
if ! rpm -q kaltura-batch;then
	echo -e "${BRIGHT_BLUE}Skipping as kaltura-batch is not installed.${NORMAL}"
	exit 0 
fi
if [ -r $CONSENT_FILE ];then
	. $CONSENT_FILE
elif [ -z "$USER_CONSENT" ];then
	get_tracking_consent
fi
. $CONSENT_FILE
if [ -n "$1" -a -r "$1" ];then
	ANSFILE=$1
	. $ANSFILE
fi
if [ ! -r /opt/kaltura/app/base-config.lock ];then
	`dirname $0`/kaltura-base-config.sh "$ANSFILE"
else
	echo -e "${BRIGHT_BLUE}base-config completed successfully, if you ever want to re-configure your system (e.g. change DB hostname) run the following script:
# rm /opt/kaltura/app/base-config.lock
# $BASE_DIR/bin/kaltura-base-config.sh
${NORMAL}
"
fi
trap 'my_trap_handler "${LINENO}" ${$?}' ERR
send_install_becon `basename $0` $ZONE install_start 0 
CONFIG_DIR=/opt/kaltura/app/configurations
if [ -r $CONFIG_DIR/system.ini ];then
	. $CONFIG_DIR/system.ini
else
	echo -e "${BRIGHT_RED}ERROR: Missing $CONFIG_DIR/system.ini. Exiting..${NORMAL}"
	exit 1
fi

BATCH_SCHED_CONF=$APP_DIR/configurations/batch/scheduler.conf
BATCH_MAIN_CONF=$APP_DIR/configurations/batch/batch.ini

# if we couldn't access the DB to retrieve the secret, assume the post install has not finished yet.
BATCH_PARTNER_ADMIN_SECRET=`echo "select admin_secret from partner where id=-1"|mysql -N -h$DB1_HOST -u$DB1_USER -p$DB1_PASS $DB1_NAME -P$DB1_PORT`
if [ -z "$BATCH_PARTNER_ADMIN_SECRET" ];then
	echo -e "${BRIGHT_RED}ERROR: could not retreive partner.admin_secret for id -1. It probably means you did not yet run $APP_DIR/kaltura-base-config.sh yet. Please do.${NORMAL}" 
	exit 2
fi

sed -i "s#@BATCH_PARTNER_ADMIN_SECRET@#$BATCH_PARTNER_ADMIN_SECRET#" -i $BATCH_MAIN_CONF
sed -i "s#@INSTALLED_HOSNAME@#`hostname`#" -i $BATCH_MAIN_CONF

BATCH_SCHEDULER_ID=`< /dev/urandom tr -dc 0-9 | head -c5`
sed "s#@BATCH_SCHEDULER_ID@#$BATCH_SCHEDULER_ID#"  -i $BATCH_MAIN_CONF 
sed "s#@INSTALLED_HOSNAME@#`hostname`#g" -i  -i $BATCH_MAIN_CONF

# logrotate:
ln -sf $APP_DIR/configurations/logrotate/kaltura_batch /etc/logrotate.d/ 
ln -sf $APP_DIR/configurations/logrotate/kaltura_apache /etc/logrotate.d/
ln -sf $APP_DIR/configurations/logrotate/kaltura_apps /etc/logrotate.d/
ln -sf $APP_DIR/configurations/apache/kaltura.conf /etc/httpd/conf.d/zzzkaltura.conf

mkdir -p $LOG_DIR/batch 
rm -rf $BASE_DIR/app/cache/*
find $BASE_DIR/log -type d -exec chmod 775 {} \; 
find $BASE_DIR/log -type f -exec chmod 664 {} \; 
chown -R kaltura.apache $BASE_DIR/app/cache/ $BASE_DIR/log

chkconfig httpd on
if service httpd status >/dev/null 2>&1;then
	service httpd reload
else
	service httpd start
fi

/etc/init.d/kaltura-batch restart >/dev/null 2>&1
ln -sf $BASE_DIR/app/configurations/monit/monit.avail/batch.rc $BASE_DIR/app/configurations/monit/monit.d/enabled.batch.rc
ln -sf $BASE_DIR/app/configurations/monit/monit.avail/httpd.rc $BASE_DIR/app/configurations/monit/monit.d/enabled.httpd.rc
/etc/init.d/kaltura-monit stop >> /dev/null 2>&1
/etc/init.d/kaltura-monit start
send_install_becon `basename $0` $ZONE install_success 0 
