#!/bin/bash - 
#===============================================================================
#          FILE: kaltura-nginx-config.sh
#         USAGE: ./kaltura-nginx-config.sh 
#   DESCRIPTION: configure server as an Nginx  node.
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
        for VAL in WWW_HOST VOD_PACKAGER_HOST VOD_PACKAGER_PORT ; do
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
                send_install_becon kaltura-nginx $ZONE "install_fail"  "$OUT"
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
if ! rpm -q kaltura-nginx;then
	echo -e "${BRIGHT_BLUE}Skipping as kaltura-nginx is not installed.${NORMAL}"
	exit 0 
fi

if [ -n "$1" -a -r "$1" ];then
        ANSFILE=$1
        verify_user_input $ANSFILE
        . $ANSFILE
        export ANSFILE
else
	echo -e "${CYAN}Kaltura API host [${YELLOW}`hostname`${CYAN}]:${NORMAL} "
	read -e WWW_HOST
	if [ -z "$WWW_HOST" ];then
		WWW_HOST=`hostname`
	fi

	echo -e "${CYAN}Nginx server name [${YELLOW}`hostname`${CYAN}]:${NORMAL} "
	read -e VOD_PACKAGER_HOST
	if [ -z "$VOD_PACKAGER_HOST" ];then
		VOD_PACKAGER_HOST=`hostname`
	fi

	echo -en "${CYAN}Nginx port to listen on [${YELLOW}88${CYAN}]:${NORMAL} "
	read -e VOD_PACKAGER_PORT
	if [ -z "$VOD_PACKAGER_PORT" ];then
		VOD_PACKAGER_PORT=88
	fi
fi
if [ -f /etc/nginx/nginx.conf ];then
	mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.old
fi
sed -e 's#@STATIC_FILES_PATH@#/etc/nginx/static#g' -e "s#@VOD_PACKAGER_HOST@#$VOD_PACKAGER_HOST#g" -e "s#@VOD_PACKAGER_PORT@#$VOD_PACKAGER_PORT#g" -e "s#@LOG_DIR@#/var/log/nginx#" -e "s#@WWW_HOST@#$WWW_HOST#g" /etc/nginx/conf.d/kaltura.conf.template > /etc/nginx/nginx.conf

chkconfig kaltura-nginx on
if service kaltura-nginx status >/dev/null 2>&1;then
	service kaltura-nginx reload
else
	service kaltura-nginx start
fi

