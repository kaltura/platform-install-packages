#!/bin/bash - 
#===============================================================================
#          FILE: kaltura-red5-config.sh
#         USAGE: ./kaltura-red5-config.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy (), <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 02/14/14 10:47:53 EST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error
if ! rpm -q kaltura-red5;then
	echo -e "${BRIGHT_BLUE}Skipping as kaltura-red5 is not installed.${NORMAL}"
        exit 0 
fi
if [ ! -r /opt/kaltura/app/base-config.lock ];then
        `dirname $0`/kaltura-base-config.sh
else
        echo "base-config completed successfully, if you ever want to re-configure your system (e.g. change DB hostname) run the following script:
# rm /opt/kaltura/app/base-config.lock
# $BASE_DIR/bin/kaltura-base-config.sh
"
fi
KALTURA_FUNCTIONS_RC=`dirname $0`/kaltura-functions.rc
if [ ! -r "$KALTURA_FUNCTIONS_RC" ];then
	OUT="ERROR:could not find $KALTURA_FUNCTIONS_RC so, exiting.."
	echo -en $OUT
	exit 3
fi
. $KALTURA_FUNCTIONS_RC
RC_FILE=/etc/kaltura.d/system.ini
if [ ! -r "$RC_FILE" ];then
        echo "${BRIGHT_RED}Could not find $RC_FILE so, exiting..${NORMAL}"
        exit 2
fi
. $RC_FILE
UI_CONF=`echo "select conf_file_path from ui_conf where tags like '%kmc_uploadWebCam%' LIMIT 1;"|mysql -u$DB1_USER -P$DB1_PORT -p$DB1_PASS $DB1_NAME -h$DB1_HOST --skip-column-names`
sed -i "s@{HOST_NAME}@$RED5_HOST@g" "$BASE_DIR/web/$UI_CONF"

if [ ! -d /usr/lib/red5/webapps/oflaDemo/streams ];then
        echo -e "${BRIGHT_RED}You need to install OflaDemo. Please follow instructions here:
https://github.com/kaltura/platform-install-packages/blob/master/doc/install-kaltura-redhat-based.md#configure-red5-server ${NORMAL}"
fi
if [ ! -L $BASE_DIR/web/content/webcam ];then
        ln -sf /usr/lib/red5/webapps/oflaDemo/streams $BASE_DIR/web/content/webcam
fi


chown apache /usr/lib/red5/webapps/oflaDemo/streams
