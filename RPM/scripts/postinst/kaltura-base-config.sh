#!/bin/bash - 
#===============================================================================
#          FILE: kaltura-base-config.sh
#         USAGE: ./kaltura-base-config.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy, <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 01/06/14 11:27:00 EST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error
verify_user_input()
{
        ANSFILE=$1
	. $ANSFILE
        for VAL in TIME_ZONE KALTURA_FULL_VIRTUAL_HOST_NAME KALTURA_VIRTUAL_HOST_NAME DB1_HOST DB1_PORT DB1_NAME DB1_USER DB1_PASS SERVICE_URL SPHINX_SERVER1 SPHINX_SERVER2 DWH_HOST DWH_PORT SPHINX_DB_HOST SPHINX_DB_PORT ; do
                if [ -z "${!VAL}" ];then
                        echo "I need $VAL in $ANSFILE."
                        exit 1
                fi
        done
}

KALT_CONF_DIR='/opt/kaltura/app/configurations/'
if [ -n "$1" -a -r "$1" ];then
        ANSFILE=$1
        verify_user_input $ANSFILE
else
        echo "Welcome to Kaltura Server `rpm -qa kaltura-base --queryformat %{version}` post install setup.
In order to finalize the system configuration, please input the following:

CDN host [`hostname`]:"
        read -e CDN_HOST
        if [ -z "$CDN_HOST" ];then
                CDN_HOST=`hostname`
		#echo $CDN_HOST
        fi

        echo "Apache virtual host [`hostname`]: "
        read -e KALTURA_VIRTUAL_HOST_NAME
        if [ -z "$KALTURA_VIRTUAL_HOST_NAME" ];then
                KALTURA_VIRTUAL_HOST_NAME=`hostname`
		#echo $KALTURA_VIRTUAL_HOST_NAME
        fi

        echo "Which port will this Vhost listen on [443]? "
        read -e KALTURA_VIRTUAL_HOST_PORT
        if [ -z "$KALTURA_VIRTUAL_HOST_PORT" ];then
                KALTURA_VIRTUAL_HOST_PORT=443
		#echo $KALTURA_VIRTUAL_HOST_PORT
        fi
        KALTURA_FULL_VIRTUAL_HOST_NAME="$KALTURA_VIRTUAL_HOST_NAME:$KALTURA_VIRTUAL_HOST_PORT"

        while [ -z "$DB1_HOST" ];do
                echo "DB hostname: "
                read -e DB1_HOST
        done

        echo "DB port [3306]: "
        read -e DB1_PORT
        if [ -z "$DB1_PORT" ];then
                DB1_PORT=3306
        fi

	echo "Analytics DB hostname [$DB1_HOST]:"
	read -e DWH_HOST
	if [ -z "$DWH_HOST" ];then
		DWH_HOST=$DB1_HOST
	fi

	echo "Analytics DB port [$DB1_PORT]:"
	read -e DWH_PORT
	if [ -z "$DWH_PORT" ];then
		DWH_PORT=$DB1_PORT
		#echo $DWH_PORT
	fi

        while [ -z "$SPHINX_SERVER1" ];do
                echo "Sphinx host: "
                read -e SPHINX_SERVER1
        done

        while [ -z "$SPHINX_SERVER2" ];do
                echo "Secondary Sphinx host: "
                read -e SPHINX_SERVER2
        done

        while [ -z "$SERVICE_URL" ];do
                echo "Service URL: "
                read -e SERVICE_URL
        done
	echo "Generating a 15 chars random passwd.."
	DB1_PASS=`< /dev/urandom tr -dc A-Za-z0-9_ | head -c15`

        while [ -z "$TIME_ZONE" ];do
                echo "Your time zone [see http://php.net/date.timezone]: "
                read -e TIME_ZONE
        done
fi


# go over all conf files that are not templates.
CONF_FILES=`find $KALT_CONF_DIR  -type f|grep -v template`

# if there's no db.ini file in place, copy the template 
if [ ! -r "$KALT_CONF_DIR/db.ini" ];then
	cp $KALT_CONF_DIR/db.template.ini $KALT_CONF_DIR/db.ini
fi
# Now we will sed.

#user = @DWH_USER@
#port = @DWH_PORT@
#password = @DWH_PASS@

for CONF_FILE in $CONF_FILES;do
	sed -i -e "s#@CDN_HOST@#$CDN_HOST#g" -e "s#@DB[1-9]_HOST@#$DB1_HOST#g" -e "s#@DB[1-9]_NAME@#kaltura#g" -e "s#@DB[1-9]_USER@#kaltura#g" -e "s#@DB[1-9]_PASS@#$DB1_PASS#g" -e "s#@DB[1-9]_PORT@#$DB1_PORT#g" -e "s#@TIME_ZONE@#$TIME_ZONE#g" -e "s#@KALTURA_FULL_VIRTUAL_HOST_NAME@#$KALTURA_FULL_VIRTUAL_HOST_NAME#g" -e "s#@KALTURA_VIRTUAL_HOST_NAME@#$KALTURA_VIRTUAL_HOST_NAME#g" -e "s#@SERVICE_URL@#$SERVICE_URL#g" -e "s#@WWW_HOST@#`hostname`#g" -e "s#@SPHINX_DB_NAME@#kaltura_sphinx_log#g" -e "s#@SPHINX_DB_HOST@#$DB1_HOST#g" -e "s#@SPHINX_DB_PORT@#$DB1_PORT#g" -e "s#@DWH_HOST@#$DWH_HOST#g" -e "s#@DWH_PORT@#$DWH_PORT#g" -e "s#@SPHINX_SERVER1@#$SPHINX_SERVER1#g" -e "s#@SPHINX_SERVER2@#$SPHINX_SERVER2#g" -e "s#@DWH_DATABASE_NAME@#kalturadw#g" $CONF_FILES 
done

