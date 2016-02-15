#!/bin/bash - 
#===============================================================================
#          FILE: kaltura-media-server-config.sh
#         USAGE: ./kaltura-media-server-config.sh 
#   DESCRIPTION: configure server as a media-server node.
#       OPTIONS: ---
#   LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Kobi Michaeli <kobi.michaeli@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 14/2/16
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error


KALTURA_FUNCTIONS_RC=`dirname $0`/kaltura-functions.rc
if [ ! -r "$KALTURA_FUNCTIONS_RC" ];then
    OUT="Could not find $KALTURA_FUNCTIONS_RC so, exiting.."
    echo $OUT
    exit 3
fi
. $KALTURA_FUNCTIONS_RC

if ! rpm -q kaltura-media-server;then
    echo -e "${BRIGHT_RED}ERROR: First install kaltura-media-server.${NORMAL}"
    exit 0
fi

if [ -r $CONSENT_FILE ];then
    . $CONSENT_FILE
elif [ -z "$USER_CONSENT" ];then
    get_tracking_consent
fi
. $CONSENT_FILE


RC_FILE="/etc/kaltura.d/system.ini"
if [ ! -r "$RC_FILE" ];then
    echo -e "${BRIGHT_RED}ERROR: could not find $RC_FILE so, exiting..${NORMAL}"
    exit 2
fi
. $RC_FILE

if [ -n "$1" -a -r "$1" ];then
    ANSFILE=$1
    . $ANSFILE
fi


MEDIA_SERVER_DIR="$BASE_DIR/media-server"

cd $MEDIA_SERVER_DIR
echo -e "${BRIGHT_BLUE}Running ant configuration${NORMAL}"
ant
/etc/init.d/WowzaStreamingEngine stop >> /dev/null 2>&1
/etc/init.d/WowzaStreamingEngine start
php $MEDIA_SERVER_DIR/register_media_server.php
RC=$?

if [ "$RC" -eq "0" ] || [ "$RC" -eq "255" ]; then
    send_install_becon `basename $0` $ZONE install_success 0
else
    send_install_becon `basename $0` $ZONE install_fail "$RC"
fi
