#!/bin/bash - 
#===============================================================================
#          FILE: kaltura-db-config.sh
#         USAGE: ./kaltura-db-config.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy, <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 01/09/14 04:57:40 EST
#      REVISION:  ---
#===============================================================================
#set -o nounset                              # Treat unset variables as an error

if [ "$#" -lt 4 ];then
	echo "Usage: $0 <mysql-hostname> <mysql-super-user> <mysql-super-user-passwd> <mysql-port> [upgrade]"
	exit 1
fi

RC_FILE=/etc/kaltura.d/system.ini
if [ ! -r "$RC_FILE" ];then
	echo "Could not find $RC_FILE so, exiting.."
	exit 2
fi
. $RC_FILE
DB_ACTIONS_RC=`dirname $0`/db_actions.rc
if [ ! -r "$DB_ACTIONS_RC" ];then
	echo "Could not find $DB_ACTIONS_RC so, exiting.."
	exit 3
fi
. $DB_ACTIONS_RC
KALTURA_FUNCTIONS_RC=`dirname $0`/kaltura-functions.rc
if [ ! -r "$KALTURA_FUNCTIONS_RC" ];then
	echo "Could not find $KALTURA_FUNCTIONS_RC so, exiting.."
	exit 3
fi
. $KALTURA_FUNCTIONS_RC

MYSQL_HOST=$1
MYSQL_SUPER_USER=$2
MYSQL_SUPER_USER_PASSWD=$3
MYSQL_PORT=$4
IS_UPGRADE=$5

if [ "$IS_UPGRADE" = 'upgrade' ];then
	echo "calling upgrade script instead."
	# the upgrade script is more complex naturally.. will include a check for schema
	# decide how far back to run alter scripts, etc.
fi
KALTURA_DB=$DB1_NAME

# check DB connectivity:
echo "Checking MySQL version.."
echo "select version();" | mysql -h$MYSQL_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT -N
if [ $? -ne 0 ];then
cat << EOF
Failed to run:
# mysql -h$MYSQL_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT."
Check your settings."
EOF
	exit 4
fi
if ! check_mysql_settings $MYSQL_SUPER_USER $MYSQL_SUPER_USER_PASSWD $MYSQL_HOST $MYSQL_PORT ;then
	exit 7
fi
if [ -z "$POPULATE_ONLY" ];then
	# check whether the 'kaltura' already exists:
	echo "use kaltura" | mysql -h$MYSQL_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT $KALTURA_DB 2> /dev/null
	if [ $? -eq 0 ];then
cat << EOF
The $KALTURA_DB DB seems to already be installed.

Did you mean to perform an upgrade? if so, run with:
# $0 $MYSQL_HOST $MYSQL_SUPER_USER $MYSQL_SUPER_USER_PASSWD $MYSQL_PORT upgrade

EOF
		exit 5
	fi 

	# this is the DB creation part, we want to exit if something fails here:
	set -e

	# create users:
	for DB_USER in $DB_USERS;do
		echo "CREATE USER ${DB_USER};"
		echo "CREATE USER ${DB_USER} IDENTIFIED BY '$DB1_PASS' ;"  | mysql -h$MYSQL_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT
	done
	# create the DBs:
	for DB in $DBS;do 
		echo "CREATE DATABASE $DB;"
		echo "CREATE DATABASE $DB;" | mysql -h$MYSQL_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT
		PRIVS=${DB}_PRIVILEGES
		DB_USER=${DB}_USER
		# apply privileges:
		echo "GRANT ${!PRIVS} ON $DB.* TO '${!DB_USER}'@'%';FLUSH PRIVILEGES;" | mysql -h$MYSQL_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT
		DB_SQL_FILES=${DB}_SQL_FILES
		# run table creation scripts:
		for SQL in ${!DB_SQL_FILES};do 
			mysql -h$MYSQL_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT $DB < $SQL
		done
	done
	echo "GRANT SELECT ON kaltura.* TO 'etl'@'%';FLUSH PRIVILEGES;" | mysql -h$MYSQL_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT

	# DB schema created. Before we move onto populating, lets check MySQL and Sphinx connectivity.
fi
set +e

echo "Checking connectivity to needed daemons..."
if ! check_connectivity $DB1_USER $DB1_PASS $DB1_HOST $DB1_PORT $SPHINX_HOST $SERVICE_URL;then
	echo "Please check your setup and then run $0 again."
	exit 6
fi

echo "Cleaning cache.."
rm -rf $APP_DIR/cache/*
sed -i "s@?a=12@@g" $APP_DIR/deployment/base/scripts/init_content/ui_conf/*
echo "Populating DB with data.. please wait.."
echo "Output for $APP_DIR/deployment/base/scripts/installPlugins.php being logged into $LOG_DIR/installPlugins.log"
php $APP_DIR/deployment/base/scripts/installPlugins.php >> $LOG_DIR/installPlugins.log  2>&1
echo "Output for $APP_DIR/deployment/base/scripts/insertDefaults.php being logged into $LOG_DIR/insertDefaults.log"
php $APP_DIR/deployment/base/scripts/insertDefaults.php $APP_DIR/deployment/base/scripts/init_data >> $LOG_DIR/insertDefaults.log  2>&1
echo "Output for $APP_DIR/deployment/base/scripts/insertPermissions.php being logged into $LOG_DIR/insertPermissions.log"
php $APP_DIR/deployment/base/scripts/insertPermissions.php  >> $LOG_DIR/insertPermissions.log 2>&1
echo "Output for $APP_DIR/deployment/base/scripts/insertContent.php being logged into $LOG_DIR/insertContent.log"
php $APP_DIR/deployment/base/scripts/insertContent.php >> $LOG_DIR/insertContent.log  2>&1

if [ -n "$IS_SSL" ];then
# force KMC login via HTTPs.
	php $APP_DIR/deployment/base/scripts/insertPermissions.php -d $APP_DIR/deployment/permissions/ssl/ > /dev/null 2>&1
fi

KMC_VERSION=`grep "^kmc_version" /opt/kaltura/app/configurations/base.ini|awk -F "=" '{print $2}'|sed 's@\s*@@g'`
echo "Generating UI confs.."
php $APP_DIR/deployment/uiconf/deploy_v2.php --ini=$WEB_DIR/flash/kmc/$KMC_VERSION/config.ini >> $LOG_DIR/deploy_v2.log  2>&1
for i in $APP_DIR/deployment/updates/scripts/patches/*.sh;do
	$i
done
find  $WEB_DIR/content/generatedUiConf -type d -exec chmod 775 {} \;

set +e
rm -rf $BASE_DIR/cache/*
rm -f $APP_DIR/log/kaltura-*.log


# DWH setup:
# @DWH_DIR@/setup/dwh_setup.sh


if [ "$DB1_HOST" = `hostname` -o "$DB1_HOST" = '127.0.0.1' -o "$DB1_HOST" = 'localhost' ];then
	ln -sf $BASE_DIR/app/configurations/monit/monit.avail/mysqld.rc $BASE_DIR/app/configurations/monit/monit.d/enabled.mysqld.rc
	/etc/init.d/kaltura-monit restart
fi
