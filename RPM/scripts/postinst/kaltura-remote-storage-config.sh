#!/bin/bash - 
#===============================================================================
#          FILE: kaltura-remote-storage-config.sh
#         USAGE: ./kaltura-remote-storage-config.sh 
#   DESCRIPTION: Auto config a remote storage profile
#       OPTIONS: ---
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
	echo 'Usage: ' . __FILE__ . ' <service_url> <partner_id> <partner_secret> <FTP|SFTP|SCP|S3> <storage_display_name> <storage_url> <storage_base_dir> <delivery_url> <username> <passwd> <storage_type>'."\n";

echo -e "${BRIGHT_BLUE}Welcome to the remote storage configuration script!${NORMAL}"
echo -e "${CYAN}Please input the partner ID for which to configure the account [all partners]:"
read PARTNERID
if [ -z "$PARTNERID" ];then
	PARTNERID='ALL'
else 
	echo -e "${CYAN}Please input partner secret:${NORMAL}"
# might need to explain how to get the secret..
fi
echo -e "${CYAN}Please select one of the following protocls [0]:
0. SFTP
1. FTP
2. SCP
3. S3 [Amazon]${NORMAL}"
read PROTOCOL
if [ -z "$PROTOCOL" ];then
	PROTOCOL='SFTP'
fi
while [ -z "$STOR_URL" ];do
	echo -e "${CYAN}Please input storage URL:
0. Amazon S3
1. Akamai
${NORMAL}"
	read STOR_TYPE
done

echo -e "${CYAN}Please input storage display name [My $STOR_TYPE over $PROTOCOL]:${NORMAL}"
read STOR_DISPLAY_STRING
if [ -z "$STOR_DISPLAY_STRING" ];then
	STOR_DISPLAY_STRING="My $STOR_TYPE over $PROTOCOL"
fi
while [ -z "$STOR_URL" ];do
	echo -e "${CYAN}Please input storage URL:${NORMAL}"
	read STOR_URL
done

while [ -z "$STOR_BASE_DIR" ];do
	echo -e "${CYAN}Please input storage base dir:${NORMAL}"
	read STOR_BASE_DIR
done

while [ -z "$DELIVERY_URL" ];do
	echo -e "${CYAN}Please input delivery URL:${NORMAL}"
	read DELIVERY_URL
done
while [ -z "$STOR_USER" ];do
	echo -e "${CYAN}Please input storage account username:${NORMAL}"
	read STOR_USER
done

while [ -z "$STOR_PASSWD" ];do
	echo -e "${CYAN}Please input storage account passwd:${NORMAL}"
	read STOR_PASSWD
done
