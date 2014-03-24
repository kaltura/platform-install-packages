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

for D in $ALL_DAEMONS; do
# if this package is installed check daemon status
        if ssh -lroot $KALTURA_VIRTUAL_HOST_NAME $SSH_QUIET_OPTS "rpm -q $D >/dev/null";then
		START=`date +%s.%N`
		if check_daemon_status $KALTURA_VIRTUAL_HOST_NAME $D;then
			END=`date +%s.%N`
			TOTAL_T=`bc <<< $TIME`
			report "Check $D daemon status" 0 "Daemon $D is running" "`bc <<< $END-$START`"
		else
			END=`date +%s.%N`
			TOTAL_T=`bc <<< $TIME`
			report "Check $D daemon status" 1 "Daemon $D is NOT running" "`bc <<< $END-$START`"
		fi
		START=`date +%s.%N`
		if [ $D != 'kaltura-monit' ];then
		if check_monit $KALTURA_VIRTUAL_HOST_NAME $D;then
			END=`date +%s.%N`
			TOTAL_T=`bc <<< $TIME`
			report "Check $D daemon is started by Monit" 0 "Daemon $D is running" "`bc <<< $END-$START`"
		else
			END=`date +%s.%N`
			TOTAL_T=`bc <<< $TIME`
			report "Check $D daemon is started by Monit" 1 "Daemon $D is NOT running" "`bc <<< $END-$START`"
		fi
		fi
		START=`date +%s.%N`
		if check_daemon_init_status $KALTURA_VIRTUAL_HOST_NAME $D;then
			END=`date +%s.%N`
			TOTAL_T=`bc <<< $TIME`
			report "check daemon $D init status" 0 "Daemon $D configured to run on init." "`bc <<< $END-$START`"
		else
			END=`date +%s.%N`
			TOTAL_T=`bc <<< $TIME`
			report "check_daemon_init_status" 1 "Daemon $D is NOT configured to run on init." "`bc <<< $END-$START`"
		fi
	else
		echo -e "[${CYAN}Check $D daemon status${NORMAL}] [${BRIGHT_YELLOW}SKIPPED as $D is not installed${NORMAL}]"
		echo -e "[${CYAN}Check $D daemon init${NORMAL}] [${BRIGHT_YELLOW}SKIPPED as $D is not installed${NORMAL}]"
	fi
done
START=`date +%s.%N`
MSG=`check_start_page`
END=`date +%s.%N`
RC=$?
END=`date +%s.%N`
report "check_start_page" $RC "$MSG" "`bc <<< $END-$START`"
START=`date +%s.%N`
MSG=`check_testme_page`
RC=$?
END=`date +%s.%N`
report "check_testme_page" $RC "$MSG" "`bc <<< $END-$START`"

START=`date +%s.%N`
MSG=`check_kmc_index_page`
RC=$?
END=`date +%s.%N`
report "check_kmc_index_page" $RC "$MSG" "`bc <<< $END-$START`"

START=`date +%s.%N`
MSG=`check_admin_console_index_page`
RC=$?
END=`date +%s.%N`
report "check_admin_console_index_page" $RC "$MSG" "`bc <<< $END-$START`"

DIRNAME=`dirname $0`
ADMIN_PARTNER_SECRET=`echo "select admin_secret from partner where id=-2" | mysql -N -h $DB1_HOST -p$DB1_PASS $DB1_NAME -u$DB1_USER`
NOW=`date +%d-%H-%m-%S`
START=`date +%s.%N`
PARTNER_ID=`php $DIRNAME/create_partner.php $ADMIN_PARTNER_SECRET mb-$NOW@kaltura.com testingpasswd $SERVICE_URL 2>&1`
RC=$?
END=`date +%s.%N`
report "Create Partner" $RC "New PID is $PARTNER_ID" "`bc <<< $END-$START`"
START=`date +%s.%N`
PARTNER_SECRET=`echo "select secret from partner where id=$PARTNER_ID" | mysql -N -h $DB1_HOST -p$DB1_PASS $DB1_NAME -u$DB1_USER`
PARTNER_ADMIN_SECRET=`echo "select admin_secret from partner where id=$PARTNER_ID" | mysql -N -h $DB1_HOST -p$DB1_PASS $DB1_NAME -u$DB1_USER`
OUTP=`php $DIRNAME/upload_test.php $SERVICE_URL $PARTNER_ID $PARTNER_SECRET $WEB_DIR/content/templates/entry/data/kaltura_logo_animated_blue.flv 2>&1`
RC=$?
END=`date +%s.%N`
TOTAL_T=`bc <<< $TIME`
report "Upload content kaltura_logo_animated_blue.flv" $RC "$OUTP" "`bc <<< $END-$START`"

START=`date +%s.%N`
OUTP=`php $DIRNAME/upload_test.php $SERVICE_URL $PARTNER_ID $PARTNER_SECRET $WEB_DIR/content/templates/entry/data/kaltura_logo_animated_green.flv 2>&1`
RC=$?
END=`date +%s.%N`
TOTAL_T=`bc <<< $TIME`
report "Upload content kaltura_logo_animated_green.flv" $RC "$OUTP" "`bc <<< $END-$START`"

unzip -oqq $WEB_DIR/content/docs/kaltura_batch_upload_falcon.zip -d $WEB_DIR/content/docs
START=`date +%s.%N`
OUTP=`php $DIRNAME/upload_bulk.php $SERVICE_URL $PARTNER_ID $PARTNER_ADMIN_SECRET MB $WEB_DIR/content/docs/kaltura_batch_upload_falcon.csv bulkUploadCsv.CSV 2>&1`
RC=$?
END=`date +%s.%N`
TOTAL_T=`bc <<< $TIME`
report "Upload bulk using CSV" $RC "$OUTP" "`bc <<< $END-$START`"

START=`date +%s.%N`
OUTP=`php $DIRNAME/upload_bulk.php $SERVICE_URL $PARTNER_ID $PARTNER_ADMIN_SECRET MB $WEB_DIR/content/docs/kaltura_batch_upload_falcon.xml bulkUploadXml.XML 2>&1`
RC=$?
END=`date +%s.%N`
TOTAL_T=`bc <<< $TIME`
report "Upload bulk using XML" $RC "$OUTP" "`bc <<< $END-$START`"


WEBCAM_SYNLINK=`readlink -f $WEB_DIR/content/webcam`
TEST_NAME="Red5 file upload"
if [ $WEBCAM_SYNLINK = /usr/lib/red5/webapps/oflaDemo/streams ]; then
	START=`date +%s.%N`
	OUTP=`test_red5_conn`
	RC=$?
	END=`date +%s.%N`
	report "$TEST_NAME" $RC "$OUTP" "`bc <<< $END-$START`"
else
	echo -e "[${CYAN}$TEST_NAME${NORMAL}] ${BRIGHT_YELLOW}[SKIPPED as OflaDemo isn't configured]
see: https://github.com/kaltura/platform-install-packages/blob/master/doc/install-kaltura-redhat-based.md#configure-red5-server${NORMAL}"
fi

START=`date +%s.%N`
OUTP=`check_missing_web_files`
RC=$?
END=`date +%s.%N`
if [ $RC -ne 0 ];then
	report "Check missing web/content files - $OUTP" $RC, $OUTP "`bc <<< $END-$START`"
else
	report "Check missing web/content files - none are missing" $RC, "All files found" "`bc <<< $END-$START`"

fi

