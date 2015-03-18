#!/bin/bash - 
#===============================================================================
#          FILE: kaltura-config-all.sh
#         USAGE: ./kaltura-config-all.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy (), <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 03/17/14 05:27:57 EDT
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error

BASE_DIR=/opt/kaltura/
if [ -n "$1" -a -r "$1" ];then
        ANSFILE=$1
       . $ANSFILE
       export ANSFILE
fi

KALTURA_FUNCTIONS_RC=`dirname $0`/kaltura-functions.rc
if [ ! -r "$KALTURA_FUNCTIONS_RC" ];then
       echo -e "Could not find $KALTURA_FUNCTIONS_RC so, exiting.."
       exit 3
fi
. $KALTURA_FUNCTIONS_RC

echo -e "Running base config..."
if [ -r /etc/sysconfig/clock ];then
       . /etc/sysconfig/clock
else
       ZONE="unknown"
fi  

$BASE_DIR/bin/kaltura-base-config.sh "$ANSFILE"
if [ $? -ne 0 ];then
       echo -e "${BRIGHT_RED}ERROR: $BASE_DIR/bin/kaltura-base-config.sh failed. Please resolve the issue and re-run the installer.${NORMAL}"
       exit 1
fi

RC_FILE=/etc/kaltura.d/system.ini
if [ ! -r "$RC_FILE" ];then
       echo -e "${BRIGHT_RED}ERROR: could not find $RC_FILE so, exiting..${NORMAL}"
       exit 2
fi
. $RC_FILE

echo -e "Running FrontEnd config..."

$BASE_DIR/bin/kaltura-front-config.sh "$ANSFILE"
if [ $? -ne 0 ];then
       echo -e "${BRIGHT_RED}ERROR: $BASE_DIR/bin/kaltura-front-config.sh failed. Please resolve the issue and re-run the installer.${NORMAL}"
       exit 2 
fi

echo -ne "Running Sphinx config... "
$BASE_DIR/bin/kaltura-sphinx-config.sh "$ANSFILE"
if [ $? -ne 0 ];then
       echo -e "${BRIGHT_RED}ERROR: $BASE_DIR/bin/kaltura-sphinx-config.sh failed. Please resolve the issue and re-run the installer.${NORMAL}"
       exit 3 
fi

trap - ERR
echo "use kaltura" | mysql -h$DB1_HOST -P$DB1_PORT -u$SUPER_USER -p$SUPER_USER_PASSWD mysql 2> /dev/null
if [ $? -ne 0 ];then
	echo -e "Configuring your Kaltura DB..."
	$BASE_DIR/bin/kaltura-db-config.sh $DB1_HOST $SUPER_USER $SUPER_USER_PASSWD $DB1_PORT $SPHINX_HOST
	RC=$?
	if [ $RC -eq 0 ];then
		if [ "$APACHE_MODE" = "HTTPS" ];then
			echo "use kaltura" | mysql -h$DB1_HOST -u$DB1_USER -p$DB1_PASS -P$DB1_PORT $DB1_NAME 2> /dev/null
			if [ $? -eq 0 ];then
				echo "update permission set STATUS=1 WHERE permission.NAME='FEATURE_KMC_ENFORCE_HTTPS';" | mysql $DB1_NAME -h$DB1_HOST -u$DB1_USER -P$DB1_PORT -p$DB1_PASS 2> /dev/null 
			fi
		else
			echo "use kaltura" | mysql -h$DB1_HOST -u$DB1_USER -p$DB1_PASS -P$DB1_PORT $DB1_NAME 2> /dev/null
			if [ $? -eq 0 ];then
				echo "update permission set STATUS=3 WHERE permission.NAME='FEATURE_KMC_ENFORCE_HTTPS';" | mysql $DB1_NAME -h$DB1_HOST -u$DB1_USER -P$DB1_PORT -p$DB1_PASS 2> /dev/null 
			fi
		fi
	elif [ $RC = 111 ];then
        echo -e "${BRIGHT_RED}ERROR: $BASE_DIR/bin/kaltura-db-config.sh $DB1_HOST $SUPER_USER $SUPER_USER_PASSWD $DB1_PORT failed when trying to populate the DB."
		echo -e "It tried reaching $SERVICE_URL/api_v3/index.php?service=system&action=ping and couldn't."
		echo -e "This probably means you have either supplied a bad service URL or have yet to configure your Apache."
		echo -e "To configure your Apache, please use $BASE_DIR/bin/kaltura-front-config.sh."
		echo -e "Since the schema creation succeeded, you can skip that part by running:"
		echo -e "# POPULATE_ONLY=1 $BASE_DIR/bin/kaltura-db-config.sh $DB1_HOST $SUPER_USER $SUPER_USER_PASSWD $DB1_PORT"
		echo -e "Please run it manually to debug the issue."
		echo -e "ou may run $0 again once done.${NORMAL}"
        exit 111
    else
		echo -e "${BRIGHT_RED}ERROR: we failed on something else..${NORMAL}"
		exit 112
    fi
fi

echo -e "Running Batch config..."

$BASE_DIR/bin/kaltura-batch-config.sh "$ANSFILE"
if [ $? -ne 0 ];then
       echo -e "${BRIGHT_RED}ERROR: $BASE_DIR/bin/kaltura-batch-config.sh failed. Please resolve the issue and re-run the installer.${NORMAL}"
	exit 113 
fi

$BASE_DIR/bin/kaltura-nginx-config.sh "$ANSFILE"
if [ $? -ne 0 ];then
       echo -e "${BRIGHT_RED}ERROR: $BASE_DIR/bin/kaltura-nginx-config.sh failed. Please resolve the issue and re-run the installer.${NORMAL}"
	exit 114 
fi

#echo -e "Running Red5 config..."
#
#$BASE_DIR/bin/kaltura-red5-config.sh "$ANSFILE" 
#

echo -e "Running DWH config..."

$BASE_DIR/bin/kaltura-dwh-config.sh "$ANSFILE" 
if [ $? -ne 0 ];then
       echo -e "${BRIGHT_RED}ERROR: $BASE_DIR/bin/kaltura-dwh-config.sh failed. Please resolve the issue and re-run the installer.${NORMAL}"
fi

rm -rf $APP_DIR/cache/*
rm -f $APP_DIR/log/kaltura-*.log

echo -e "${CYAN}
====================================================================================================================

Setup completed successfully! 

To access your Kaltura tools visit:
${BRIGHT_BLUE}$SERVICE_URL${CYAN}

To verify the integrity of your deployment and that all components are fully configured and installed,
you can run the sanity tests using the following command:
$BASE_DIR/bin/kaltura-sanity.sh 

To begin, access the Admin Console using the Admin email and password you've entered while installing.
When logged in to the KAC, create a new publisher account to being using Kaltura.
Visit ${BRIGHT_BLUE}http://www.kaltura.org${CYAN} to join the community and get help!
Visit ${BRIGHT_BLUE}http://forum.kaltura.org${CYAN} to post issues and help others with theirs.
Visit ${BRIGHT_BLUE}http://knowledge.kaltura.com${CYAN} to read documentation and learn more.
=====================================================================================================================


Thank you for running Kaltura! To keep Kaltura viable, stable and tested, please join the community and help by contributing sanity tests that verify overall platform stability: http://bit.ly/kaltura-ci , and by contributing to the project roadmap by solving simple tasks and challenges: http://bit.ly/kaltura-tasks.


${NORMAL}
"

find $BASE_DIR/app/cache/ $BASE_DIR/log -type d -exec chmod 775 {} \; 
find $BASE_DIR/app/cache/ $BASE_DIR/log -type f -exec chmod 664 {} \; 
chown -R kaltura.apache $BASE_DIR/app/cache/ $BASE_DIR/log
chmod 775 $BASE_DIR/web/content
send_post_inst_msg $ADMIN_CONSOLE_ADMIN_MAIL 

send_install_beacon `basename $0` $ZONE install_success

