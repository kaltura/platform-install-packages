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
#        AUTHOR: Tan-Tan <jonathan.kanarek@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 14/12/14
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error
# functions

function read_user_var_input() {
    TEMP_VAR=""  # Note that this is the var which will be used as a returned val
    echo -e "${CYAN}Please enter $1. Enter 'QUIT' in order to quit.${NORMAL}"
    read -e TEMP_VAR
    while [ -z "$TEMP_VAR" ];do
        echo -en "${CYAN}$1 var cannot be empty${NORMAL}\n"
        read TEMP_VAR
    done
    [[ "$TEMP_VAR" == "QUIT" ]] && echo -e "${BRIGHT_RED}Exiting due to user request${NORMAL}" && exit 10 # We quit if the user requests it
}


function check_mandatory_vars() {
    for item in $MANDATORY_VARS_LIST; do
        if [ -z "${!item}" ]; then
            read_user_var_input $item
            eval $item=$TEMP_VAR
        fi
    done
}

function send_fail_beacon_and_exit() {
    MESSAGE=$1
    RC=$2
    echo -e "${BRIGHT_RED}$MESSAGE${NORMAL}"
    send_install_becon kaltura-base $ZONE "install_fail" "$MESSAGE"
    exit $RC
}


KALTURA_FUNCTIONS_RC=`dirname $0`/kaltura-functions.rc
if [ ! -r "$KALTURA_FUNCTIONS_RC" ];then
    OUT="Could not find $KALTURA_FUNCTIONS_RC so, exiting.."
    echo $OUT
    RC=3
fi
. $KALTURA_FUNCTIONS_RC

if [ -r $CONSENT_FILE ];then
    . $CONSENT_FILE
elif [ -z "$USER_CONSENT" ];then
    get_tracking_consent
fi
. $CONSENT_FILE


RC_FILE="/etc/kaltura.d/system.ini"
if [ ! -r "$RC_FILE" ];then
    echo -e "${BRIGHT_RED}ERROR: could not find $RC_FILE so, exiting..${NORMAL}"
    RC=2
fi
. $RC_FILE

if [ -n "$1" -a -r "$1" ];then
    ANSFILE=$1
    . $ANSFILE
fi

# # VARS
MANDATORY_VARS_LIST="MEDIA_SERVER_DOMAIN_NAME PRIMARY_MEDIA_SERVER_HOST KALTURA_FULL_VIRTUAL_HOST_NAME"
BROADCAST_TEMPLATE_FILE=$APP_DIR/configurations/broadcast.template.ini
BROADCAST_FILE=$APP_DIR/configurations/broadcast.ini
TEMP_BROADCAST="/tmp/"`basename $BROADCAST_FILE`
HTTP_DEFAULT_PORT="80"
HTTPS_DEFAULT_PORT="443"
MEDIA_SERVERS_INI_TEMPLATE="$APP_DIR/configurations/media_servers.template.ini"
MEDIA_SERVERS_INI="$APP_DIR/configurations/media_servers.ini"


if [ ! -r "$BROADCAST_TEMPLATE_FILE" ];then
    send_fail_beacon_and_exit "ERROR: could not find $BROADCAST_TEMPLATE_FILE so, exiting.." 5
fi

if [ ! -r "$APP_DIR/configurations/media_servers.template.ini" ]; then
    send_fail_beacon_and_exit "$APP_DIR/configurations/media_servers.template.ini was not found. Exiting." 1
fi

# Checking if any mandatory vars are missing.
check_mandatory_vars

if [ "$SECONDARY_MEDIA_SERVER_HOST" == "$PRIMARY_MEDIA_SERVER_HOST" ];
then
    send_fail_beacon_and_exit "PRIMARY_MEDIA_SERVER_HOST and SECONDARY_MEDIA_SERVER_HOST cannot be the same. Please fix and re-run" 21
fi

if [ ! -r /opt/kaltura/app/base-config.lock ];then
    `dirname $0`/kaltura-base-config.sh "$ANSFILE"
    if [ $? -ne 0 ];then
        send_fail_beacon_and_exit "ERROR: Base config failed. Please correct and re-run $0." 22
    fi
else
    echo -e "${BRIGHT_BLUE}base-config completed successfully, if you ever want to re-configure your system (e.g. change DB hostname) run the following script:
# rm /opt/kaltura/app/base-config.lock
# $BASE_DIR/bin/kaltura-base-config.sh
${NORMAL}
"
fi

echo -e "${BRIGHT_BLUE}Setting up broadcast.ini${NORMAL}"
cp $BROADCAST_TEMPLATE_FILE $TEMP_BROADCAST
BROADCAST_FILE_TEMP=/tmp/temp_broadcast_line_removal
if [ -z "$SECONDARY_MEDIA_SERVER_HOST" ]; 
then 
    echo -e "${CYAN}'SECONDARY_MEDIA_SERVER_HOST' is not set. Type 'y' for yes or 'n' for leaving it empty${NORMAL}"
    TEMP_VAR=""
    while [ "$TEMP_VAR" != 'n' ] && [ "$TEMP_VAR" != 'y' ]; 
    do
        read_user_var_input "please type 'y' or 'n'"
    done
    if [ "$TEMP_VAR" == 'y' ];then
        read_user_var_input "Enter 'SECONDARY_MEDIA_SERVER_HOST' value in order to configure it."
        SECONDARY_MEDIA_SERVER_HOST=$TEMP_VAR
    else  # temp file for line removal
        echo -e "${YELLOW}Warning: SECONDARY_MEDIA_SERVER_HOST was not defined. In case this is not correct, please run '$0' again${NORMAL}"
        # 4 line removal of the secondary media server  in case it's empty / the same as the primary (thus turned empty by the script)
        START_LINE=`grep -n @SECONDARY_MEDIA_SERVER_HOST@ $TEMP_BROADCAST | cut -d':' -f1`
        START_LINE=`expr $START_LINE - 1`
        BLOCK_OFFSET=4
        awk -v start_line=$START_LINE -v end_line=`expr $START_LINE + $BLOCK_OFFSET` '{
            if (NR < start_line || NR > end_line)
                print $0 
        }' $TEMP_BROADCAST > $BROADCAST_FILE_TEMP
        [ -f $BROADCAST_FILE_TEMP ] && mv $BROADCAST_FILE_TEMP $TEMP_BROADCAST
    fi
fi

# sed for broadcast.ini
sed -i -e "s/@KALTURA_FULL_VIRTUAL_HOST_NAME@/$KALTURA_FULL_VIRTUAL_HOST_NAME/g" \
    -e "s/@PRIMARY_MEDIA_SERVER_HOST@/$PRIMARY_MEDIA_SERVER_HOST/g" \
    -e "s/@SECONDARY_MEDIA_SERVER_HOST@/$SECONDARY_MEDIA_SERVER_HOST/g" $TEMP_BROADCAST
mv $TEMP_BROADCAST $BROADCAST_FILE 

# Tending to media_server.ini now
echo -e "${BRIGHT_BLUE}Setting up media_server.ini${NORMAL}"
temp_media_server_ini="/tmp/"`basename $MEDIA_SERVERS_INI`
cp $MEDIA_SERVERS_INI_TEMPLATE $temp_media_server_ini
if [ "$PROTOCOL" == "http" ]; then
    sed -i -e "s/@HTTP_PORT@/$KALTURA_VIRTUAL_HOST_PORT/g" \
    -e "s/@HTTPS_PORT@/$HTTPS_DEFAULT_PORT/g" \
    -e "s/@MEDIA_SERVER_DOMAIN@/$MEDIA_SERVER_DOMAIN_NAME/g" $temp_media_server_ini
else
    sed -i -e "s/@HTTPS_PORT@/$KALTURA_VIRTUAL_HOST_PORT/g" \
    -e "s/@HTTP_PORT@/$HTTP_DEFAULT_PORT/g" \
    -e "s/@MEDIA_SERVER_DOMAIN@/$MEDIA_SERVER_DOMAIN_NAME/g" $temp_media_server_ini
fi
mv $temp_media_server_ini $MEDIA_SERVERS_INI

echo -e "${BRIGHT_BLUE}The setup was finished successfully.${NORMAL}"
send_install_becon `basename $0` $ZONE install_start 0
send_install_becon `basename $0` $ZONE install_success 0