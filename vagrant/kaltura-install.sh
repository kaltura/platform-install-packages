#!/usr/bin/env bash
# exit on errors
set -e
source kaltura-install-config.sh
# flush, stop and disable iptables from init. This for testing purposes ONLY. Make sure to replace with proper FW settings
iptables -F
service iptables stop
chkconfig iptables off
setenforce permissive
yum -y clean all
rpm -ihv --force http://installrepo.kaltura.org/releases/kaltura-release.noarch.rpm
yum -y install mysql mysql-server
service mysqld start
# this might fail if we already set the root password previously
set +e
mysqladmin -u root password "$MYSQL_ROOT_PASSWORD"
set -e
mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "update mysql.user set password=PASSWORD('$MYSQL_ROOT_PASSWORD') where user='root'"
mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e ""
mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1')"
mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "DELETE FROM mysql.user WHERE User=''"
mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "DELETE FROM mysql.db WHERE Db='test' OR Db='test\_%'"
mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "FLUSH PRIVILEGES"
chkconfig mysqld on
# if you prefer using a diff MTA, please relace accordingly
yum install -y postfix
service postfix restart
yum -y install kaltura-server
/opt/kaltura/bin/kaltura-mysql-settings.sh
service memcached restart
service ntpd restart
chkconfig memcached on
chkconfig ntpd on
echo "USER_CONSENT=0" > /opt/kaltura/bin/contact.rc
echo "127.0.0.1 $KALTURA_DOMAIN" >> /etc/hosts
echo "TIME_ZONE=\"UTC\"
KALTURA_FULL_VIRTUAL_HOST_NAME=\"$KALTURA_DOMAIN:80\"
KALTURA_VIRTUAL_HOST_NAME=\"$KALTURA_DOMAIN\"
DB1_HOST=\"127.0.0.1\"
DB1_PORT=\"3306\"
DB1_PASS=\"$MYSQL_ROOT_PASSWORD\"
DB1_NAME=\"kaltura\"
DB1_USER=\"kaltura\"
SERVICE_URL=\"http://$KALTURA_DOMAIN:80\"
SPHINX_SERVER1=\"127.0.0.1\"
SPHINX_SERVER2=\" \"
DWH_HOST=\"127.0.0.1\"
DWH_PORT=\"3306\"
SPHINX_DB_HOST=\"127.0.0.1\"
SPHINX_DB_PORT=\"3306\"
ADMIN_CONSOLE_ADMIN_MAIL=\"$KALTURA_ADMIN_EMAIL\"
ADMIN_CONSOLE_PASSWORD=\"$KALTURA_ADMIN_PASSWORD\"
CDN_HOST=\"$KALTURA_DOMAIN\"
KALTURA_VIRTUAL_HOST_PORT=\"80\"
SUPER_USER=\"root\"
SUPER_USER_PASSWD=\"vagrant\"
ENVIRONMENT_NAME=\"$KALTURA_ENVIRONMENT_NAME\"
DWH_PASS=\"$MYSQL_ROOT_PASSWORD\"
PROTOCOL=\"http\"
RED5_HOST=\"$KALTURA_DOMAIN\"
USER_CONSENT=\"0\"
CONFIG_CHOICE=\"0\"
IS_SSL=\"N\"" > kaltura.ans
/opt/kaltura/bin/kaltura-config-all.sh kaltura.ans
unzip oflaDemo-r4472-java6.war -d/usr/lib/red5/webapps/oflaDemo
service red5 restart
/opt/kaltura/bin/kaltura-red5-config.sh
