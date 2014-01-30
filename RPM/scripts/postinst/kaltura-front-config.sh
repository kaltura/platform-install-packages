#!/bin/bash 
#===============================================================================
#          FILE: kaltura-front-config.sh
#         USAGE: ./kaltura-front-config.sh 
#   DESCRIPTION: configure server as a front node.
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 01/02/14 09:24:27 EST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error
enable_apps_conf()
{
	KALTURA_APACHE_CONFD=$1
	cd $KALTURA_APACHE_CONFD
	for CONF in  apps.conf var.conf ;do
		echo "Enabling Apache config - $CONF"
		ln -s $CONF enabled.$CONF
	done
}
enable_admin_conf()
{
	KALTURA_APACHE_CONFD=$1
	echo "Enabling Apache config - admin.conf"
	ln -s $KALTURA_APACHE_CONFD/admin.conf $KALTURA_APACHE_CONFD/enabled.admin.conf 
}
create_answer_file()
{
	ANSFILE="$1"
        for VAL in CONFIG_CHOICE IS_SSL CRT_FILE KEY_FILE; do
                if [ -n "${!VAL}" ];then
			sed "/^$VAL=.*/d" -i $ANSFILE
			echo "$VAL=\"${!VAL}\"" >> $ANSFILE 
                fi
        done
	echo "

========================================================================================================================
Kaltura install answer file written to $ANSFILE  -  Please save it!
This answers file can be used to silently-install re-install this machine or deploy other hosts in your cluster.
========================================================================================================================

"
}
if [ -n "$1" -a -r "$1" ];then
	ANSFILE=$1
	. $ANSFILE
	AUTO_YES=1
	NEWANSFILE="/tmp/kaltura_`date +%d_%m_%H_%M.ans`"
	cp $ANSFILE $NEWANSFILE
fi
if [ ! -r /opt/kaltura/app/base-config.lock ];then
	`dirname $0`/kaltura-base-config.sh "$ANSFILE"
else
	echo "base-config completed successfully, if you ever want to re-configure your system (e.g. change DB hostname) run the following script:
# rm /opt/kaltura/app/base-config.lock
# $BASE_DIR/bin/kaltura-base-config.sh
"
fi
RC_FILE=/etc/kaltura.d/system.ini
if [ ! -r "$RC_FILE" ];then
	echo "Could not find $RC_FILE so, exiting.."
	exit 1 
fi
. $RC_FILE
KALTURA_APACHE_CONF=$APP_DIR/configurations/apache
KALTURA_APACHE_CONFD=$KALTURA_APACHE_CONF/conf.d
if [ -z "$IS_SSL" ];then
#unset IS_SSL
cat << EOF 
Is your Apache working with SSL?[Y/n]
EOF
	read IS_SSL
	if [ -z "$IS_SSL" ];then
        	IS_SSL='Y'
        fi  
fi
if [ "$IS_SSL" != 'Y' -a "$IS_SSL" != 1 ];then
#-a ! -r "$ANSFILE" ];then
	echo "update permission set STATUS=3 WHERE permission.NAME='FEATURE_KMC_ENFORCE_HTTPS' ;" | mysql $DB1_NAME -h$DB1_HOST -u$DB1_USER -P$DB1_PORT -p$DB1_PASS 
	if [ -z "$AUTO_YES" ];then
		echo "It is recommended that you do work using HTTPs. Would you like to continue anyway?[N/y]"
		read CONT
		if [ "$CONT" != 'y' ];then
			echo "Exiting."
			exit 2
		fi
		IS_SSL='N'
	fi
	MAIN_APACHE_CONF=$KALTURA_APACHE_CONF/kaltura.conf
else
	# configure SSL:
	MAIN_APACHE_CONF=$KALTURA_APACHE_CONF/kaltura.ssl.conf
	if [ -z "$CRT_FILE" ] ;then
		echo "Please input path to your SSL certificate[/etc/ssl/certs/localhost.crt]:"
		read -e CRT_FILE
		if [ -z "$CRT_FILE" ];then
			CRT_FILE=/etc/ssl/certs/localhost.crt
		fi
		
	fi
	if [ -z "$KEY_FILE" ];then
		echo "Please input path to your SSL key[/etc/pki/tls/private/localhost.key]:"
		read -e KEY_FILE
		if [ -z "$KEY_FILE" ];then
			KEY_FILE=/etc/pki/tls/private/localhost.key
		fi

	fi
	# check key and crt match
	CRT_SUM=`openssl x509 -in $CRT_FILE -modulus -noout | openssl md5`
	KEY_SUM=`openssl rsa -in $KEY_FILE -modulus -noout | openssl md5`
	if [ "$CRT_SUM" != "$KEY_SUM" ];then
		echo "

	MD5 sums between .key and .crt files DO NOT MATCH
	# openssl rsa -in $KEY_PATH -modulus -noout | openssl md5
	$KEY_HASH
	# openssl x509 -in $CERT_PATH -modulus -noout | openssl md5
	$CRT_HASH

	"
		exit 3
	fi
	# it might fail if done before there's a DB but I don't want it to stop the config script, it can be easily fixed later.
	php $APP_DIR/deployment/base/scripts/insertPermissions.php -d $APP_DIR/deployment/permissions/ssl/ >/dev/null 2>&1 ||true

	# if cert is self signed:
	if openssl verify  $CRT_FILE | grep 'self signed certificate' -q ;then
		echo "

WARNING: self signed cerificate detected. Will set settings.clientConfig.verifySSL=0 in $APP_DIR/configurations/admin.ini.

	"
		echo "settings.clientConfig.verifySSL=0" >> $APP_DIR/configurations/admin.ini
		sed -i  's@\(\[production\]\)@\1\nsettings.clientConfig.verifySSL=0@' $APP_DIR/configurations/admin.ini
	fi
	if [ -f /etc/httpd/conf.d/ssl.conf ];then
		echo "Moving /etc/httpd/conf.d/ssl.conf to /etc/httpd/conf.d/ssl.conf.ks.bak."
		mv /etc/httpd/conf.d/ssl.conf /etc/httpd/conf.d/ssl.conf.ks.bak
	fi
	sed "s#@SSL_CERTIFICATE_FILE@#$CRT_FILE#g" $MAIN_APACHE_CONF.template > $MAIN_APACHE_CONF
	sed -i "s#@SSL_CERTIFICATE_KEY_FILE@#$KEY_FILE#g" $MAIN_APACHE_CONF
fi

if [ "$IS_SSL" = 'Y' ];then 
	DEFAULT_PORT=443
else
	DEFAULT_PORT=80
fi

if [ -z "$KALTURA_VIRTUAL_HOST_PORT" ];then
	echo "Which port will this Vhost listen on? [$DEFAULT_PORT] "
	read -e KALTURA_VIRTUAL_HOST_PORT
	if [ -z "$KALTURA_VIRTUAL_HOST_PORT" ];then
		KALTURA_VIRTUAL_HOST_PORT=$DEFAULT_PORT
		#echo $KALTURA_VIRTUAL_HOST_PORT
	fi
	if [ "$KALTURA_VIRTUAL_HOST_PORT" -eq 443 ];then
		PROTOCOL="https"
	else
		PROTOCOL="http"
	fi
fi

if [ -z "$SERVICE_URL" ];then
	echo "Service URL [$PROTOCOL://$KALTURA_VIRTUAL_HOST_NAME:$KALTURA_VIRTUAL_HOST_PORT]: "
	read -e SERVICE_URL
	if [ -z "$SERVICE_URL" ];then
		SERVICE_URL=$PROTOCOL://$KALTURA_FULL_VIRTUAL_HOST_NAME
	fi
fi

echo "use kaltura" | mysql -h$MYSQL_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT $KALTURA_DB 2> /dev/null
if [ $? -eq 0 ];then
	echo "update permission set STATUS=2 WHERE permission.PARTNER_ID IN ('0') AND permission.NAME='FEATURE_KMC_ENFORCE_HTTPS' ORDER BY permission.STATUS ASC LIMIT 1;" | mysql $DB1_NAME -h$DB1_HOST -u$DB1_USER -P$DB1_PORT -p$DB1_PASS 
fi


cp $KALTURA_APACHE_CONFD/enabled.kaltura.conf.template $KALTURA_APACHE_CONFD/enabled.kaltura.conf 
sed -e "s#@APP_DIR@#$APP_DIR#g" -e "s#@LOG_DIR@#$LOG_DIR#g" -e "s#@WEB_DIR@#$WEB_DIR#g" -e "s#@KALTURA_VIRTUAL_HOST_NAME@#$KALTURA_VIRTUAL_HOST_NAME#g" -e "s#@KALTURA_VIRTUAL_HOST_PORT@#$KALTURA_VIRTUAL_HOST_PORT#g" -e "s#@SERVICE_URL@#$SERVICE_URL#g" -i $MAIN_APACHE_CONF $KALTURA_APACHE_CONFD/enabled.kaltura.conf

CONF_FILES=`find $APP_DIR/configurations  -type f| grep -v template`
for i in settings.serviceUrl \$wgKalturaServiceUrl \$wgKalturaCDNUrl \$wgKalturaStatsServiceUrl apphome_url admin_console_url admin_console SERVICE_URL settings.serviceUrl; do sed -i "s#\($i\)\s*=.*#\1=$SERVICE_URL#g" $CONF_FILES;done

find /etc/httpd/conf.d -type l -name "kaltura*" -exec rm {} \;
ln -fs $MAIN_APACHE_CONF /etc/httpd/conf.d/  

if [ -z "$CONFIG_CHOICE" ];then
cat << EOF 
Please select one of the following options:
0. Kaltura Management Console [KMC], Hosted Apps, HTML5 lib and ClipApp
1. KAC - Kaltura Admin Console
2. All web interfaces 
EOF

	CONFIG_MSG="Setup enabled the following Apache configuration for you:"
	read CONFIG_CHOICE
fi

# remove current syms if any.
find $KALTURA_APACHE_CONFD -type l -exec rm {} \;

if [ "$CONFIG_CHOICE" = 0 ];then
	enable_apps_conf $KALTURA_APACHE_CONFD
elif [ "$CONFIG_CHOICE" = 1 ];then
	enable_admin_conf $KALTURA_APACHE_CONFD
elif [ "$CONFIG_CHOICE" = 2 ];then
	enable_apps_conf $KALTURA_APACHE_CONFD
	enable_admin_conf $KALTURA_APACHE_CONFD
else
        echo "Choose a value between 0-2"
        exit 1
fi

# cronjobs:
ln -sf $APP_DIR/configurations/cron/api /etc/cron.d/kaltura-api
ln -sf $APP_DIR/configurations/cron/cleanup /etc/cron.d/kaltura-cleanup

# logrotate:
ln -sf $APP_DIR/configurations/logrotate/kaltura_apache /etc/logrotate.d/ 
ln -sf $APP_DIR/configurations/logrotate/kaltura_apps /etc/logrotate.d/

if [ -r "$NEWANSFILE" ];then
	create_answer_file $NEWANSFILE
fi
chown -R apache.kaltura /opt/kaltura/log /opt/kaltura/app/cache
chmod -R 775 /opt/kaltura/log /opt/kaltura/app/cache/
service httpd restart
