#!/bin/bash - 
#===============================================================================
#          FILE: kaltura-red5-config.sh
#         USAGE: ./kaltura-red5-config.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
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
        echo "First install kaltura-red."
        exit 11
fi
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
UI_CONF=`echo "select conf_file_path from ui_conf where tags like '%kmc_uploadWebCam%';"|mysql -u$DB1_USER -P$DB1_PORT -p$DB1_PASS $DB1_NAME -h$DB1_HOST --skip-column-names`
sed -i "s@{HOST_NAME}@$RED5_HOST@g" "$BASE_DIR/web/$UI_CONF"
if [ ! -L $BASE_DIR/web/content/webcam ];then
        #mv $BASE_DIR/web/content/webcam $BASE_DIR/web/content/webcam.org
        ln -sf /usr/lib/red5/webapps/oflaDemo/streams $BASE_DIR/web/content/webcam
fi
chown apache /usr/lib/red5/webapps/oflaDemo/streams
