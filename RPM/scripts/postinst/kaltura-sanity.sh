#!/bin/bash - 
#===============================================================================
#          FILE: kaltura_sanity.sh
#         USAGE: ./kaltura_sanity.sh 
#   DESCRIPTION: post install sanity script 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy (), <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 03/20/14 07:16:53 EDT
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error

KALTURA_FUNCTIONS_RC=`dirname $0`/kaltura-functions.rc
if [ ! -r "$KALTURA_FUNCTIONS_RC" ];then
	OUT="${BRIGHT_RED}ERROR:could not find $KALTURA_FUNCTIONS_RC so, exiting..${NORMAL}"
	echo -en $OUT
	exit 1
fi
. $KALTURA_FUNCTIONS_RC
RC_FILE=/etc/kaltura.d/system.ini
if [ ! -r "$RC_FILE" ];then
	echo -e "${BRIGHT_RED}ERROR: could not find $RC_FILE so, exiting..${NORMAL}"
	exit 2 
fi
. $RC_FILE

report()
{
	TNAME=$1
	RC=$2
	MESSAGE=$3
	TIME=$4
	echo "$TNAME, RC: $RC, MESSAGE: $MESSAGE, test took: $TIME"
}
if [ "$ROLE" = "allin1" ];then
	for D in $ALL_DAEMONS; do
		START=`date +%s.%N`
		if check_daemon_status $KALTURA_VIRTUAL_HOST_NAME $D;then
			END=`date +%s.%N`
			TOTAL_T=`bc <<< $TIME`
			report "check_daemon_status" 0 "Daemon $D is running" "`bc <<< $END-$START`"
		else
			END=`date +%s.%N`
			TOTAL_T=`bc <<< $TIME`
			report "check_daemon_status" 1 "Daemon $D is NOT running" "`bc <<< $END-$START`"
		fi
		START=`date +%s.%N`
		if check_daemon_init_status $KALTURA_VIRTUAL_HOST_NAME $D;then
			END=`date +%s.%N`
			TOTAL_T=`bc <<< $TIME`
			report "check_daemon_init_status" 0 "Daemon $D configured to run on init." "`bc <<< $END-$START`"
		else
			END=`date +%s.%N`
			TOTAL_T=`bc <<< $TIME`
			report "check_daemon_init_status" 1 "Daemon $D is NOT configured to run on init." "`bc <<< $END-$START`"
		fi
	done
fi
ADMIN_PARTNER_SECRET=`echo "select admin_secret from partner where id=-2" | mysql -N -h $DB1_HOST -p$DB1_PASS $DB1_NAME -u$DB1_USER`
START=`date +%s.%N`
report "MySQL instance init" $RC "instance ID: $MYSQL_ID" "$TIME"
PARTNER_ID=`php $CSI_HOME/sanity_tests/create_partner.php $ADMIN_PARTNER_SECRET mb@kaltura.com testingpasswd $SERVICE_URL`
RC=$?
END=`date +%s.%N`
TOTAL_T=`bc <<< $TIME`
report "Create Partner" $RC "New PID is $PARTNER_ID" "`bc <<< $END-$START`"
START=`date +%s.%N`
PARTNER_SECRET=`echo "select secret from partner where id=$PARTNER_ID" | mysql -N -h $DB1_HOST -p$DB1_PASS $DB1_NAME -u$DB1_USER`
OUTP=`php $CSI_HOME/sanity_tests/upload_test.php $SERVICE_URL $PARTNER_ID $PARTNER_SECRET $WEB_DIR/content/templates/entry/data/kaltura_logo_animated_blue.flv`
RC=$?
END=`date +%s.%N`
TOTAL_T=`bc <<< $TIME`
report "Upload content kaltura_logo_animated_blue.flv" $RC "$OUTP" "`bc <<< $END-$START`"

OUTP=`php $CSI_HOME/sanity_tests/upload_test.php $SERVICE_URL $PARTNER_ID $PARTNER_SECRET $WEB_DIR/content/templates/entry/data/kaltura_logo_animated_green.flv`
RC=$?
END=`date +%s.%N`
TOTAL_T=`bc <<< $TIME`
report "Upload content kaltura_logo_animated_green.flv" $RC "$OUTP" "`bc <<< $END-$START`"

