#!/bin/bash - 
#===============================================================================
#          FILE: kaltura_sanity.sh
#         USAGE: ./kaltura_sanity.sh 
#   DESCRIPTION: post install sanity script 
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
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
if [ `id -u` != 0 ];then 
	echo -e "${BRIGHT_RED}ERROR: please run as super user, exiting..${NORMAL}"
	exit 3
fi
RC_FILE=/etc/kaltura.d/system.ini
if [ ! -r "$RC_FILE" ];then
	echo -e "${BRIGHT_RED}ERROR: could not find $RC_FILE so, exiting..${NORMAL}"
	exit 2 
fi
. $RC_FILE

DIRNAME=`dirname $0`
CAPTIONS_FILE=$DIRNAME/example.srt
rm  /tmp/`hostname`-reportme.`date +%d_%m_%Y`.sql 2> /dev/null
rm $LOG_DIR/log/*log  $LOG_DIR/log/batch/*log 2> /dev/null
for PARTITION in '/' $WEB_DIR;do
	START=`date +%s.%N`
	OUT=`check_space $PARTITION`
	RC=$?
	END=`date +%s.%N`
	TOTAL_T=`bc <<< $TIME`
	if [ $RC -ne 0 ];then
		report "Space on $PARTITION" $RC "Aborting since space on $PARTITION too low [$OUT]" "`bc <<< $END-$START`"
		exit 11
	else
		report "Space on $PARTITION" $RC "Good - $PARTITION has $SPACE free space [$OUT]" "`bc <<< $END-$START`"
	fi
done
for D in $ALL_DAEMONS; do
# if this package is installed check daemon status
        if $QUERY_COMMAND $D >/dev/null;then
		START=`date +%s.%N`
		if check_daemon_status  $D;then
			END=`date +%s.%N`
			TOTAL_T=`bc <<< $TIME`
			report "Check $D daemon status" 0 "Daemon $D is running" "`bc <<< $END-$START`"
		else
			END=`date +%s.%N`
			TOTAL_T=`bc <<< $TIME`
			report "Check $D daemon status" 1 "Daemon $D is NOT running" "`bc <<< $END-$START`"
		fi
		START=`date +%s.%N`
		if [ $D != $MONIT_DAEMON ];then
		if check_monit  $D;then
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
		if check_daemon_init_status $D;then
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

$QUERY_COMMAND kaltura-kmc --queryformat %{version} >/dev/null 2>&1
if [ $? -eq 0 ];then
	KMC_VER=`$QUERY_COMMAND kaltura-kmc --queryformat %{version} `
	COMP_NAME=kaltura-html5lib
        COMP_VER=`$QUERY_COMMAND $COMP_NAME --queryformat %{version} >/dev/null 2>&1`
	if [ $? -eq 0 ];then
		START=`date +%s.%N`
		MSG=`check_kmc_config_versions $COMP_NAME $KMC_VER`
		RC=$?
		END=`date +%s.%N`
		report "$COMP_NAME ver in KMC config.ini" $RC "$MSG" "`bc <<< $END-$START`"
	else
		echo -e "[${CYAN}$COMP_NAME ver in KMC config.ini${NORMAL}][${BRIGHT_YELLOW}SKIPPED as $COMP_NAME is not installed${NORMAL}]"
	fi
	COMP_NAME=kaltura-kdp3	
        COMP_VER=`$QUERY_COMMAND $COMP_NAME --queryformat %{version} >/dev/null 2>&1`
	if [ $? -eq 0 ];then
		START=`date +%s.%N`
		MSG=`check_kmc_config_versions $COMP_NAME $KMC_VER`
		RC=$?
		END=`date +%s.%N`
		report "$COMP_NAME ver in KDP3 config.ini" $RC "$MSG" "`bc <<< $END-$START`"
	else
		echo -e "[${CYAN}$COMP_NAME ver in KDP3 config.ini${NORMAL}][${BRIGHT_YELLOW}SKIPPED as $COMP_NAME is not installed${NORMAL}]"
	fi
	COMP_NAME=kaltura-kmc
        COMP_VER=`$QUERY_COMMAND $COMP_NAME --queryformat %{version}`
	if [ $? -eq 0 ];then
		START=`date +%s.%N`
		MSG=`check_kmc_config_versions kaltura-kmc $KMC_VER`
		RC=$?
		END=`date +%s.%N`
		report "$COMP_NAME ver in KMC config.ini" $RC "$MSG" "`bc <<< $END-$START`"
		START=`date +%s.%N`
		OUT=`php $DIRNAME/get_kmc_swfs.php`
		RC=$?
		END=`date +%s.%N`
		report "Get KMC SWFs" $RC "$OUT" "`bc <<< $END-$START`"
		
	else
		echo -e "[${CYAN}$COMP_NAME ver in KMC config.ini${NORMAL}][${BRIGHT_YELLOW}SKIPPED as $COMP_NAME is not installed${NORMAL}]"
	fi
fi

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

if $QUERY_COMMAND kaltura-html5lib >/dev/null 2>&1 ;then
	START=`date +%s.%N`
	MSG=`check_studio_index_page`
	RC=$?
	END=`date +%s.%N`
	report "check_studio_index_page" $RC "$MSG" "`bc <<< $END-$START`"
fi

if $QUERY_COMMAND kaltura-clipapp >/dev/null 2>&1 ;then
	START=`date +%s.%N`
	MSG=`check_clipapp_index_page`
	RC=$?
	END=`date +%s.%N`
	report "check_clipapp_index_page" $RC "$MSG" "`bc <<< $END-$START`"
fi

ADMIN_PARTNER_SECRET=`echo "select admin_secret from partner where id=-2" | mysql -N -h $DB1_HOST -p$DB1_PASS $DB1_NAME -u$DB1_USER  -P$DB1_PORT`
NOW=`date +%d-%H-%m-%S`
START=`date +%s.%N`
if $QUERY_COMMAND kaltura-batch >/dev/null 2>&1 || $QUERY_COMMAND kaltura-front >/dev/null 2>&1 ;then
	PARTNER_ID=`php $DIRNAME/create_partner.php $ADMIN_PARTNER_SECRET mb-$HOSTNAME@kaltura.com testingpasswd $SERVICE_URL 2>&1`
	RC=$?
	END=`date +%s.%N`
	report "Create Partner" $RC "New PID is $PARTNER_ID" "`bc <<< $END-$START`"
	if [ $RC -ne 0 ];then
		echo -e "${BRIGHT_RED}Partner creation failed. I will skip all tests that require it.${NORMAL}"
	else
		START=`date +%s.%N`
		OUT=`php $DIRNAME/dropbox_test.php $SERVICE_URL $PARTNER_ID $ADMIN_PARTNER_SECRET /tmp/sanity-drop-$NOW-$HOSTNAME 2>&1`
		RC=$?
		END=`date +%s.%N`
		if [ $RC -ne 0 ];then
		
			report "Local dropfolder creation failed" $RC "$OUT" "`bc <<< $END-$START`" 
		else
			report "Local dropfolder creation succeeded" $RC "$OUT" "`bc <<< $END-$START`" 
		
		fi
		PARTNER_SECRET=`echo "select secret from partner where id=$PARTNER_ID" | mysql -N -h $DB1_HOST -p$DB1_PASS $DB1_NAME -u$DB1_USER -P$DB1_PORT`
		 PARTNER_ADMIN_SECRET=`echo "select admin_secret from partner where id=$PARTNER_ID" | mysql -N -h $DB1_HOST -p$DB1_PASS $DB1_NAME -u$DB1_USER -P$DB1_PORT`
		 ZERO_PARTNER_ADMIN_SECRET=`echo "select admin_secret from partner where id=0" | mysql -N -h $DB1_HOST -p$DB1_PASS $DB1_NAME -u$DB1_USER -P$DB1_PORT`
		sed -i "s#@PARTNER_ID@#$PARTNER_ID#g" $BASE_DIR/bin/sanity_config.ini
		sed -i "s#@PARTNER_ADMIN_SECRET@#$PARTNER_ADMIN_SECRET#g" $BASE_DIR/bin/sanity_config.ini
		sed -i "s#@ADMIN_CONSOLE_PARTNER_ID@#-2#g" $BASE_DIR/bin/sanity_config.ini
		sed -i "s#@ADMIN_CONSOLE_PARTNER_ADMIN_SECRET@#$ADMIN_PARTNER_SECRET#g" $BASE_DIR/bin/sanity_config.ini
			START=`date +%s.%N`
			FLAVOR_PARAM_ID=`php $DIRNAME/create_flavor_params.php $ZERO_PARTNER_ADMIN_SECRET $SERVICE_URL 2>&1`
			#echo "$DIRNAME/create_flavor_params.php $ZERO_PARTNER_ADMIN_SECRET $SERVICE_URL 2>&1"
			RC=$?
			END=`date +%s.%N`
			TOTAL_T=`bc <<< $TIME`
			report "Create flavor param" $RC "$FLAVOR_PARAM_ID" "`bc <<< $END-$START`"
			if [ "$RC" -eq 0 ];then
				START=`date +%s.%N`
				OUT=`php  $DIRNAME/delete_flavor_params.php $ZERO_PARTNER_ADMIN_SECRET $SERVICE_URL $FLAVOR_PARAM_ID 2>&1`
				#echo  "$DIRNAME/delete_flavor_params.php $ZERO_PARTNER_ADMIN_SECRET $SERVICE_URL $FLAVOR_PARAM_ID 2>&1"
				RC=$?
				END=`date +%s.%N`
				TOTAL_T=`bc <<< $TIME`
				report "Delete flavor param" $RC "$FLAVOR_PARAM_ID" "`bc <<< $END-$START`"
			fi
			START=`date +%s.%N`
			UPLOADED_ENT=`php $DIRNAME/upload_test.php $SERVICE_URL $PARTNER_ID $PARTNER_SECRET $WEB_DIR/content/templates/entry/data/kaltura_logo_animated_blue.flv 2>&1`
			RC=$?
			END=`date +%s.%N`
			TOTAL_T=`bc <<< $TIME`
			report "Upload content kaltura_logo_animated_blue.flv" $RC "$UPLOADED_ENT" "`bc <<< $END-$START`"
			START=`date +%s.%N`
			CONVERT_SUCCESS=0
			for i in `seq 1 9`;do
				php $DIRNAME/check_entry_status.php $SERVICE_URL $PARTNER_ID $PARTNER_SECRET $UPLOADED_ENT
				# for us, status 2 is good
				if [ $? -eq 2 ];then
					RC=0
					END=`date +%s.%N`
					TOTAL_T=`bc <<< $TIME`
					CONVERT_SUCCESS=1
					break;
				fi
				echo -e "${CYAN}Napping 10 seconds to allow entry $UPLOADED_ENT to digest.. ${NORMAL}"
				sleep 10
			done
			if [ "$CONVERT_SUCCESS" -eq 1 ];then
				report "kaltura_logo_animated_blue.flv - $UPLOADED_ENT status" $RC "$UPLOADED_ENT converted" "`bc <<< $END-$START`"
				START=`date +%s.%N`
				OUT=` php $DIRNAME/create_thumbnail.php $SERVICE_URL $PARTNER_ID $PARTNER_ADMIN_SECRET $UPLOADED_ENT 1 2>&1`
				curl -s $OUT > /tmp/$UPLOADED_ENT.jpg
				compare -verbose -metric mae /tmp/$UPLOADED_ENT.jpg $DIRNAME/kaltura_logo_animated_blue_1_sec.jpg /tmp/$UPLOADED_ENT-diff.jpg  2>&1 | grep -q "all: 0 (0)" 
				RC=$?
				END=`date +%s.%N`
				TOTAL_T=`bc <<< $END-$START`
				if [ $RC -ne 0 ];then
					report "Thumb for $UPLOADED_ENT does not match the signature of $DIRNAME/kaltura_logo_animated_blue_1_sec.jpg" $RC "$OUT" "$TOTAL_T"
				else
					report "Thumb for $UPLOADED_ENT identical to $DIRNAME/kaltura_logo_animated_blue_1_sec.jpg" $RC "$OUT" "$TOTAL_T"
				fi	
				START=`date +%s.%N`
				OUT=`php $DIRNAME/clip_test.php $SERVICE_URL $PARTNER_ID $PARTNER_ADMIN_SECRET  $UPLOADED_ENT 0`
				RC=$?
				END=`date +%s.%N`
				TOTAL_T=`bc <<< $END-$START`
				if [ $RC -eq 0 ];then
					report "Clipping $UPLOADED_ENT Succeeded" $RC "$OUT" "$TOTAL_T"
				else
					report "Clipping $UPLOADED_ENT failed" $RC "$OUT" "$TOTAL_T"
				fi	

				START=`date +%s.%N`
				OUT=`php $DIRNAME/clip_test.php $SERVICE_URL $PARTNER_ID $PARTNER_ADMIN_SECRET  $UPLOADED_ENT 1`
				RC=$?
				END=`date +%s.%N`
				TOTAL_T=`bc <<< $END-$START`
				if [ $RC -eq 0 ];then
					report "Trimming $UPLOADED_ENT Succeeded" $RC "$OUT" "$TOTAL_T"
				else
					report "Trimming $UPLOADED_ENT failed" $RC "$OUT" "$TOTAL_T"
				fi	
				
				START=`date +%s.%N`
				OUT=`php $DIRNAME/play.php --service-url=$SERVICE_URL --entry-id=$UPLOADED_ENT  --partner=$PARTNER_ID --secret=$PARTNER_SECRET|sed "s@\"@@g"`
				RC=$?
				END=`date +%s.%N`
				TOTAL_T=`bc <<< $END-$START`
				if [ $RC -ne 0 ];then
					report "Mock playback $UPLOADED_ENT failed" $RC "$OUT" "$TOTAL_T"
				else
					report "Mock playback $UPLOADED_ENT succeeded" $RC "$OUT" "$TOTAL_T"
				fi	
				START=`date +%s.%N`
				OUT=`php $DIRNAME/add_caption.php $PARTNER_ID $PARTNER_ADMIN_SECRET $SERVICE_URL $UPLOADED_ENT $CAPTIONS_FILE EN`
				RC=$?
				END=`date +%s.%N`
				TOTAL_T=`bc <<< $END-$START`
				if [ $RC -ne 0 ];then
					report "Adding captions to $UPLOADED_ENT failed" $RC "$OUT" "$TOTAL_T"
				else
					report "Addition captions to $UPLOADED_ENT succeeded" $RC "$OUT" "$TOTAL_T"
				fi	
				START=`date +%s.%N`
				# ',' means search for either one of these strings, i.e: logical OR
				OUT=`php $DIRNAME/search_entry.php $PARTNER_ID $PARTNER_SECRET $SERVICE_URL "Example,Deja,Bold"`	
				RC=$?
				END=`date +%s.%N`
				TOTAL_T=`bc <<< $END-$START`
				if [ $RC -ne 0 ];then
					report "Searching for Example||Deja||Bold in $UPLOADED_ENT metadata failed" $RC "$OUT" "$TOTAL_T"
				else
					report "Searching for Example||Deja||Bold in $UPLOADED_ENT metadata succeded" $RC "$OUT" "$TOTAL_T"
				fi	
				START=`date +%s.%N`
				OUT=`php $DIRNAME/recon.php $SERVICE_URL $PARTNER_ID $PARTNER_ADMIN_SECRET $UPLOADED_ENT`
				RC=$?
				if [ $RC -eq 0 ];then
					CONVERT_SUCCESS=0
					for i in `seq 1 9`;do
						php $DIRNAME/check_entry_status.php $SERVICE_URL $PARTNER_ID $PARTNER_SECRET $UPLOADED_ENT
						# for us, status 2 is good
						if [ $? -eq 2 ];then
							RC=0
							END=`date +%s.%N`
							TOTAL_T=`bc <<< $TIME`
							CONVERT_SUCCESS=1
							break;
						fi
						echo -e "${CYAN}Napping 10 seconds to allow entry $UPLOADED_ENT to digest.. ${NORMAL}"
						sleep 10
					done
					END=`date +%s.%N`
					TOTAL_T=`bc <<< $END-$START`
					if [ "$CONVERT_SUCCESS" -eq 1 ];then
						report "Entry reconversion of $UPLOADED_ENT succeeded" $RC "$OUT" "$TOTAL_T"
					else
						report "Entry reconversion of $UPLOADED_ENT failed" $RC "$OUT" "$TOTAL_T"
					fi	
				else
					END=`date +%s.%N`
					TOTAL_T=`bc <<< $END-$START`
					report "Calling media->convert on $UPLOADED_ENT failed" $RC "$OUT" "$TOTAL_T"
					
				fi
			else
				report "kaltura_logo_animated_blue.flv - $UPLOADED_ENT status" 1 "$UPLOADED_ENT failed to convert." "`bc <<< $END-$START`"
			fi
			START=`date +%s.%N`
			echo "Testing mail sending" |mail -s "Kaltura sanity test email" mb-$HOSTNAME@kaltura.com
			echo -e "${CYAN}Napping 30 seconds to allow mail to be sent out.. ${NORMAL}"
			sleep 30
			MSG=`grep mb-$HOSTNAME@kaltura.com $MAIL_LOG `
			RC=$?
			END=`date +%s.%N`
			if [ $RC -ne 0 ];then
				report "Could not find an email sending entry for mb-$HOSTNAME@kaltura.com [PID is $PARTNER_ID] in $MAIL_LOG" $RC "" "`bc <<< $END-$START`"
			else
				report "Found an email sending entry for mb-$HOSTNAME@kaltura.com[PID is $PARTNER_ID] in $MAIL_LOG" $RC "$MSG" "`bc <<< $END-$START`"

			fi

			if $QUERY_COMMAND kaltura-dwh >> /dev/null 2>&1;then
				echo -e "${CYAN}Testing analytics, be patient..

Please note: if you are running this test on a clustered ENV, it will fail but this does not mean there is an actual problem.
The tech information as to why is available here: 
https://github.com/kaltura/platform-install-packages/issues/106#issuecomment-42837404
${NORMAL}"
  # this is to allow the logrotation to finish.
  sleep 120 
				START=`date +%s.%N`
				OUTP=`php $DIRNAME/dwh_cycle.php $DIRNAME/sanity_config.ini 2>&1`
				RC=$?
				CLEANOUTPUT=`echo $OUTP|sed 's@"@@g'`
				OUTP=`echo $CLEANOUTPUT|sed "s@'@@g"`
				END=`date +%s.%N`
				TOTAL_T=`bc <<< $TIME`
				report "DWH cycle" $RC "$OUTP" "`bc <<< $END-$START`"
			fi

			START=`date +%s.%N`
			OUTP=`php $DIRNAME/upload_test.php $SERVICE_URL $PARTNER_ID $PARTNER_SECRET $WEB_DIR/content/templates/entry/data/kaltura_logo_animated_blue.flv 2>&1`
			RC=$?
			CLEANOUTPUT=`echo $OUTP|sed 's@"@@g'`
			OUTP=`echo $CLEANOUTPUT|sed "s@'@@g"`
			END=`date +%s.%N`
			TOTAL_T=`bc <<< $TIME`
			report "Upload content kaltura_logo_animated_green.flv" $RC "$OUTP" "`bc <<< $END-$START`"

			unzip -oqq $WEB_DIR/content/docs/kaltura_batch_upload_falcon.zip -d $WEB_DIR/content/docs
			START=`date +%s.%N`
			OUTP=`php $DIRNAME/upload_bulk.php $SERVICE_URL $PARTNER_ID $PARTNER_ADMIN_SECRET MB $WEB_DIR/content/docs/kaltura_batch_upload_falcon.csv bulkUploadCsv.CSV 2>&1`
			RC=$?
			CLEANOUTPUT=`echo $OUTP|sed 's@"@@g'`
			OUTP=`echo $CLEANOUTPUT|sed "s@'@@g"`
			END=`date +%s.%N`
			TOTAL_T=`bc <<< $TIME`
			report "Upload bulk using CSV" $RC "$OUTP" "`bc <<< $END-$START`"

			START=`date +%s.%N`
			OUTP=`php $DIRNAME/upload_bulk.php $SERVICE_URL $PARTNER_ID $PARTNER_ADMIN_SECRET MB $WEB_DIR/content/docs/kaltura_batch_upload_falcon.xml bulkUploadXml.XML 2>&1`
			RC=$?
			CLEANOUTPUT=`echo $OUTP|sed 's@"@@g'`
			OUTP=`echo $CLEANOUTPUT|sed "s@'@@g"`
			END=`date +%s.%N`
			TOTAL_T=`bc <<< $TIME`
			report "Upload bulk using XML" $RC "$OUTP" "`bc <<< $END-$START`"
			START=`date +%s.%N`
			OUTP=`php $DIRNAME/generate_player.php $SERVICE_URL $PARTNER_ID $PARTNER_ADMIN_SECRET 3.9.8 $DIRNAME/player.xml 2>&1`
			RC=$?
			CLEANOUTPUT=`echo $OUTP|sed 's@"@@g'`
			OUTP=`echo $CLEANOUTPUT|sed "s@'@@g"`
			END=`date +%s.%N`
			TOTAL_T=`bc <<< $TIME`
			report "Create player" $RC "$OUTP" "`bc <<< $END-$START`"
			START=`date +%s.%N`
			OUTP=`php $DIRNAME/generate_thumb.php $SERVICE_URL $PARTNER_ID $PARTNER_ADMIN_SECRET $UPLOADED_ENT 2>&1`
			RC=$?
			CLEANOUTPUT=`echo $OUTP|sed 's@"@@g'`
			OUTP=`echo $CLEANOUTPUT|sed "s@'@@g"`
			END=`date +%s.%N`
			TOTAL_T=`bc <<< $TIME`
			report "Generate thumb" $RC "$OUTP" "`bc <<< $END-$START`"


			START=`date +%s.%N`
			OUTP=`php $DIRNAME/delete_partner.php $DIRNAME/sanity_config.ini 2>&1`
			RC=$?
			CLEANOUTPUT=`echo $OUTP|sed 's@"@@g'`
			OUTP=`echo $CLEANOUTPUT|sed "s@'@@g"`
			END=`date +%s.%N`
			TOTAL_T=`bc <<< $TIME`
			report "Delete partner" $RC "$OUTP" "`bc <<< $END-$START`"
	fi
sed -i "1,/^adminConsolePartnerId/s/^adminConsolePartnerId\s*=.*/adminConsolePartnerId=@ADMIN_CONSOLE_PARTNER_ID@/" $DIRNAME/sanity_config.ini
sed -i "1,/^adminConsoleSecret/s/^adminConsoleSecret\s*=.*/adminConsoleSecret=@ADMIN_CONSOLE_PARTNER_ADMIN_SECRET@/" $DIRNAME/sanity_config.ini
sed -i "1,/^partnerId/s/^partnerId\s*=.*/partnerId=@PARTNER_ID@/" $DIRNAME/sanity_config.ini
sed -i "1,/^adminSecret/s/^adminSecret\s*=.*/adminSecret=@PARTNER_ADMIN_SECRET@/" $DIRNAME/sanity_config.ini

fi
WEBCAM_SYNLINK=`readlink -f $WEB_DIR/content/webcam`
TEST_NAME="Red5 file upload"
if [ "$WEBCAM_SYNLINK" = /usr/lib/red5/webapps/oflaDemo/streams ]; then
	START=`date +%s.%N`
	OUTP=`test_red5_conn`
	RC=$?
	CLEANOUTPUT=`echo $OUTP|sed 's@"@@g'`
	OUTP=`echo $CLEANOUTPUT|sed "s@'@@g"`
	END=`date +%s.%N`
	report "$TEST_NAME" $RC "$OUTP" "`bc <<< $END-$START`"
else
	echo -e "[${CYAN}$TEST_NAME${NORMAL}] ${BRIGHT_YELLOW}[SKIPPED as OflaDemo isn't configured]
see: https://github.com/kaltura/platform-install-packages/blob/master/doc/install-kaltura-redhat-based.md#configure-red5-server${NORMAL}"
fi


echo -e "${BRIGHT_BLUE}

Thank you for running Kaltura! To keep Kaltura viable, stable and well tested, please join the community and help by contributing sanity tests that verify overall platform stability: http://bit.ly/kaltura-ci , and by contributing to the project roadmap by solving simple tasks and challenges: http://bit.ly/kaltura-tasks.
${NORMAL}"

#START=`date +%s.%N`
#OUTP=`check_missing_web_files`
#RC=$?
#END=`date +%s.%N`
#if [ $RC -ne 0 ];then
#	report "Check missing web/content files - $OUTP" $RC, $OUTP "`bc <<< $END-$START`"
#else
#	report "Check missing web/content files - none are missing" $RC, "All files found" "`bc <<< $END-$START`"
#
#fi

