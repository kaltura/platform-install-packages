#!/bin/bash -
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
if [ -n "$1" -a -r "$1" ];then
	ANSFILE=$1
	. $ANSFILE
fi
if [ ! -r /opt/kaltura/app/base-config.lock ];then
	`dirname $0`/kaltura-base-config.sh "$ANSFILE"
else
	echo "base-config skipped as /opt/kaltura/app/base-config.lock was found. Remove the lock to reconfigure."
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
cat << EOF 
Is your Apache working with SSL?[Y/n]
EOF
	read IS_SSL
fi
if [ "$IS_SSL" != 'Y' -a "$IS_SSL" != 1 -a ! -r "$ANSFILE" ];then
	echo "It is recommended that you do work using HTTPs. Would you like to continue anyway?[N/y]"
	read CONT
	if [ "$CONT" != 'y' ];then
		echo "Exiting."
		exit 2
	fi
else
	# configure SSL:
	KALTURA_SSL_CONF=$KALTURA_APACHE_CONF/kaltura.ssl.conf.template
	while [ -z "$CRT_FILE" ];do
		echo "Please input path to your SSL certificate:"
		read -e CRT_FILE
	done
	while [ -z "$KEY_FILE" ];do
		echo "Please input path to your SSL key:"
		read -e KEY_FILE
	done
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
echo "
IS_SSL=1" >> $RC_FILE 

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
sed -i "s#@SSL_CERTIFICATE_FILE@#$CRT_FILE#g" $KALTURA_APACHE_CONF/kaltura.ssl.conf
sed -i "s#@SSL_CERTIFICATE_KEY_FILE@#$KEY_FILE#g" $KALTURA_APACHE_CONF/kaltura.ssl.conf
ln -fs $KALTURA_APACHE_CONF/kaltura.ssl.conf /etc/httpd/conf.d/  
# clientConfig.verifySSL
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

if [ $CONFIG_CHOICE = 0 ];then
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

service httpd restart
