#!/bin/bash - 
#===============================================================================
#          FILE: kaltura-nginx-config.sh
#         USAGE: ./kaltura-nginx-config.sh 
#   DESCRIPTION: configure server as an Nginx  node.
#       OPTIONS: ---
#   LICENSE: AGPLv3+
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
        for VAL in WWW_HOST VOD_PACKAGER_HOST ; do
            if [ -z "${!VAL}" ];then
                    VALS="$VALS\n$VAL"
                    RC=1
            fi
        done
        # Checking if at least one of the ports is defined
        if [ -z VOD_PACKAGER_PORT -a VOD_PACKAGER_SSL_PORT ]; then
            RC=1
        fi

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

    if [ "$VOD_PACKAGER_PORT" == "$VOD_PACKAGER_SSL_PORT" ]; then
        echo -e "${RED}The same port is used for nginx in both ssl and non-ssl mode. Please change one of them and run $0 again${NORMAL}"
        exit 4
    fi
else
    echo -e "${CYAN}Note that nginx can be configured to work in both ${YELLOW}ssl${CYAN} and ${YELLOW}non-ssl mode${NORMAL} "
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

    echo -e "${CYAN}Should nginx be configured in http mode? [${YELLOW}y/n${CYAN}]:${NORMAL} "
    read -e IS_VOD_PACKAGER_HTTP
    temp_var=`echo $IS_VOD_PACKAGER_HTTP | tr '[:upper:]' '[:lower:]'`
    IS_VOD_PACKAGER_HTTP=$temp_var
    if [ "$IS_VOD_PACKAGER_HTTP" != 'y' ] && [ "$IS_VOD_PACKAGER_HTTP" != 'n' ]; then
        echo -e "${BRIGHT_RED}The option can only be 'y' or 'n'. Please re-run${NORMAL}"
        exit 5
    fi

    if [ $IS_VOD_PACKAGER_HTTP == 'y' ]; then
        echo -en "${CYAN}Nginx port to listen on [${YELLOW}88${CYAN}]:${NORMAL} "
        read -e VOD_PACKAGER_PORT
        if [ -z "$VOD_PACKAGER_PORT" ];then
            VOD_PACKAGER_PORT=88
        fi
    fi

    echo -e "${CYAN}Should nginx be configured in https mode? [${YELLOW}y/n${CYAN}]:${NORMAL} "
    read -e IS_VOD_PACKAGER_SSL
    temp_var=`echo $IS_VOD_PACKAGER_SSL | tr '[:upper:]' '[:lower:]'`
    IS_VOD_PACKAGER_SSL=$temp_var
    if [ "$IS_VOD_PACKAGER_SSL" != 'y' ] && [ "$IS_VOD_PACKAGER_SSL" != 'n' ]; then
        echo -e "${BRIGHT_RED}The option can only be 'y' or 'n'. Please re-run${NORMAL}"
        exit 5
    fi

    if [ "$IS_VOD_PACKAGER_SSL" == 'y' ];then
        echo -e "${CYAN}Please input path to your SSL certificate[${YELLOW}/etc/ssl/certs/localhost.crt${CYAN}]:${NORMAL}"
        read -e CRT_FILE
        echo "crt file: $CRT_FILE"
        if [ -z "$CRT_FILE" ];then
                CRT_FILE="/etc/ssl/certs/localhost.crt"
        fi
        echo -e "${CYAN}Please input path to your SSL CA file or leave empty in case you have none${CYAN}:${NORMAL}"
        read -e KEY_FILE
        echo -e "${CYAN}Please input the nginx https port${CYAN}[${YELLOW}default port is 8008${CYAN}]:${NORMAL}:${NORMAL}"
        read -e VOD_PACKAGER_SSL_PORT
        if [ -z "$VOD_PACKAGER_SSL_PORT" ]; then
            VOD_PACKAGER_SSL_PORT=8008
            echo "No input was provided. Nginx https port will be $VOD_PACKAGER_SSL_PORT"
        fi
    fi

fi
if [ -f /etc/nginx/nginx.conf ];then
    mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.old
fi

cp /etc/nginx/conf.d/kaltura.conf.template /tmp/nginx.conf.tmp
# Removal according to the set vars
if [ -z "$VOD_PACKAGER_PORT" ] && [ ! -z "$VOD_PACKAGER_SSL_PORT" ]; then
    echo "Setting up non-ssl mode"
    sed -i -e '/listen @VOD_PACKAGER_PORT@;/d' /tmp/nginx.conf.tmp
fi  

if [ -z "$VOD_PACKAGER_SSL_PORT" ] && [ ! -z "$VOD_PACKAGER_PORT" ]; then
    echo "Setting up ssl mode"
    sed -i -e '/listen @VOD_PACKAGER_SSL_PORT@ ssl;/d' -e '/ssl_certificate_key @SSL_CERTIFICATE_CHAIN_FILE@;/d' -e '/ssl_certificate  @SSL_CERTIFICATE_FILE@;/d' /tmp/nginx.conf.tmp
fi

# The actual replacement
sed -i  -e "s#@VOD_PACKAGER_SSL_PORT@#$VOD_PACKAGER_SSL_PORT#g" -e "s#@VOD_PACKAGER_PORT@#$VOD_PACKAGER_PORT#g" -e "s#@SSL_CERTIFICATE_FILE@#$CRT_FILE#g" -e "s#@SSL_CERTIFICATE_CHAIN_FILE@#$KEY_FILE#g"  -e 's#@STATIC_FILES_PATH@#/etc/nginx/static#g' -e "s#@VOD_PACKAGER_HOST@#$VOD_PACKAGER_HOST#g" -e "s#@VOD_PACKAGER_SSL_PORT@#$VOD_PACKAGER_SSL_PORT#g" -e "s#@VOD_PACKAGER_PORT@#$VOD_PACKAGER_PORT#g" -e "s#@LOG_DIR@#/var/log/nginx#" -e "s#@WWW_HOST@#$WWW_HOST#g"  -e "s#@SSL_CERTIFICATE_FILE@#$CRT_FILE#g" -e "s#@SSL_CERTIFICATE_CHAIN_FILE@#$KEY_FILE#g" /tmp/nginx.conf.tmp
mv /tmp/nginx.conf.tmp /etc/nginx/nginx.conf

chkconfig kaltura-nginx on
if service kaltura-nginx status >/dev/null 2>&1;then
    service kaltura-nginx reload
else
    service kaltura-nginx start
fi




