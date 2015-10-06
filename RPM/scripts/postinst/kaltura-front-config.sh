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
trap 'my_trap_handler "${LINENO}" ${$?}' ERR
send_install_becon `basename $0` $ZONE install_start 0 
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
trap 'my_trap_handler "${LINENO}" ${$?}' ERR

	if [ -z "$AUTO_YES" ];then
		echo -e "${YELLOW}It is recommended that you do work using HTTPs. Would you like to continue anyway?[N/y]${NORMAL}"
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
		echo -e "${CYAN}Please input path to your SSL chain file or leave empty in case you have none${CYAN}:${NORMAL}"
		read -e CHAIN_FILE
	fi
	#if [ -z "$CA_FILE" ];then
	#	echo -e "${CYAN}Please input path to your SSL CA file or leave empty in case you have none${CYAN}:${NORMAL}"
	#	read -e CA_FILE
	#fi
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
	if openssl verify  $CRT_FILE | grep 'self signed certificate' -q ;then
		echo -e "${YELLOW}

WARNING: self signed cerificate detected. Will set settings.clientConfig.verifySSL=0 in $APP_DIR/configurations/admin.ini.
	${NORMAL}
	"
		echo -e "settings.clientConfig.verifySSL=0" >> $APP_DIR/configurations/admin.ini
		sed -i  's@\(\[production\]\)@\1\nsettings.clientConfig.verifySSL=0@' $APP_DIR/configurations/admin.ini
	fi
	#if [ -f /etc/httpd/conf.d/ssl.conf ];then
	#	echo "Moving /etc/httpd/conf.d/ssl.conf to /etc/httpd/conf.d/ssl.conf.ks.bak."
	#	mv /etc/httpd/conf.d/ssl.conf /etc/httpd/conf.d/ssl.conf.ks.bak
	#fi
	sed "s#@SSL_CERTIFICATE_FILE@#$CRT_FILE#g" -i $MAIN_APACHE_CONF
	sed -i "s#@SSL_CERTIFICATE_KEY_FILE@#$KEY_FILE#g" $MAIN_APACHE_CONF
	if [ -r "$CHAIN_FILE" ];then
		sed -i "s^SSLCertificateChainFile @SSL_CERTIFICATE_CHAIN_FILE@^SSLCertificateChainFile $CHAIN_FILE^" $MAIN_APACHE_CONF
	else
		CHAIN_FILE="NO_CHAIN"
		sed -i "s^SSLCertificateChainFile @SSL_CERTIFICATE_CHAIN_FILE@^#SSLCertificateChainFile @SSL_CERTIFICATE_CHAIN_FILE@^" $MAIN_APACHE_CONF
	fi
	if [ -r "$CA_FILE" ];then
		sed -i "s^SSLCACertificateFile @SSL_CERTIFICATE_CA_FILE@^SSLCACertificateFile $CA_FILE^" $MAIN_APACHE_CONF
	else
		CA_FILE="NO_CA"
		sed -i "s^SSLCACertificateFile @SSL_CERTIFICATE_CA_FILE@^#SSLCACertificateFile @SSL_CERTIFICATE_CA_FILE@^" $MAIN_APACHE_CONF
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
	trap 'my_trap_handler "${LINENO}" ${$?}' ERR
else
	DEFAULT_PORT=80
fi

if [ -z "$KALTURA_VIRTUAL_HOST_PORT" ];then
	echo -e "${CYAN}Which port will this Vhost listen on? [${YELLOW}$DEFAULT_PORT${CYAN}]${NORMAL} "
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
	echo -e "${CYAN}Service URL [${YELLOW}$PROTOCOL://$KALTURA_VIRTUAL_HOST_NAME:$KALTURA_VIRTUAL_HOST_PORT${CYAN}]:${NORMAL} "
	read -e SERVICE_URL
	if [ -z "$SERVICE_URL" ];then
		SERVICE_URL=$PROTOCOL://$KALTURA_FULL_VIRTUAL_HOST_NAME
	fi
fi


# Dropping the port when it's a standard one
if [ "$KALTURA_VIRTUAL_HOST_PORT" -eq 443 -o "$KALTURA_VIRTUAL_HOST_PORT" -eq 80 ];then
        KALTURA_FULL_VIRTUAL_HOST_NAME="$KALTURA_VIRTUAL_HOST_NAME"
        SERVICE_URL=$KALTURA_VIRTUAL_HOST_PORT://$KALTURA_FULL_VIRTUAL_HOST_NAME
else
        KALTURA_FULL_VIRTUAL_HOST_NAME="$KALTURA_VIRTUAL_HOST_NAME:$KALTURA_VIRTUAL_HOST_PORT"
fi


cp $KALTURA_APACHE_CONFD/enabled.kaltura.conf.template $KALTURA_APACHE_CONFD/enabled.kaltura.conf 
cp $KALTURA_APACHE_CONF/kaltura.conf.template $KALTURA_APACHE_CONF/kaltura.conf
sed -e "s#@APP_DIR@#$APP_DIR#g" -e "s#@LOG_DIR@#$LOG_DIR#g" -e "s#@WEB_DIR@#$WEB_DIR#g" -e "s#@KALTURA_VIRTUAL_HOST_NAME@#$KALTURA_VIRTUAL_HOST_NAME#g" -e "s#@KALTURA_VIRTUAL_HOST_PORT@#$KALTURA_VIRTUAL_HOST_PORT#g" -e "s#@SERVICE_URL@#$SERVICE_URL#g" -i $MAIN_APACHE_CONF $KALTURA_APACHE_CONFD/enabled.kaltura.conf

CONF_FILES=`find $APP_DIR/configurations  -type f| grep -v template`

for i in settings.serviceUrl \$wgKalturaServiceUrl \$wgKalturaCDNUrl \$wgKalturaStatsServiceUrl apphome_url admin_console_url admin_console SERVICE_URL settings.serviceUrl; do sed -i "s#\($i\)\s*=.*#\1=$SERVICE_URL#g" $CONF_FILES;done

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
service httpd restart
chkconfig httpd on
chkconfig memcached on
service memcached restart
ln -sf $BASE_DIR/app/configurations/monit/monit.avail/httpd.rc $BASE_DIR/app/configurations/monit/monit.d/enabled.httpd.rc
ln -sf $BASE_DIR/app/configurations/monit/monit.avail/memcached.rc $BASE_DIR/app/configurations/monit/monit.d/enabled.memcached.rc
/etc/init.d/kaltura-monit restart
	trap - ERR
	echo "use kaltura" | mysql -h$DB1_HOST -u$DB1_USER -p$DB1_PASS -P$DB1_PORT $DB1_NAME 2> /dev/null
	if [ $? -eq 0 ];then
		if [ -r $BASE_DIR/apps/studio/`rpm -qa kaltura-html5-studio --queryformat %{version}`/studio.ini ];then
			php $BASE_DIR/app/deployment/uiconf/deploy_v2.php --ini=$BASE_DIR/apps/studio/`rpm -qa kaltura-html5-studio --queryformat %{version}`/studio.ini >> /dev/null
			sed -i "s@^\(studio_version\s*=\)\(.*\)@\1 `rpm -qa kaltura-html5-studio --queryformat %{version}`@g" -i $BASE_DIR/app/configurations/local.ini
		fi
	# we can't use rpm -q kaltura-kmc because this node may not be the one where we installed the KMC RPM on, as it resides in the web dir and does not need to be installed on all front nodes.
		KMC_PATH=`ls -ld $BASE_DIR/web/flash/kmc/v* 2>/dev/null|awk -F " " '{print $NF}' |tail -1`
#sed -i "s#\(@KMC_VERSION@\)\s*=.*#\1=%{_kmc_version}#g" $RPM_BUILD_ROOT%{prefix}/bin/sanity_config.template.ini
#sed -i "s#\(@KMC_LOGIN_VERSION@\)\s*=.*#\1=%{kmc_login_version}#g" $RPM_BUILD_ROOT%{prefix}/bin/sanity_config.template.ini
		#ln -sf $KMC_PATH/uiconf/kaltura/kmc  $BASE_DIR/web/content/uiconf/kaltura
		php $BASE_DIR/app/deployment/uiconf/deploy_v2.php --ini=$KMC_PATH/config.ini >> /dev/null
		HTML5_PATH=`ls -ld $BASE_DIR/web/html5/html5lib/v* 2>/dev/null|awk -F " " '{print $NF}' |tail -1`
		sed -i "s@^\(html5_version\s*=\)\(.*\)@\1 `rpm -qa kaltura-html5lib --queryformat %{version}`@g" -i $BASE_DIR/app/configurations/local.ini
		# https://github.com/kaltura/mwEmbed/issues/574
		# find $BASE_DIR/web/html5/html5lib/ -type f -exec sed -i "s@http://cdnapi.kaltura.com@$SERVICE_URL@g" {} \;
	fi
	trap 'my_trap_handler "${LINENO}" ${$?}' ERR
send_install_becon `basename $0` $ZONE install_success 0 
