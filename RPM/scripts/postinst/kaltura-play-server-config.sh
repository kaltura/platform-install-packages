#!/bin/bash - 
#===============================================================================
#          FILE: kaltura-play-server-config.sh
#         USAGE: ./kaltura-play-server-config.sh 
#   DESCRIPTION: configure server as a batch node.
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 01/02/14 09:23:34 EST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error
verify_user_input()
{
        ANSFILE=$1
        . $ANSFILE
        RC=0
        for VAL in SERVICE_URL PLAY_PARTNER_ADMIN_SECRET CLOUD_HOSTNAME CLOUD_SECRET  ; do
                if [ -z "${!VAL}" ];then
                        VALS="$VALS\n$VAL"
                        RC=1
                fi
        done
        if [ $RC -eq 1 ];then
                OUT="ERROR: Missing the following params in $ANSFILE
                $VALS
                "
                echo -en "${BRIGHT_RED}$OUT${NORMAL}\n"
                send_install_becon kaltura-play-server $ZONE "install_fail"  "$OUT"
                exit $RC 
        fi
}


KALTURA_FUNCTIONS_RC=`dirname $0`/kaltura-functions.rc
if [ ! -r "$KALTURA_FUNCTIONS_RC" ];then
	OUT="ERROR: Could not find $KALTURA_FUNCTIONS_RC so, exiting.."
	echo -e $OUT
	exit 3
fi
. $KALTURA_FUNCTIONS_RC
if ! rpm -q kaltura-play-server;then
	echo -e "${BRIGHT_BLUE}Skipping as kaltura-play-server is not installed.${NORMAL}"
	exit 0 
fi

if [ -n "$1" -a -r "$1" ];then
        ANSFILE=$1
        verify_user_input $ANSFILE
        . $ANSFILE
        export ANSFILE
else
                echo -e "${CYAN}Your Kaltura Service URL:
(Base URL where the Kaltura API and Apps will be accessed from - this would be your Load Balancer URL on a cluster or same as your virtual host in an all-in-one Kaltura server - Must be accessible from both inside the machine and from any clients / browsers that will use Kaltura):
${NORMAL} "
                read SERVICE_URL
                echo -e "${CYAN}Admin secret of partner -6:
Can be obtained with:
mysql> select admin_secret from kaltura.partner where id=-6;${NORMAL}"
		read PLAY_PARTNER_ADMIN_SECRET
		
		echo -e "${CYAN}Hostname of the cloud load balancer:${NORMAL}"
		read CLOUD_HOSTNAME 
	
		echo -e "${CYAN}Cloud secret [random string]:${NORMAL}"
		read CLOUD_SECRET
fi
PLAY_PREFIX=/opt/kaltura/play-server
sed -e "s#@CLOUD_SHARED_BASE_PATH@#$PLAY_PREFIX/share#g" -e "s#@LOG_DIR@#$PLAY_PREFIX/log#g" -e "s#@SERVICE_URL@#$SERVICE_URL#g" -e "s#@PLAY_PARTNER_ADMIN_SECRET@#$PLAY_PARTNER_ADMIN_SECRET#g" -e "s#@CLOUD_HOSTNAME@#$CLOUD_HOSTNAME#g" -e "s#@CLOUD_SECRET@#$CLOUD_SECRET#g" /opt/kaltura/play-server/config/user_input.ini.template > /opt/kaltura/play-server/config/user_input.ini 
