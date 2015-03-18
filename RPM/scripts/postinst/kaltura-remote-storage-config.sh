#!/bin/bash - 
#===============================================================================
#          FILE: kaltura-remote-storage-config.sh
#         USAGE: ./kaltura-remote-storage-config.sh 
#   DESCRIPTION: Auto config a remote storage profile
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 03/30/14 09:07:54 EDT
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
RC_FILE=/etc/kaltura.d/system.ini
if [ ! -r "$RC_FILE" ];then
	echo -e "${BRIGHT_RED}ERROR: could not find $RC_FILE so, exiting..${NORMAL}"
	exit 1 
fi
. $RC_FILE


echo -e "${BRIGHT_BLUE}Welcome to the remote storage configuration script!${NORMAL}"
while [ -z "$PARTNERID" ];do
	echo -e "${CYAN}Please enter the partner id of the Kaltura account you'd like to configure the CDN for, or enter ALL (in caps) to set it as the default for all accounts:${NORMAL}"
	read -e PARTNERID
done
echo -e "${CYAN}Please enter your admin console user email address [$ADMIN_CONSOLE_ADMIN_MAIL]:${NORMAL}"
read -e MINUS2_MAIL
if [ -z "$MINUS2_MAIL" ];then
	MINUS2_MAIL=$ADMIN_CONSOLE_ADMIN_MAIL
fi
echo -e "${CYAN}Please enter the password you use to login to the admin console:${NORMAL}"
read -e MINUS2_PASSWD
while [ -z "$STOR_TYPE" ];do
	echo -e "${CYAN}Please input storage type:
0. Amazon S3
1. Akamai
${NORMAL}"
	read -e STOR_TYPE
done
if [ "$STOR_TYPE" -ne 0 ];then
	echo -e "${CYAN}Please choose the protocol you'd like to use to upload to the remote storage profile [SFTP]:
	SFTP
	FTP
	SCP
	S3 [Amazon]${NORMAL}"
	read -e PROTOCOL
	if [ -z "$PROTOCOL" ];then
		PROTOCOL='SFTP'
	fi
else
	PROTOCOL=S3
fi
echo -e "${CYAN}Please input storage display name [My storage profile]:${NORMAL}"
read -e STOR_DISPLAY_STRING
if [ -z "$STOR_DISPLAY_STRING" ];then
	STOR_DISPLAY_STRING="My storage profile"
fi
while [ -z "$STOR_URL" ];do
	echo -e "${CYAN}Please input storage hostname:${NORMAL}"
	read -e STOR_URL
done

echo -e "${CYAN}Please enter the directory on the remote storage server where the Kaltura files will be stored [/]:${NORMAL}"
read -e STOR_BASE_DIR
if [ -z "$STOR_BASE_DIR" ];then
	STOR_BASE_DIR="/"
fi

while [ -z "$STOR_HTTP_DELIVERY_URL" ];do
	echo -e "${CYAN}Please enter the CDN HTTP url from which the Kaltura player will perform playback:${NORMAL}"
	read -e STOR_HTTP_DELIVERY_URL
done

echo -e "${CYAN}Please enter the CDN HTTPS url from which the Kaltura player will perform playback:${NORMAL}"
read -e STOR_HTTPS_DELIVERY_URL
echo -e "${CYAN}Please enter the CDN RTMP url from which the Kaltura player will perform playback:${NORMAL}"
read -e STOR_RTMP_DELIVERY_URL

while [ -z "$STOR_USER" ];do
	echo -e "${CYAN}Please input storage account username:${NORMAL}"
	read -e STOR_USER
done

while [ -z "$STOR_PASSWD" ];do
	echo -e "${CYAN}Please input storage account passwd:${NORMAL}"
	read -e STOR_PASSWD
done

# make the API call to create it
php `dirname $0`/kaltura-remote-storage-config.php $SERVICE_URL $PARTNERID $MINUS2_MAIL $MINUS2_PASSWD $PROTOCOL "$STOR_DISPLAY_STRING" $STOR_URL $STOR_BASE_DIR $STOR_HTTP_DELIVERY_URL $STOR_USER $STOR_PASSWD $STOR_TYPE

if [ $? -eq 0 ]; then
	echo -e "${BRIGHT_BLUE}$STOR_DISPLAY_STRING successfully configured.${NORMAL}"
	# are we Akamai?
	if [ $STOR_TYPE = 1 ];then
		/opt/kaltura/bin/update_akamai_hls_flavor_tags.sh	
	fi
fi

