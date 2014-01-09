#!/bin/bash - 
#===============================================================================
#          FILE: kaltura-db-config.sh
#         USAGE: ./kaltura-db-config.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy (), <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 01/09/14 04:57:40 EST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error
verify_user_input()
{
        ANSFILE=$1
        for VAL in DB1_HOST DB1_PORT DB1_NAME DB1_USER DB1_PASS ; do
                if [ -z "${!VAL}" ];then
                        echo "I need $VAL in $ANSFILE."
                        exit 1
                fi
        done
}
if [ -n "$1" -a -r "$1" ];then
        ANSFILE=$1
        verify_user_input $ANSFILE
else
        echo "Welcome to Kaltura Server `rpm -qa kaltura-base --queryformat %{version}` post install setup.
In order to finalize the system configuration, please input the following:"

        while [ -z "$DB1_HOST" ];do
                echo "DB hostname: "
                read -e DB1_HOST
        done

        echo "DB name [kaltura]: "
        read -e DB1_NAME
        if [ -z "$DB1_NAME" ];then
                DB1_NAME=kaltura
        fi

        while [ -z "$DB_SUPER_USER" ];do
                echo "DB super user [used to create the kaltura user and scheme]: "
                read -e DB_SUPER_USER
        done
        while [ -z "$DB_SUPER_PASS" ];do
                echo "DB super user passwd: "
                STTY_ORIG=`stty -g`
                stty -echo
                read -e DB_SUPER_PASS
                stty $STTY_ORIG

        done
        while [ -z "$DB1_USER" ];do
                echo "Kaltura DB user: "
                read -e DB1_USER
        done
	DB1_PASS=`< /dev/urandom tr -dc A-Za-z0-9_ | head -c15`
fi

# now replace config tokens and run SQL creation scripts.
