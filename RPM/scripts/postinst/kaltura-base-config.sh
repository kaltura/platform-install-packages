#!/bin/bash -e 
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
        for VAL in TIME_ZONE KALTURA_FULL_VIRTUAL_HOST_NAME KALTURA_VIRTUAL_HOST_NAME DB1_HOST DB1_PORT DB1_NAME DB1_USER SERVICE_URL SPHINX_SERVER1 SPHINX_SERVER2 DWH_HOST DWH_PORT SPHINX_DB_HOST SPHINX_DB_PORT ADMIN_CONSOLE_ADMIN_MAIL SUPER_USER SUPER_USER_PASSWD; do
                if [ -z "${!VAL}" ];then
                        echo "I need $VAL in $ANSFILE."
                        exit 1
                fi
        done
}

create_answer_file()
{
        for VAL in TIME_ZONE KALTURA_FULL_VIRTUAL_HOST_NAME KALTURA_VIRTUAL_HOST_NAME DB1_HOST DB1_PORT DB1_PASS DB1_NAME DB1_USER SERVICE_URL SPHINX_SERVER1 SPHINX_SERVER2 DWH_HOST DWH_PORT SPHINX_DB_HOST SPHINX_DB_PORT ADMIN_CONSOLE_ADMIN_MAIL; do
                if [ -n "${!VAL}" ];then
			echo "$VAL=${!VAL}" >> /tmp/kaltura_`date +%d_%m_%H_%M`.ans
                        
                fi
        done
	echo "
Answer file written to /tmp/kaltura_`date +%d_%m_%H_%M`.ans
You can use it to install the other hosts in your cluster.
"

}

DISPLAY_NAME="Kaltura Server `rpm -qa kaltura-base --queryformat %{version}`"
KALT_CONF_DIR='/opt/kaltura/app/configurations/'
if [ -n "$1" -a -r "$1" ];then
        ANSFILE=$1
        verify_user_input $ANSFILE
else
        echo "Welcome to Kaltura Server $DISPLAY_NAME post install setup.
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

        while [ -z "$SUPER_USER" ];do
                echo "MySQL super user [this is only for setting the kaltura user passwd and WILL NOT be used with the application]: "
                read -e SUPER_USER
        done
        while [ -z "$SUPER_USER_PASSWD" ];do
                echo "MySQL super user passwd [this is only for setting the kaltura user passwd and WILL NOT be used with the application]: "
                read -e SUPER_USER_PASSWD
        done

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
	
	echo "Secondary Sphinx host: "
	read -e SPHINX_SERVER2
	if [ -z $SPHINX_SERVER2 ];then
		SPHINX_SERVER2=" "
	fi

        while [ -z "$SERVICE_URL" ];do
                echo "Service URL: "
                read -e SERVICE_URL
        done
        while [ -z "$ADMIN_CONSOLE_ADMIN_MAIL" ];do
                echo "Admin's mail address for alerts: "
                read -e ADMIN_CONSOLE_ADMIN_MAIL
        done
        while [ -z "$TIME_ZONE" ];do
                echo "Your time zone [see http://php.net/date.timezone]: "
                read -e TIME_ZONE
        done
sed -i "s#\(date.timezone\)\s*=.*#\1='$TIME_ZONE'#g" /etc/php.ini /etc/php.d/*kaltura*ini
fi
if [ -z "$DB1_PASS" ];then
	DB1_PASS=`< /dev/urandom tr -dc A-Za-z0-9_ | head -c15`
	echo "update mysql.user set password=PASSWORD('$DB1_PASS') WHERE user='kaltura';flush PRIVILEGES" | mysql -h$DB1_HOST -P3306 -u$SUPER_USER -p$SUPER_USER_PASSWD mysql
fi
create_answer_file
DB1_NAME=kaltura
DB1_USER=kaltura

# no added value in putting this on a separate server..
SPHINX_DB_HOST=$DB1_HOST
SPHINX_DB_PORT=$DB1_PORT

CONF_FILES=`find $KALT_CONF_DIR  -type f -name "*template*"`
BASE_DIR=/opt/kaltura
# Now we will sed.

for TMPL_CONF_FILE in $CONF_FILES;do
	CONF_FILE=`echo $TMPL_CONF_FILE | sed 's@\(.*\)\.template\(.*\)@\1\2@'`
#	echo $CONF_FILE
	cp $TMPL_CONF_FILE $CONF_FILE
	sed -e "s#@CDN_HOST@#$CDN_HOST#g" -e "s#@DB[1-9]_HOST@#$DB1_HOST#g" -e "s#@DB[1-9]_NAME@#$DB1_NAME#g" -e "s#@DB[1-9]_USER@#$DB1_USER#g" -e "s#@DB[1-9]_PASS@#$DB1_PASS#g" -e "s#@DB[1-9]_PORT@#$DB1_PORT#g" -e "s#@TIME_ZONE@#$TIME_ZONE#g" -e "s#@KALTURA_FULL_VIRTUAL_HOST_NAME@#$KALTURA_FULL_VIRTUAL_HOST_NAME#g" -e "s#@KALTURA_VIRTUAL_HOST_NAME@#$KALTURA_VIRTUAL_HOST_NAME#g" -e "s#@SERVICE_URL@#$SERVICE_URL#g" -e "s#@WWW_HOST@#`hostname`#g" -e "s#@SPHINX_DB_NAME@#kaltura_sphinx_log#g" -e "s#@SPHINX_DB_HOST@#$SPHINX_DB_HOST#g" -e "s#@SPHINX_DB_PORT@#$DB1_PORT#g" -e "s#@DWH_HOST@#$DWH_HOST#g" -e "s#@DWH_PORT@#$DWH_PORT#g" -e "s#@SPHINX_SERVER1@#$SPHINX_SERVER1#g" -e "s#@SPHINX_SERVER2@#$SPHINX_SERVER2#g" -e "s#@DWH_DATABASE_NAME@#kalturadw#g" -e "s#@DWH_USER@#etl#g" -e "s#@DWH_PASS@#$DB1_PASS#g" -e "s#@ADMIN_CONSOLE_ADMIN_MAIL@#$ADMIN_CONSOLE_ADMIN_MAIL#g" -e "s#@WEB_DIR@#$BASE_DIR/web#g" -e "s#@LOG_DIR@#$BASE_DIR/log#g" -e "s#/opt/kaltura/app#$BASE_DIR/app#g" -e "s#@PHP_BIN@#/usr/bin/php#g" -e "s#@OS_KALTURA_USER@#kaltura#g" -e "s#@BASE_DIR@#$BASE_DIR#" -e "s#@APP_DIR@#$BASE_DIR/app#" -i $CONF_FILE
done

# gen secrets
ADMIN_SECRET=`< /dev/urandom tr -dc A-Za-z0-9_ | head -c10`
HASHED_ADMIN_SECRET=`echo $ADMIN_SECRET|md5sum`
ADMIN_SECRET=`echo $HASHED_ADMIN_SECRET|awk -F " " '{print $1}'`

MONITOR_PARTNER_ADMIN_SECRET=`< /dev/urandom tr -dc A-Za-z0-9_ | head -c10`
HASHED_MONITOR_PARTNER_ADMIN_SECRET=`echo $HASHED_MONITOR_PARTNER_ADMIN_SECRET | md5sum`
MONITOR_PARTNER_ADMIN_SECRET=`echo $HASHED_MONITOR_PARTNER_ADMIN_SECRET | awk -F " " '{print $1}'` 

MONITOR_PARTNER_SECRET=`< /dev/urandom tr -dc A-Za-z0-9_ | head -c10`
HASHED_MONITOR_PARTNER_SECRET=`echo $HASHED_MONITOR_PARTNER_SECRET | md5sum`
MONITOR_PARTNER_SECRET=`echo $HASHED_MONITOR_PARTNER_SECRET | awk -F " " '{print $1}'` 

PARTNER_ZERO_ADMIN_SECRET=`< /dev/urandom tr -dc A-Za-z0-9_ | head -c10`
HASHED_PARTNER_ZERO_ADMIN_SECRET=`echo $PARTNER_ZERO_ADMIN_SECRET|md5sum`
PARTNER_ZERO_ADMIN_SECRET=`echo $HASHED_PARTNER_ZERO_ADMIN_SECRET|awk -F " " '{print $1}'`


BATCH_PARTNER_ADMIN_SECRET=`< /dev/urandom tr -dc A-Za-z0-9_ | head -c10`
HASHED_BATCH_PARTNER_ADMIN_SECRET=`echo $BATCH_PARTNER_ADMIN_SECRET|md5sum`
BATCH_PARTNER_ADMIN_SECRET=`echo $HASHED_BATCH_PARTNER_ADMIN_SECRET|awk -F " " '{print $1}'`

MEDIA_PARTNER_ADMIN_SECRET=`< /dev/urandom tr -dc A-Za-z0-9_ | head -c10`
HASHED_MEDIA_PARTNER_ADMIN_SECRET=`echo $MEDIA_PARTNER_ADMIN_SECRET|md5sum`
MEDIA_PARTNER_ADMIN_SECRET=`echo $HASHED_MEDIA_PARTNER_ADMIN_SECRET|awk -F " " '{print $1}'`

TEMPLATE_PARTNER_ADMIN_SECRET=`< /dev/urandom tr -dc A-Za-z0-9_ | head -c10`
HASHED_TEMPLATE_PARTNER_ADMIN_SECRET=`echo $TEMPLATE_PARTNER_ADMIN_SECRET|md5sum`
TEMPLATE_PARTNER_ADMIN_SECRET=`echo $HASHED_TEMPLATE_PARTNER_ADMIN_SECRET|awk -F " " '{print $1}'`

HOSTED_PAGES_PARTNER_ADMIN_SECRET=`< /dev/urandom tr -dc A-Za-z0-9_ | head -c10`
HASHED_HOSTED_PAGES_PARTNER_ADMIN_SECRET=`echo $HOSTED_PAGES_PARTNER_ADMIN_SECRET|md5sum`
HOSTED_PAGES_PARTNER_ADMIN_SECRET=`echo $HASHED_HOSTED_PAGES_PARTNER_ADMIN_SECRET|awk -F " " '{print $1}'`


# SQL statement files tokens:
for TMPL in `find /opt/kaltura/app/deployment/base/scripts/init_content/ -name "*template*"`;do
	DEST_FILE=`echo $TMPL | sed 's@\(.*\)\.template\(.*\)@\1\2@'`
	cp $TMPL $DEST_FILE
	sed -e "s#@WEB_DIR@#/opt/kaltura/web#g" -e "s#@TEMPLATE_PARTNER_ADMIN_SECRET@#$ADMIN_SECRET#g" -e "s#@ADMIN_CONSOLE_PARTNER_ADMIN_SECRET@#$ADMIN_SECRET#g" -e "s#@MONITOR_PARTNER_ADMIN_SECRET@#$MONITOR_PARTNER_ADMIN_SECRET#g" -e "s#@SERVICE_URL@#$SERVICE_URL#g" -e "s#@ADMIN_CONSOLE_ADMIN_MAIL@#$ADMIN_CONSOLE_ADMIN_MAIL#g" -e "s#@MONITOR_PARTNER_SECRET@#$MONITOR_PARTNER_SECRET#g" -e "s#@PARTNER_ZERO_ADMIN_SECRET@#$PARTNER_ZERO_ADMIN_SECRET#g" -e "s#@BATCH_PARTNER_ADMIN_SECRET@#$BATCH_PARTNER_ADMIN_SECRET#g" -e "s#@MEDIA_PARTNER_ADMIN_SECRET@#$MEDIA_PARTNER_ADMIN_SECRET#g" -e "s#@TEMPLATE_PARTNER_ADMIN_SECRET@#$TEMPLATE_PARTNER_ADMIN_SECRET#g" -e "s#@HOSTED_PAGES_PARTNER_ADMIN_SECRET@#$HOSTED_PAGES_PARTNER_ADMIN_SECRET#g" -e "s#@STORAGE_BASE_DIR@#$BASE_DIR/web#g" -e "s#@DELIVERY_HTTP_BASE_URL@#https://dontknow.com#g" -e "s#@DELIVERY_RTMP_BASE_URL@#rtmp://reallydontknow.com#g" -e "s#@DELIVERY_ISS_BASE_URL@#https://honesttogodihavenoidea.com#g" -i $DEST_FILE
done


for TMPL in `find /opt/kaltura/app/deployment/base/scripts/init_data/ -name "*template*"`;do
	DEST_FILE=`echo $TMPL | sed 's@\(.*\)\.template\(.*\)@\1\2@'`
	cp $TMPL $DEST_FILE
	sed -e "s#@WEB_DIR@#/opt/kaltura/web#g" -e "s#@TEMPLATE_PARTNER_ADMIN_SECRET@#$ADMIN_SECRET#g" -e "s#@ADMIN_CONSOLE_PARTNER_ADMIN_SECRET@#$ADMIN_SECRET#g" -e "s#@MONITOR_PARTNER_ADMIN_SECRET@#$MONITOR_PARTNER_ADMIN_SECRET#g" -e "s#@SERVICE_URL@#$SERVICE_URL#g" -e "s#@ADMIN_CONSOLE_ADMIN_MAIL@#$ADMIN_CONSOLE_ADMIN_MAIL#g" -e "s#@MONITOR_PARTNER_SECRET@#$MONITOR_PARTNER_SECRET#g" -e "s#@PARTNER_ZERO_ADMIN_SECRET@#$PARTNER_ZERO_ADMIN_SECRET#g" -e "s#@BATCH_PARTNER_ADMIN_SECRET@#$BATCH_PARTNER_ADMIN_SECRET#g" -e "s#@MEDIA_PARTNER_ADMIN_SECRET@#$MEDIA_PARTNER_ADMIN_SECRET#g" -e "s#@TEMPLATE_PARTNER_ADMIN_SECRET@#$TEMPLATE_PARTNER_ADMIN_SECRET#g" -e "s#@KALTURA_VERSION@#$DISPLAY_NAME#g" -e "s#@HOSTED_PAGES_PARTNER_ADMIN_SECRET@#$HOSTED_PAGES_PARTNER_ADMIN_SECRET#g" -e "s#@STORAGE_BASE_DIR@#$BASE_DIR/web#g" -e "s#@DELIVERY_HTTP_BASE_URL@#https://dontknow.com#g" -e "s#@DELIVERY_RTMP_BASE_URL@#rtmp://reallydontknow.com#g" -e "s#@DELIVERY_ISS_BASE_URL@#https://honesttogodihavenoidea.com#g" -i $DEST_FILE
done

echo "
Generating client libs... see log at $BASE_DIR/log/generate.php.log

"
php /opt/kaltura/app/generator/generate.php >> $BASE_DIR/log/generate.php.log 2>&1
touch "base-config.lock" "$BASE_DIR/app/base-config.lock"

echo "Configuration of $DISPLAY_NAME finished successfully!"
