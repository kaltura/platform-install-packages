#!/bin/bash - 
#===============================================================================
#          FILE: kaltura-push-server-config.sh
#         USAGE: ./kaltura-push-server-config.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
#       LICENSE: AGPLv3+
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
        for VAL in RABBIT_MQ_SERVER RABBIT_USER RABBIT_PASSWD RABBIT_MQ_SERVER_HOSTS SOCKET_IO_PORT TOKEN_KEY TOKEN_IV ; do
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
                send_install_becon kaltura-push-server $ZONE "install_fail"  "$OUT"
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
if ! rpm -q kaltura-push-server;then
        echo -e "${BRIGHT_BLUE}Skipping as kaltura-push-server is not installed.${NORMAL}"
        exit 0 
fi
PUSH_SERVER_PREFIX=/opt/kaltura/push-server

if [ -n "$1" -a -r "$1" ];then
        ANSFILE=$1
        verify_user_input $ANSFILE
        . $ANSFILE
        export ANSFILE
else
                echo -e "${CYAN}RabbitMQ hostname [`hostname`]:${NORMAL} "
                read RABBIT_MQ_SERVER
                if [ -z "$RABBIT_MQ_SERVER" ];then
                        RABBIT_MQ_SERVER=`hostname`
                fi
                echo -e "${CYAN}RabbitMQ username${NORMAL}"
                read RABBIT_USER

                echo -e "${CYAN}RabbitMQ passwd:${NORMAL}"
                read -s RABBIT_PASSWD

                echo -e "${CYAN}Comma separated RabbitMQ hosts [$RABBIT_MQ_SERVER:5672]:${NORMAL}"
                read RABBIT_MQ_SERVER_HOSTS
                if [ -z "$RABBIT_MQ_SERVER_HOSTS" ];then
                        RABBIT_MQ_SERVER_HOSTS=$RABBIT_MQ_SERVER:5672
                fi
                echo -e "${CYAN}Push Server port [8888]:${NORMAL}"
                read SOCKET_IO_PORT
                if [ -z "$SOCKET_IO_PORT" ];then
                        SOCKET_IO_PORT=8888
                fi
                echo -e "${CYAN}Push Server secret:${NORMAL}"
                read -s TOKEN_KEY
                echo -e "${CYAN}Push Server secret IV:${NORMAL}"
                read -s TOKEN_IV
fi

export RABBIT_USER RABBIT_PASSWD 
/opt/kaltura/push-server/bin/configure-rabbitmq.sh

sed -e "s#@LOG_DIR@#$PUSH_SERVER_PREFIX/log#g" -e "s#@QUEUE_NAME@#`hostname`#g" -e "s#@EXCHANGE@#kaltura_exchange#g" -e "s#@RABBIT_MQ_SERVER@#$RABBIT_MQ_SERVER#g" -e "s#@RABBIT_MQ_USERNAME@#$RABBIT_USER#g" -e "s#@RABBIT_MQ_PASSWORD@#$RABBIT_PASSWD#g" -e "s#@RABBIT_MQ_SERVER_HOSTS@#$RABBIT_MQ_SERVER_HOSTS#g" -e "s#@SOCKET_IO_PORT@#$SOCKET_IO_PORT#g" -e "s#@TOKEN_KEY@#$TOKEN_KEY#g" -e "s#@TOKEN_IV@#$TOKEN_IV#g" $PUSH_SERVER_PREFIX/config/config.ini.template > $PUSH_SERVER_PREFIX/config/config.ini

service kaltura-push-server restart
