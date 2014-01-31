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
	RC=0
        for VAL in TIME_ZONE KALTURA_FULL_VIRTUAL_HOST_NAME KALTURA_VIRTUAL_HOST_NAME DB1_HOST DB1_PORT DB1_NAME DB1_USER SERVICE_URL SPHINX_SERVER1 SPHINX_SERVER2 DWH_HOST DWH_PORT SPHINX_DB_HOST SPHINX_DB_PORT ADMIN_CONSOLE_ADMIN_MAIL ADMIN_CONSOLE_PASSWORD SUPER_USER SUPER_USER_PASSWD CDN_HOST KALTURA_VIRTUAL_HOST_PORT DB1_PASS DWH_PASS; do
                if [ -z "${!VAL}" ];then
                        #echo "I need $VAL in $ANSFILE."
                        #exit 1
			VALS="$VALS\n$VAL"
			RC=1
                fi
        done
	if [ $RC -eq 1 ];then
		echo -en "Missing the following params in $ANSFILE
		$VALS
		"
		exit $RC 
	fi
}

create_answer_file()
{
	POST_INST_MAIL_TMPL=$1
	ANSFILE=/tmp/kaltura_`date +%d_%m_%H_%M`.ans
        for VAL in TIME_ZONE KALTURA_FULL_VIRTUAL_HOST_NAME KALTURA_VIRTUAL_HOST_NAME DB1_HOST DB1_PORT DB1_PASS DB1_NAME DB1_USER SERVICE_URL SPHINX_SERVER1 SPHINX_SERVER2 DWH_HOST DWH_PORT SPHINX_DB_HOST SPHINX_DB_PORT ADMIN_CONSOLE_ADMIN_MAIL ADMIN_CONSOLE_PASSWORD CDN_HOST KALTURA_VIRTUAL_HOST_PORT SUPER_USER SUPER_USER_PASSWD ENVIRONMENT_NAME DWH_PASS; do
                if [ -n "${!VAL}" ];then
			#ANSFILE=/tmp/kaltura_`date +%d_%m_%H_%M`.ans
			echo "$VAL=\"${!VAL}\"" >> $ANSFILE 
                fi
        done
			sed -i "s#@ANSFILE@#$ANSFILE#g" $POST_INST_MAIL_TMPL 
	echo "

========================================================================================================================
Kaltura install answer file written to $ANSFILE  -  Please save it!
This answers file can be used to silently-install re-install this machine or deploy other hosts in your cluster.
========================================================================================================================

"

}


KALTURA_FUNCTIONS_RC=`dirname $0`/kaltura-functions.rc
if [ ! -r "$KALTURA_FUNCTIONS_RC" ];then
	echo "Could not find $KALTURA_FUNCTIONS_RC so, exiting.."
	exit 3
fi
. $KALTURA_FUNCTIONS_RC
LOCALHOST=127.0.0.1
DISPLAY_NAME="Kaltura Server `rpm -qa kaltura-base --queryformat %{version}`"
KALT_CONF_DIR='/opt/kaltura/app/configurations/'
if [ -n "$1" -a -r "$1" ];then
        ANSFILE=$1
        verify_user_input $ANSFILE
	. $ANSFILE
	export ANSFILE
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

        if [ -z "$DB1_HOST" ];then
                echo "DB hostname [$LOCALHOST]: "
                read -e DB1_HOST
        	if [ -z "$DB1_HOST" ];then
			DB1_HOST=$LOCALHOST	
		fi
        fi

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
                read -s SUPER_USER_PASSWD
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

        if [ -z "$SPHINX_SERVER1" ];then
                echo "Sphinx host [$LOCALHOST]: "
                read -e SPHINX_SERVER1
		if [ -z $SPHINX_SERVER1 ];then
			SPHINX_SERVER1="$LOCALHOST"
		fi
        fi
	
	echo "Secondary Sphinx host: [leave empty if none] "
	read -e SPHINX_SERVER2
	if [ -z $SPHINX_SERVER2 ];then
		SPHINX_SERVER2=" "
	fi

        while [ -z "$SERVICE_URL" ];do
		if [ "$KALTURA_VIRTUAL_HOST_PORT" -eq 443 ];then
			PROTOCOL="https"
		else
			PROTOCOL="http"
		fi
                echo "Service URL [$PROTOCOL://$KALTURA_FULL_VIRTUAL_HOST_NAME]: "
                read -e SERVICE_URL
		if [ -z "$SERVICE_URL" ];then
			SERVICE_URL=$PROTOCOL://$KALTURA_FULL_VIRTUAL_HOST_NAME
		fi
        done
        while [ -z "$ADMIN_CONSOLE_ADMIN_MAIL" ];do
                echo "Kaltura Admin user (email address): "
                read -e ADMIN_CONSOLE_ADMIN_MAIL
        done
        while [ -z "$ADMIN_CONSOLE_PASSWORD" ];do
                echo "Admin user login password (must be minimum 8 chars and include at least one of each: upper-case, lower-case, number and a special character):"
                read -s ADMIN_CONSOLE_PASSWORD
		if echo $ADMIN_CONSOLE_PASSWORD | grep -q "/" ;then
			echo "Passwd can't have the '/' char in it. Please re-input"
			unset ADMIN_CONSOLE_PASSWORD
		fi
        done
        while [ -z "$TIME_ZONE" ];do
                echo "Your time zone [see http://php.net/date.timezone]: "
                read -e TIME_ZONE
        done
	
	if [ -z "$ENVIRONMENT_NAME" ];then
		echo "How would you like to name your system (this name will show as the From field in emails sent by the system) [Kaltura Video Platform]?"
		read ENVIRONMENT_NAME
		if [ -z "$ENVIRONMENT_NAME" ];then
			ENVIRONMENT_NAME="Kaltura Video Platform"
		fi
	fi

	if [ -z "$CONTACT_URL" ];then
		echo "Your website Contact Us URL [http://corp.kaltura.com/company/contact-us]:"
		read CONTACT_URL
		if [ -z "$CONTACT_URL" ];then
			CONTACT_URL="http://corp.kaltura.com/company/contact-us"
		fi
	fi
	if [ -z "$CONTACT_PHONE_NUMBER" ];then
		echo "Contact us phone number [+1 800 871 5224]?"
		read CONTACT_PHONE_NUMBER
		if [ -z "$CONTACT_PHONE_NUMBER" ];then
			CONTACT_PHONE_NUMBER="+1 800 871 5224"
		fi
	fi


BEGINNERS_TUTORIAL_URL=http://bit.ly/KalturaUploadMenu
QUICK_START_GUIDE_URL=http://bit.ly/KalturaKmcManual
FORUMS_URLS=http://bit.ly/KalturaForums





sed -i "s#\(date.timezone\)\s*=.*#\1='$TIME_ZONE'#g" /etc/php.ini /etc/php.d/*kaltura*ini
fi

if [ -z "$DB1_PASS" ];then
	DB1_PASS=`< /dev/urandom tr -dc A-Za-z0-9_ | head -c15`
	echo "update mysql.user set password=PASSWORD('$DB1_PASS') WHERE user='kaltura';flush PRIVILEGES" | mysql -h$DB1_HOST -P$DB1_PORT -u$SUPER_USER -p$SUPER_USER_PASSWD mysql
fi
DB1_NAME=kaltura
DB1_USER=kaltura

# no added value in putting this on a separate server..
SPHINX_DB_HOST=$DB1_HOST
SPHINX_DB_PORT=$DB1_PORT

BASE_DIR=/opt/kaltura
CONF_FILES=`find $KALT_CONF_DIR  -type f -name "*template*"`
CONF_FILES="$CONF_FILES $BASE_DIR/app/batch/batches/Mailer/emails_en.template.ini `find $BASE_DIR/dwh  -type f -name "*template*"`"
# Now we will sed.

for TMPL_CONF_FILE in $CONF_FILES;do
	CONF_FILE=`echo $TMPL_CONF_FILE | sed 's@\(.*\)\.template\(.*\)@\1\2@'`
#	echo $CONF_FILE
	cp $TMPL_CONF_FILE $CONF_FILE
	sed -e "s#@CDN_HOST@#$CDN_HOST#g" -e "s#@DB[1-9]_HOST@#$DB1_HOST#g" -e "s#@DB[1-9]_NAME@#$DB1_NAME#g" -e "s#@DB[1-9]_USER@#$DB1_USER#g" -e "s#@DB[1-9]_PASS@#$DB1_PASS#g" -e "s#@DB[1-9]_PORT@#$DB1_PORT#g" -e "s#@TIME_ZONE@#$TIME_ZONE#g" -e "s#@KALTURA_FULL_VIRTUAL_HOST_NAME@#$KALTURA_FULL_VIRTUAL_HOST_NAME#g" -e "s#@KALTURA_VIRTUAL_HOST_NAME@#$KALTURA_VIRTUAL_HOST_NAME#g" -e "s#@SERVICE_URL@#$SERVICE_URL#g" -e "s#@WWW_HOST@#$KALTURA_VIRTUAL_HOST_NAME#g" -e "s#@SPHINX_DB_NAME@#kaltura_sphinx_log#g" -e "s#@SPHINX_DB_HOST@#$SPHINX_DB_HOST#g" -e "s#@SPHINX_DB_PORT@#$DB1_PORT#g" -e "s#@DWH_HOST@#$DWH_HOST#g" -e "s#@DWH_PORT@#$DWH_PORT#g" -e "s#@SPHINX_SERVER1@#$SPHINX_SERVER1#g" -e "s#@SPHINX_SERVER2@#$SPHINX_SERVER2#g" -e "s#@DWH_DATABASE_NAME@#kalturadw#g" -e "s#@DWH_USER@#etl#g" -e "s#@DWH_PASS@#$DB1_PASS#g" -e "s#@ADMIN_CONSOLE_ADMIN_MAIL@#$ADMIN_CONSOLE_ADMIN_MAIL#g" -e "s#@WEB_DIR@#$BASE_DIR/web#g" -e "s#@LOG_DIR@#$BASE_DIR/log#g" -e "s#/opt/kaltura/app#$BASE_DIR/app#g" -e "s#@PHP_BIN@#/usr/bin/php#g" -e "s#@OS_KALTURA_USER@#kaltura#g" -e "s#@BASE_DIR@#$BASE_DIR#" -e "s#@APP_DIR@#$BASE_DIR/app#" -e "s#@DWH_DIR@#$BASE_DIR/dwh#g" -e "s#@EVENTS_LOGS_DIR@#$BASE_DIR/web/logs#g" -e "s#@TMP_DIR@#$BASE_DIR/tmp#g" -e "s#@APACHE_SERVICE@#httpd#g" -e "s#@KALTURA_VIRTUAL_HOST_PORT@#$KALTURA_VIRTUAL_HOST_PORT#g" -e "s#@BIN_DIR@#$BASE_DIR/bin#g" -e "s#@KALTURA_VERSION@#$DISPLAY_NAME#g" -e "s#@SPHINX_SERVER@#$SPHINX_SERVER#g" -e "s#@IMAGE_MAGICK_BIN_DIR@#/usr/bin#g" -e "s#@CURL_BIN_DIR@#/usr/bin#g" -e "s@^\(bin_path_mediainfo\).*@\1=/usr/bin/mediainfo@g" -e "s#@CONTACT_URL@#$CONTACT_URL#g" -e "s#@ENVIRONMENT_NAME@#$ENVIRONMENT_NAME#g" -e "s#@BEGINNERS_TUTORIAL_URL@#$BEGINNERS_TUTORIAL_URL#g" -e "s#@BEGINNERS_TUTORIAL_URL@#$BEGINNERS_TUTORIAL_URL#g" -e "s#@QUICK_START_GUIDE_URL@#$QUICK_START_GUIDE_URL#g" -e "s#@FORUMS_URLS@#$FORUMS_URLS#g" -e "s#@CONTACT_PHONE_NUMBER@#$CONTACT_PHONE_NUMBER#g" -e "s#@UNSUBSCRIBE_EMAIL_URL@#$SERVICE_URL/index.php/extwidget/blockMail?e=#g" -e "s#@UICONF_TAB_ACCESS@#SYSTEM_ADMIN_BATCH_CONTROL#g"  -e "s#@EVENTS_FETCH_METHOD@#local#g" -i $CONF_FILE
done

create_answer_file $POST_INST_MAIL_TMPL

echo "
SERVICE_URL=$SERVICE_URL
SPHINX_HOST=$SPHINX_SERVER1
DB1_PORT=$DB1_PORT
SUPER_USER=$SUPER_USER
SUPER_USER_PASSWD=$SUPER_USER_PASSWD
KALTURA_VIRTUAL_HOST_NAME=$KALTURA_VIRTUAL_HOST_NAME
KALTURA_FULL_VIRTUAL_HOST_NAME=$KALTURA_FULL_VIRTUAL_HOST_NAME">> $BASE_DIR/app/configurations/system.ini
# these two have passwds in them.
chown kaltura.apache $BASE_DIR/app/configurations/system.ini $BASE_DIR/app/configurations/db.ini
chmod 640 $BASE_DIR/app/configurations/system.ini $BASE_DIR/app/configurations/db.ini


# gen secrets
ADMIN_SECRET=`$ADMIN_CONSOLE_ADMIN_PASSWD`
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
	sed -e "s#@WEB_DIR@#/opt/kaltura/web#g" -e "s#@TEMPLATE_PARTNER_ADMIN_SECRET@#$ADMIN_SECRET#g" -e "s#@ADMIN_CONSOLE_PARTNER_ADMIN_SECRET@#$ADMIN_SECRET#g" -e "s#@MONITOR_PARTNER_ADMIN_SECRET@#$MONITOR_PARTNER_ADMIN_SECRET#g" -e "s#@SERVICE_URL@#$SERVICE_URL#g" -e "s#@ADMIN_CONSOLE_ADMIN_MAIL@#$ADMIN_CONSOLE_ADMIN_MAIL#g" -e "s#@MONITOR_PARTNER_SECRET@#$MONITOR_PARTNER_SECRET#g" -e "s#@PARTNER_ZERO_ADMIN_SECRET@#$PARTNER_ZERO_ADMIN_SECRET#g" -e "s#@BATCH_PARTNER_ADMIN_SECRET@#$BATCH_PARTNER_ADMIN_SECRET#g" -e "s#@MEDIA_PARTNER_ADMIN_SECRET@#$MEDIA_PARTNER_ADMIN_SECRET#g" -e "s#@TEMPLATE_PARTNER_ADMIN_SECRET@#$TEMPLATE_PARTNER_ADMIN_SECRET#g" -e "s#@HOSTED_PAGES_PARTNER_ADMIN_SECRET@#$HOSTED_PAGES_PARTNER_ADMIN_SECRET#g" -e "s#@STORAGE_BASE_DIR@#$BASE_DIR/web#g" -e "s#@DELIVERY_HTTP_BASE_URL@#https://dontknow.com#g" -e "s#@DELIVERY_RTMP_BASE_URL@#rtmp://reallydontknow.com#g" -e "s#@DELIVERY_ISS_BASE_URL@#https://honesttogodihavenoidea.com#g" -e "s/@ADMIN_CONSOLE_PASSWORD@/$ADMIN_CONSOLE_PASSWORD/g" -i $DEST_FILE
done


for TMPL in `find /opt/kaltura/app/deployment/base/scripts/init_data/ -name "*template*"`;do
	DEST_FILE=`echo $TMPL | sed 's@\(.*\)\.template\(.*\)@\1\2@'`
	cp $TMPL $DEST_FILE
	sed -e "s#@WEB_DIR@#/opt/kaltura/web#g" -e "s#@TEMPLATE_PARTNER_ADMIN_SECRET@#$ADMIN_SECRET#g" -e "s#@ADMIN_CONSOLE_PARTNER_ADMIN_SECRET@#$ADMIN_SECRET#g" -e "s#@MONITOR_PARTNER_ADMIN_SECRET@#$MONITOR_PARTNER_ADMIN_SECRET#g" -e "s#@SERVICE_URL@#$SERVICE_URL#g" -e "s#@ADMIN_CONSOLE_ADMIN_MAIL@#$ADMIN_CONSOLE_ADMIN_MAIL#g" -e "s#@MONITOR_PARTNER_SECRET@#$MONITOR_PARTNER_SECRET#g" -e "s#@PARTNER_ZERO_ADMIN_SECRET@#$PARTNER_ZERO_ADMIN_SECRET#g" -e "s#@BATCH_PARTNER_ADMIN_SECRET@#$BATCH_PARTNER_ADMIN_SECRET#g" -e "s#@MEDIA_PARTNER_ADMIN_SECRET@#$MEDIA_PARTNER_ADMIN_SECRET#g" -e "s#@TEMPLATE_PARTNER_ADMIN_SECRET@#$TEMPLATE_PARTNER_ADMIN_SECRET#g" -e "s#@KALTURA_VERSION@#$DISPLAY_NAME#g" -e "s#@HOSTED_PAGES_PARTNER_ADMIN_SECRET@#$HOSTED_PAGES_PARTNER_ADMIN_SECRET#g" -e "s#@STORAGE_BASE_DIR@#$BASE_DIR/web#g" -e "s#@DELIVERY_HTTP_BASE_URL@#https://dontknow.com#g" -e "s#@DELIVERY_RTMP_BASE_URL@#rtmp://reallydontknow.com#g" -e "s#@DELIVERY_ISS_BASE_URL@#https://honesttogodihavenoidea.com#g"  -e "s/@ADMIN_CONSOLE_PASSWORD@/$ADMIN_CONSOLE_PASSWORD/g" -i $DEST_FILE
done

if [ ! -r "$BASE_DIR/app/base-config-generator.lock" ];then
	echo "
	Generating client libs... see log at $BASE_DIR/log/generate.php.log

	"
	php /opt/kaltura/app/generator/generate.php >> $BASE_DIR/log/generate.php.log 2>&1 && touch "$BASE_DIR/app/base-config-generator.lock"
fi

set +e


ln -sf $BASE_DIR/app/configurations/logrotate/kaltura_base /etc/logrotate.d/
touch  "$BASE_DIR/app/base-config.lock"
rm -rf $BASE_DIR/cache/*
rm -f $BASE_DIR/log/kaltura*.log

echo "Configuration of $DISPLAY_NAME finished successfully!"
