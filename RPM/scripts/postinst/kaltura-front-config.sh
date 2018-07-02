#!/bin/bash  
#===============================================================================
#          FILE: kaltura-front-config.sh
#         USAGE: ./kaltura-front-config.sh 
#   DESCRIPTION: configure server as a front node.
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
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
		echo -e "${CYAN}Enabling Apache config - $CONF${NORMAL}"
		ln -s $CONF enabled.$CONF
	done
}
enable_admin_conf()
{
	KALTURA_APACHE_CONFD=$1
	echo -e "${CYAN}Enabling Apache config - admin.conf${NORMAL}"
	ln -s $KALTURA_APACHE_CONFD/admin.conf $KALTURA_APACHE_CONFD/enabled.admin.conf 
}
create_answer_file()
{
	ANSFILE="$1"
        for VAL in CONFIG_CHOICE IS_SSL CRT_FILE KEY_FILE CHAIN_FILE CA_FILE; do
                if [ -n "${!VAL}" ];then
			sed "/^$VAL=.*/d" -i $ANSFILE
			echo "$VAL=\"${!VAL}\"" >> $ANSFILE 
                fi
        done
	echo -e "${CYAN}

========================================================================================================================
Kaltura install answer file written to $ANSFILE  -  Please save it!
This answers file can be used to silently-install re-install this machine or deploy other hosts in your cluster.
========================================================================================================================
${NORMAL}
"
}
KALTURA_FUNCTIONS_RC=`dirname $0`/kaltura-functions.rc
if [ ! -r "$KALTURA_FUNCTIONS_RC" ];then
	OUT="Could not find $KALTURA_FUNCTIONS_RC so, exiting.."
	echo $OUT
	exit 3
fi
PHP_MINOR_VER=`php -r 'echo PHP_MINOR_VERSION;'`
if [ "$PHP_MINOR_VER" -gt 3 ];then
        if ! rpm -q php-pecl-zendopcache >/dev/null;then
                yum -y install php-pecl-zendopcache
        fi
fi

. $KALTURA_FUNCTIONS_RC
NEWANSFILE="/tmp/kaltura_`date +%d_%m_%H_%M.ans`"
if [ -n "$1" -a -r "$1" ];then
	ANSFILE=$1
	. $ANSFILE
	AUTO_YES=1
	cp $ANSFILE $NEWANSFILE
else
	touch $NEWANSFILE
fi
if [ ! -r /opt/kaltura/app/base-config.lock ];then
	`dirname $0`/kaltura-base-config.sh "$ANSFILE"
	if [ $? -ne 0 ];then
		echo -e "${BRIGHT_RED}ERROR: Base config failed. Please correct and re-run $0.${NORMAL}"
		exit 21
	fi
else
	echo -e "${BRIGHT_BLUE}base-config completed successfully, if you ever want to re-configure your system (e.g. change DB hostname) run the following script:
# rm /opt/kaltura/app/base-config.lock
# $BASE_DIR/bin/kaltura-base-config.sh
${NORMAL}
"
fi
RC_FILE=/etc/kaltura.d/system.ini
if [ ! -r "$RC_FILE" ];then
	echo -e "${BRIGHT_RED}ERROR: could not find $RC_FILE so, exiting..${NORMAL}"
	exit 1 
fi
. $RC_FILE
if ! rpm -q kaltura-front;then
	echo -e "${BRIGHT_BLUE}Skipping as kaltura-front is not installed.${NORMAL}"
	exit 0 
fi
trap 'my_trap_handler "${LINENO}" $?' ERR
send_install_becon "`basename $0`" "install_start" 0 
KALTURA_APACHE_CONF=$APP_DIR/configurations/apache
KALTURA_APACHE_CONFD=$KALTURA_APACHE_CONF/conf.d
#unset IS_SSL
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
if [ "$IS_SSL" != 'Y' -a "$IS_SSL" != 1 -a "$IS_SSL" != 'y' -a "$IS_SSL" != 'true' ];then
trap - ERR
echo "use kaltura" | mysql -h$DB1_HOST -u$DB1_USER -p$DB1_PASS -P$DB1_PORT $DB1_NAME 2> /dev/null
if [ $? -eq 0 ];then
	echo "update permission set STATUS=3 WHERE permission.NAME='FEATURE_KMC_ENFORCE_HTTPS' ;" | mysql $DB1_NAME -h$DB1_HOST -u$DB1_USER -P$DB1_PORT -p$DB1_PASS 2> /dev/null 
fi
trap 'my_trap_handler "${LINENO}" $?' ERR

	IS_SSL='N'
	MAIN_APACHE_CONF=$KALTURA_APACHE_CONF/kaltura.conf
else
	# configure SSL:
	MAIN_APACHE_CONF=$KALTURA_APACHE_CONF/kaltura.ssl.conf
	if [ ! -r "$CRT_FILE" ] ;then
		echo -e "${CYAN}Please input path to your SSL certificate[${YELLOW}/etc/ssl/certs/localhost.crt${CYAN}]:${NORMAL}"
		read -e CRT_FILE
		if [ -z "$CRT_FILE" ];then
			CRT_FILE=/etc/ssl/certs/localhost.crt
		fi
		
	fi
	if [ ! -r "$KEY_FILE" ];then
		echo -e "${CYAN}Please input path to your SSL key[${YELLOW}/etc/pki/tls/private/localhost.key${CYAN}]:${NORMAL}"
		read -e KEY_FILE
		if [ -z "$KEY_FILE" ];then
			KEY_FILE=/etc/pki/tls/private/localhost.key
		fi

	fi
	if [ -z "$CHAIN_FILE" ];then
		echo -e "${CYAN}Please input path to your SSL CA file or leave empty in case you have none${CYAN}:${NORMAL}"
		read -e CHAIN_FILE
	fi
	# check key and crt match
	CRT_SUM=`openssl x509 -in $CRT_FILE -modulus -noout | openssl md5`
	KEY_SUM=`openssl rsa -in $KEY_FILE -modulus -noout | openssl md5`
	if [ "$CRT_SUM" != "$KEY_SUM" ];then
		echo -e ${BRIGHT_RED}"

	ERROR: MD5 sums between .key and .crt files DO NOT MATCH
	# openssl rsa -in $KEY_PATH -modulus -noout | openssl md5
	$KEY_HASH
	# openssl x509 -in $CERT_PATH -modulus -noout | openssl md5
	$CRT_HASH
	${NORMAL}
	"
		exit 3
	fi
	# it might fail if done before there's a DB but I don't want it to stop the config script, it can be easily fixed later.
	php $APP_DIR/deployment/base/scripts/insertPermissions.php -d $APP_DIR/deployment/permissions/ssl/ >/dev/null 2>&1 ||true

	# if cert is self signed:
	if [ -r "$CHAIN_FILE" ];then
		VERIFY_COMMAND="openssl verify -CAfile $CHAIN_FILE $CRT_FILE"
	elif [ -r "$CA_FILE" ];then
		VERIFY_COMMAND="openssl verify -CAfile $CA_FILE $CRT_FILE"
	else
		VERIFY_COMMAND="openssl verify $CRT_FILE"
	fi  
	if $VERIFY_COMMAND | grep 'self signed certificate' -q ;then
		echo -e "${YELLOW}

WARNING: self signed cerificate detected. Will set settings.clientConfig.verifySSL=0 in $APP_DIR/configurations/admin.ini.
	${NORMAL}
	"
		echo -e "settings.clientConfig.verifySSL=0" >> $APP_DIR/configurations/admin.ini
		sed -i  's@\(\[production\]\)@\1\nsettings.clientConfig.verifySSL=0@' $APP_DIR/configurations/admin.ini
	fi
	sed "s#@SSL_CERTIFICATE_FILE@#$CRT_FILE#g" -i $MAIN_APACHE_CONF
	sed -i "s#@SSL_CERTIFICATE_KEY_FILE@#$KEY_FILE#g" $MAIN_APACHE_CONF
	if [ -r "$CHAIN_FILE" ];then
		sed -i "s^SSLCACertificateFile @SSL_CERTIFICATE_CHAIN_FILE@^SSLCACertificateFile $CHAIN_FILE^" $MAIN_APACHE_CONF
	else
		CA_FILE="NO_CA"
		sed -i "s^SSLCACertificateFile @SSL_CERTIFICATE_CHAIN_FILE@^#SSLCACertificateFile @SSL_CERTIFICATE_CHAIN_FILE@^" $MAIN_APACHE_CONF
	fi
	echo "IS_SSL=y" >> $RC_FILE 
	echo "CRT_FILE=$CRT_FILE" >> $RC_FILE
        echo "KEY_FILE=$KEY_FILE" >> $RC_FILE
        echo "CA_FILE=$CA_FILE" >> $RC_FILE
        echo "CHAIN_FILE=$CHAIN_FILE" >> $RC_FILE

fi

if [ "$IS_SSL" = 'Y' -o "$IS_SSL" = 1 -o "$IS_SSL" = 'y' -o "$IS_SSL" = 'true' ];then
	DEFAULT_PORT=443
	trap - ERR
	echo "use kaltura" | mysql -h$DB1_HOST -u$DB1_USER -p$DB1_PASS -P$DB1_PORT $DB1_NAME 2> /dev/null
	if [ $? -eq 0 ];then
		echo "update permission set STATUS=1 WHERE permission.PARTNER_ID IN ('0') AND permission.NAME='FEATURE_KMC_ENFORCE_HTTPS' ORDER BY permission.STATUS ASC LIMIT 1;" | mysql $DB1_NAME -h$DB1_HOST -u$DB1_USER -P$DB1_PORT -p$DB1_PASS 
	fi
	trap 'my_trap_handler "${LINENO}" $?' ERR
else
	DEFAULT_PORT=80
fi

if [ -z "$KALTURA_VIRTUAL_HOST_PORT" ];then
	echo -e "${CYAN}Which port will this Vhost listen on? [${YELLOW}$DEFAULT_PORT${CYAN}]${NORMAL} "
	read -e KALTURA_VIRTUAL_HOST_PORT
	if [ -z "$KALTURA_VIRTUAL_HOST_PORT" ];then
		KALTURA_VIRTUAL_HOST_PORT=$DEFAULT_PORT
	fi
	if [ "$KALTURA_VIRTUAL_HOST_PORT" -eq 443 ];then
		PROTOCOL="https"
	else
		PROTOCOL="http"
	fi
fi

if [ -z "$SERVICE_URL" ];then
	echo -e "${CYAN}Service URL [${YELLOW}$PROTOCOL://$KALTURA_FULL_VIRTUAL_HOST_NAME${CYAN}]:${NORMAL} "
	read -e SERVICE_URL
	if [ -z "$SERVICE_URL" ];then
		SERVICE_URL=$PROTOCOL://$KALTURA_FULL_VIRTUAL_HOST_NAME
	fi
fi



cp $KALTURA_APACHE_CONFD/enabled.kaltura.conf.template $KALTURA_APACHE_CONFD/enabled.kaltura.conf 
cp $KALTURA_APACHE_CONF/kaltura.conf.template $KALTURA_APACHE_CONF/kaltura.conf
sed -e "s#@APP_DIR@#$APP_DIR#g" -e "s#@LOG_DIR@#$LOG_DIR#g" -e "s#@WEB_DIR@#$WEB_DIR#g" -e "s#@KALTURA_VIRTUAL_HOST_NAME@#$KALTURA_VIRTUAL_HOST_NAME#g" -e "s#@KALTURA_VIRTUAL_HOST_PORT@#$KALTURA_VIRTUAL_HOST_PORT#g" -e "s#@SERVICE_URL@#$SERVICE_URL#g" -i $MAIN_APACHE_CONF $KALTURA_APACHE_CONFD/enabled.kaltura.conf

CONF_FILES=`find $APP_DIR/configurations  -type f| grep -v template`

find /etc/httpd/conf.d -type l -name "zzzkaltura*" -exec rm {} \;
ln -fs $MAIN_APACHE_CONF /etc/httpd/conf.d/zzz`basename $MAIN_APACHE_CONF`

if [ -z "$CONFIG_CHOICE" ];then
cat << EOF 
Please select one of the following options [0]:
0. All web interfaces 
1. Kaltura Management Console [KMC], Hosted Apps, HTML5 lib and ClipApp
2. KAC - Kaltura Admin Console
EOF

	CONFIG_MSG="Setup enabled the following Apache configuration for you:"
	read CONFIG_CHOICE
fi

find $KALTURA_APACHE_CONFD -type l -exec rm {} \;

if [ "$CONFIG_CHOICE" = 1 ];then
	enable_apps_conf $KALTURA_APACHE_CONFD
elif [ "$CONFIG_CHOICE" = 2 ];then
	enable_admin_conf $KALTURA_APACHE_CONFD
elif [ "$CONFIG_CHOICE" = 0 ];then
	enable_apps_conf $KALTURA_APACHE_CONFD
	enable_admin_conf $KALTURA_APACHE_CONFD
else
	enable_apps_conf $KALTURA_APACHE_CONFD
	enable_admin_conf $KALTURA_APACHE_CONFD
fi

# cronjobs:
ln -sf $APP_DIR/configurations/cron/api /etc/cron.d/kaltura-api
# currently causing issues, commenting
#ln -sf $APP_DIR/configurations/cron/cleanup /etc/cron.d/kaltura-cleanup

# logrotate:
ln -sf $APP_DIR/configurations/logrotate/kaltura_apache /etc/logrotate.d/ 
ln -sf $APP_DIR/configurations/logrotate/kaltura_apps /etc/logrotate.d/

if [ -r "$NEWANSFILE" ];then
	create_answer_file $NEWANSFILE
fi
find $BASE_DIR/app/cache/ $BASE_DIR/log -type d -exec chmod 775 {} \; 
find $BASE_DIR/app/cache/ $BASE_DIR/log -type f -exec chmod 664 {} \; 
chown -R kaltura.apache $BASE_DIR/app/cache/ $BASE_DIR/log
find $BASE_DIR/web/html5/html5lib -type d -name cache -exec chown apache {} \;
service httpd restart
chkconfig httpd on
chkconfig memcached on
service memcached restart
ln -sf $BASE_DIR/app/configurations/monit/monit.avail/httpd.rc $BASE_DIR/app/configurations/monit/monit.d/enabled.httpd.rc
ln -sf $BASE_DIR/app/configurations/monit/monit.avail/memcached.rc $BASE_DIR/app/configurations/monit/monit.d/enabled.memcached.rc
service kaltura-monit restart
trap - ERR

HTML5_STUDIO_VERSION=`rpm -q kaltura-html5-studio --queryformat %{version}`
HTML5LIB_VERSION=`yum info  kaltura-html5lib| grep Version|awk -F ":" '{print $NF}'|sed 's/\s*//g'|tail -1`
sed -i "s@^\(html5_version\s*=\)\(.*\)@\1 $HTML5LIB_VERSION@g" -i $BASE_DIR/app/configurations/local.ini
sed -i "s/@HTML5_VER@/$HTML5LIB_VERSION/g" -i $BASE_DIR/apps/studio/$HTML5_STUDIO_VERSION/studio.ini
	echo "use kaltura" | mysql -h$DB1_HOST -u$DB1_USER -p$DB1_PASS -P$DB1_PORT $DB1_NAME 2> /dev/null
	if [ $? -eq 0 ];then
		if [ -r $BASE_DIR/apps/studio/$HTML5_STUDIO_VERSION/studio.ini ];then
			php $BASE_DIR/app/deployment/uiconf/deploy_v2.php --ini=$BASE_DIR/apps/studio/$HTML5_STUDIO_VERSION/studio.ini >> /dev/null
			sed -i "s@^\(studio_version\s*=\)\(.*\)@\1 $HTML5_STUDIO_VERSION@g" -i $BASE_DIR/app/configurations/local.ini
		fi
	# we can't use rpm -q kaltura-kmc because this node may not be the one where we installed the KMC RPM on, as it resides in the web dir and does not need to be installed on all front nodes.
		KMC_PATH=`ls -ld $BASE_DIR/web/flash/kmc/v* 2>/dev/null|awk -F " " '{print $NF}' |tail -1`
		php $BASE_DIR/app/deployment/uiconf/deploy_v2.php --ini=$KMC_PATH/config.ini >> /dev/null
		KMCNG_PATH=`ls -ld $BASE_DIR/apps/kmcng/v* 2>/dev/null|awk -F " " '{print $NF}' |tail -1`
		php $BASE_DIR/app/deployment/uiconf/deploy_v2.php --ini=$KMCNG_PATH/deploy/config.ini >> /dev/null
	fi
	trap 'my_trap_handler "${LINENO}" $?' ERR
send_install_becon `basename $0` install_success 0 
