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
#        AUTHOR: Tan-Tan <kobi.michaeli@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 14/12/14
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

if [ -n "$1" -a -r "$1" ];then
    ANSFILE=$1
    . $ANSFILE
fi

if [ ! -r /opt/kaltura/app/base-config.lock ];then
    `dirname $0`/kaltura-base-config.sh "$ANSFILE"
    if [ $? -ne 0 ];then
        echo -e "${BRIGHT_RED}ERROR: Base config failed. Please correct and re-run $0.${NORMAL}"
        exit 21
    fi
else
    echo -e "${BRIGHT_BLUE}base-config completed successfully, if you ever want to re-configure your system (e.g. change DB hostname) run the following script:
# rm /opt/kaltura/app/base-config.lock
# $BASE_DIR/bin/kaltura-base-config.sh
${NORMAL}
"
fi

RC_FILE="/etc/kaltura.d/system.ini"
if [ ! -r "$RC_FILE" ];then
    echo -e "${BRIGHT_RED}ERROR: could not find $RC_FILE so, exiting..${NORMAL}"
    exit 2
fi
. $RC_FILE


MANDATORY_VARS_LIST="MEDIA_SERVER_DOMAIN_NAME PRIMARY_MEDIA_SERVER_HOST KALTURA_FULL_VIRTUAL_HOST_NAME"

function read_user_var_input() {
    TEMP_VAR=""  # Note that this is the var which will be used as a returned val
    echo -e "${CYAN}PLease enter $1. Enter 'QUIT' in order to quit.${NORMAL}"
    read -e TEMP_VAR
    while [ -z "$TEMP_VAR" ];do
        echo -en "${CYAN}$1 var cannot be empty${NORMAL}\n"
        read TEMP_VAR
    done
    [[ "$TEMP_VAR" == "QUIT" ]] && echo -e "${BRIGHT_RED}Exiting due to user request${NORMAL}" && exit 1 # We quit if the user requests it
}


function check_mandatory_vars () {
    for item in $MANDATORY_VARS_LIST; do
        if [ -z "${!item}" ]; then
            read_user_var_input $item
            eval $item=$TEMP_VAR
        fi
    done
}


MEDIA_SERVER_DIR="$BASE_DIR/media-server"

pushd $MEDIA_SERVER_DIR
echo -e "${CYAN}Running ant configuration${NORMAL}"
ant
/etc/init.d/WowzaStreamingEngine stop >> /dev/null 2>&1
/etc/init.d/WowzaStreamingEngine start
php register_media_server.php
popd

send_install_becon `basename $0` $ZONE install_start 0
send_install_becon `basename $0` $ZONE install_success 0

