#!/bin/bash - 
#===============================================================================
#          FILE: kaltura-media-server-config.sh
#         USAGE: ./kaltura-media-server-config.sh 
#   DESCRIPTION: configure server as a media-server node.
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Tan-Tan <jonathan.kanarek@kaltura.com>
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


BROADCAST_TEMPLATE_FILE=$BASE_DIR/app/configurations/broadcast.template.ini
BROADCAST_FILE=$BASE_DIR/app/configurations/broadcast.ini
TEMP_BROADCAST=/tmp/temp_broadcast.ini
# In case no primary server is configured, there is no point running.

if [ -z $KALTURA_FULL_VIRTUAL_HOST_NAME ];
then
	echo -e "${BRIGHT_RED} KALTURA_FULL_VIRTUAL_HOST_NAME value was not found in $1 answer file. \nPlease fix the used answer file.${NORMAL}"
	exit 2
else
	echo "Copying broadcast.template.ini"
	cp $BROADCAST_TEMPLATE_FILE $TEMP_BROADCAST
	# Resetting the KALTURA_FULL_VIRTUAL_HOST_NAME after template copy
	sed -i s/@KALTURA_FULL_VIRTUAL_HOST_NAME@/$KALTURA_FULL_VIRTUAL_HOST_NAME/ $TEMP_BROADCAST
fi

# Setting the primary server setting. No point of continuing the setup in case there is no server.
if [ -z $PRIMARY_MEDIA_SERVER_HOST ]; then
	echo -e "${BRIGHT_RED}PRIMARY_MEDIA_SERVER_HOST value was not found in $1 answer file. \nPlease fix the $BROADCAST_FILE if needed.${NORMAL}"
	echo -e "You can fix this later by running kaltura-media-server-config.sh <answer file>\n"
	exit 2
else
	echo "Setting PRIMARY_MEDIA_SERVER_HOST"
	sed -i s/@PRIMARY_MEDIA_SERVER_HOST@/$PRIMARY_MEDIA_SERVER_HOST/ $TEMP_BROADCAST
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


# temp file for line removal
BROADCAST_FILE_TEMP=/tmp/temp_broadcast_line_removal
if [ -z $SECONDARY_MEDIA_SERVER_HOST ] ; 
then 
	echo -e "${BRIGHT_RED}Warning: SECONDARY_MEDIA_SERVER_HOST was not found in $1 answer file.\n ${NORMAL}"
	
	# 4 line removal of the secondary media server  in case it's empty / the same as the primary (thus turned empty by the script)
	START_LINE=`grep -n @SECONDARY_MEDIA_SERVER_HOST@ $TEMP_BROADCAST | cut -d':' -f1`
	START_LINE=`expr $START_LINE - 1`
	BLOCK_OFFSET=4
	awk -v start_line=$START_LINE -v end_line=`expr $START_LINE + $BLOCK_OFFSET` '{
	    if (NR < start_line || NR > end_line)
	        print $0 
	}' $TEMP_BROADCAST > $BROADCAST_FILE_TEMP
	[ -f $BROADCAST_FILE_TEMP ] && mv $BROADCAST_FILE_TEMP $TEMP_BROADCAST

elif [ $SECONDARY_MEDIA_SERVER_HOST == $PRIMARY_MEDIA_SERVER_HOST ];
then
	echo -e "${BRIGHT_RED}Warning: SECONDARY_MEDIA_SERVER_HOST & PRIMARY_MEDIA_SERVER_HOST have the same value in $1 answer file ($PRIMARY_MEDIA_SERVER_HOST). No secondary server will be configured under $BROADCAST_FILE."
	echo -e "You can fix this later by running kaltura-media-server-config.sh <answer file> ${NORMAL}"
	
	# Removing unneeded lines
	START_LINE=`grep -n @SECONDARY_MEDIA_SERVER_HOST@ $TEMP_BROADCAST | cut -d':' -f1`
	START_LINE=`expr $START_LINE - 1`
	BLOCK_OFFSET=4
	awk -v start_line=$START_LINE -v end_line=`expr $START_LINE + $BLOCK_OFFSET` '{
	    if (NR < start_line || NR > end_line)
	        print $0 
	}' $TEMP_BROADCAST > $BROADCAST_FILE_TEMP
	[ -f $BROADCAST_FILE_TEMP ] && mv $BROADCAST_FILE_TEMP $TEMP_BROADCAST
else
	echo "Setting SECONDARY_MEDIA_SERVER_HOST"
	sed -i s/@SECONDARY_MEDIA_SERVER_HOST@/$SECONDARY_MEDIA_SERVER_HOST/ $TEMP_BROADCAST
fi

if [ -f $TEMP_BROADCAST ]; then
	echo "Replacing $BROADCAST_FILE"
	mv $TEMP_BROADCAST $BROADCAST_FILE
fi


RC_FILE=/etc/kaltura.d/system.ini
if [ ! -r "$RC_FILE" ];then
	echo -e "${BRIGHT_RED}ERROR: could not find $RC_FILE so, exiting..${NORMAL}"
	exit 2
fi
. $RC_FILE


if [ ! -r "$BROADCAST_FILE" ];then
	echo -e "${BRIGHT_RED}ERROR: could not find $RC_FILE so, exiting..${NORMAL}"
	exit 2
fi

send_install_becon `basename $0` $ZONE install_start 0
cd $BASE_DIR/media-server
ant
/etc/init.d/WowzaStreamingEngine stop >> /dev/null 2>&1
/etc/init.d/WowzaStreamingEngine start
send_install_becon `basename $0` $ZONE install_success 0
