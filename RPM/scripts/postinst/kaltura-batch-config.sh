#!/bin/bash - 
#===============================================================================
#          FILE: kaltura-batch-config.sh
#         USAGE: ./kaltura-batch-config.sh 
#   DESCRIPTION: configure server as a batch node.
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 01/02/14 09:23:34 EST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error
verify_user_input()
{
        ANSFILE=$1
	. $ANSFILE
        for VAL in SERVICE_URL ; do
                if [ -z "${!VAL}" ];then
                        echo "I need $VAL in $ANSFILE."
                        exit 1
                fi
        done
}

KALTURA_RC=/etc/kaltura.d/system.ini
if [ ! -r $KALTURA_RC ];then
	echo "Couldn't find $KALTURA_RC."
	exit 1
fi

BATCH_SCHED_CONF=/opt/kaltura/app/configurations/batch/scheduler.conf
BATCH_MAIN_CONF=/opt/kaltura/app/configurations/batch/batch.ini

# if we couldn't access the DB to retrieve the secret, assume the post install has not finished yet.
BATCH_PARTNER_ADMIN_SECRET=`echo "select admin_secret from partner where id=-1"|mysql -N -h$DB1_HOST -u$DB1_USER -p$DB1_PASS $DB1_NAME`
if [ -z "$BATCH_PARTNER_ADMIN_SECRET" ];then
	echo "Could not retreive partner.admin_secret for id -1. It probably means you did not yet run $APP_DIR/kaltura-base-config.sh yet. Please do." 
	exit 2
fi

if [ -n "$1" -a -r "$1" ];then
        ANSFILE=$1
        verify_user_input $ANSFILE
else

        echo "Welcome to Kaltura Server `rpm -qa kaltura-batch --queryformat %{version}` post install setup.
In order to finalize the batch configuration, please input the following:"
        while [ -z "$SERVICE_URL" ];do
                echo "Service URL: "
                read -e $SERVICE_URL
        done

        while [ -z "$BATCH_URL" ];do
                echo "Batch URL: "
                read -e $BATCH_URL
        done

fi
sed -i "s#@BATCH_PARTNER_ADMIN_SECRET@#$BATCH_PARTNER_ADMIN_SECRET#" -i $BATCH_MAIN_CONF
sed -i "s#@SERVICE_URL@#$SERVICE_URL#" -i $BATCH_MAIN_CONF
sed -i "s#@INSTALLED_HOSNAME@#`hostname`#" -i $BATCH_MAIN_CONF

BATCH_SCHEDULER_ID=`< /dev/urandom tr -dc 0-9 | head -c5`
sed 's#@BATCH_SCHEDULER_ID@#$BATCH_SCHEDULER_ID#' $SCHED_CONF.template > $SCHED_CONF


