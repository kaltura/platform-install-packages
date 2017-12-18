#!/bin/bash - 
#===============================================================================
#          FILE: kaltura-db-config.sh
#         USAGE: ./kaltura-db-config.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy, <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 01/09/14 04:57:40 EST
#      REVISION:  ---
#===============================================================================
#set -o nounset                              # Treat unset variables as an error

KALTURA_FUNCTIONS_RC=`dirname $0`/kaltura-functions.rc
if [ ! -r "$KALTURA_FUNCTIONS_RC" ];then
	echo "Could not find $KALTURA_FUNCTIONS_RC so, exiting.."
	exit 3
fi
. $KALTURA_FUNCTIONS_RC
if [ "$#" -lt 4 ];then
	echo -e "${BRIGHT_RED}Usage: $0 <mysql-hostname> <mysql-super-user> <mysql-super-user-passwd> <mysql-port> [upgrade]${NORMAL}"
	exit 1
fi

RC_FILE=/etc/kaltura.d/system.ini
if [ ! -r "$RC_FILE" ];then
	echo -e "${BRIGHT_RED}ERROR: could not find $RC_FILE so, exiting..${NORMAL}"
	exit 2
fi
. $RC_FILE
DB_ACTIONS_RC=`dirname $0`/db_actions.rc
if [ ! -r "$DB_ACTIONS_RC" ];then
	echo -e "${BRIGHT_RED}ERROR: could not find $DB_ACTIONS_RC so, exiting..${NORMAL}"
	exit 3
fi
. $DB_ACTIONS_RC
KALTURA_FUNCTIONS_RC=`dirname $0`/kaltura-functions.rc
if [ ! -r "$KALTURA_FUNCTIONS_RC" ];then
	echo -e "${BRIGHT_RED}ERROR: could not find $KALTURA_FUNCTIONS_RC so, exiting..${NORMAL}"
	exit 3
fi
. $KALTURA_FUNCTIONS_RC
trap 'my_trap_handler "${LINENO}" $?' ERR
send_install_becon "`basename $0`" "install_start" 0 

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
echo -e "${CYAN}Checking MySQL version..${NORMAL}"
MYVER=`echo "select version();" | mysql -h$MYSQL_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT -N`
MYMAJVER=`echo $MYVER| awk -F "." '{print $1}'`
MYMINORVER=`echo $MYVER| awk -F "." '{print $2}'`

if [ "$MYMAJVER" -ne 5 ];then
	echo -e "${BRIGHT_RED}Your version of MySQL is not compatible with Kaltura at the moment. 
Please install and configure MySQL 5.1 according to the instructions on the Kaltura install manual before proceeding with the Kaltura installation.${NORMAL}"
	exit 1
else
	echo -e "${CYAN}Ver $MYVER found compatible${NORMAL}"
fi

if [ $? -ne 0 ];then
cat << EOF
Failed to run:
# mysql -h$MYSQL_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT."
Check your settings."
EOF
	exit 4
fi
if ! check_mysql_settings $MYSQL_SUPER_USER $MYSQL_SUPER_USER_PASSWD $MYSQL_HOST $MYSQL_PORT ;then
	if [ $MYSQL_HOST = 'localhost' -o $MYSQL_HOST = '127.0.0.1' ];then
		echo "Your MySQL settings are incorrect, do you wish to run $BASE_DIR/bin/kaltura-mysql-settings.sh in order to correct them? [Y/n]"
		read ANS
		if [ "$ANS" = "Y" ];then
			$BASE_DIR/bin/kaltura-mysql-settings.sh
		else
			echo -e "${BRIGHT_RED}Please adjust your MySQL configuration manually and re-run.${NORMAL}" 
			exit 8
		fi
	else
		echo "Your MySQL settings are incorrect, please set the following in your MySQL conf file [my.cnf]:
lower_case_table_names = 1
innodb_file_per_table
innodb_log_file_size=32M
open_files_limit = 20000
max_allowed_packet = 16M

Restart the MySQL daemon and re-run the config script.
"
		exit 7
	fi
fi
trap - ERR
if [ -z "$POPULATE_ONLY" ];then
	# check whether the 'kaltura' already exists:
	echo "use kaltura" | mysql -h$MYSQL_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT $KALTURA_DB 2> /dev/null
	if [ $? -eq 0 ];then
cat << EOF
The $KALTURA_DB DB seems to already be installed.

if you meant to perform an upgrade? run with:
# $0 $MYSQL_HOST $MYSQL_SUPER_USER $MYSQL_SUPER_USER_PASSWD $MYSQL_PORT upgrade

Otherwise, do you wish to remove the existing DB [n/Y]?

EOF
		read REMOVE
		if [ $REMOVE = "Y" ];then
			`dirname $0`/kaltura-drop-db.sh
		else
			exit 5
		fi
	fi 
trap 'my_trap_handler "${LINENO}" $?' ERR

	# this is the DB creation part, we want to exit if something fails here:
	set -e

	# create users:
	USER_EXISTS=`echo "SELECT EXISTS(SELECT 1 FROM mysql.user WHERE user = 'kaltura');" | mysql -h$MYSQL_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT`
	if [ "$USER_EXISTS" != "1" ];then
		echo "CREATE USER kaltura;"
		echo "CREATE USER kaltura@'%' IDENTIFIED BY '$DB1_PASS' ;"  | mysql -h$MYSQL_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT
	fi
	USER_EXISTS=`echo "SELECT EXISTS(SELECT 1 FROM mysql.user WHERE user = 'etl');" | mysql -h$MYSQL_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT`
	if [ "$USER_EXISTS" != "1" ];then
		echo "CREATE USER etl;"
		echo "CREATE USER etl@'%' IDENTIFIED BY '$DWH_PASS' ;"  | mysql -h$MYSQL_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT
	fi
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
	echo -e "${BRIGHT_RED}Please check your setup and then run $0 again.${NORMAL}"
cat << EOF

Do you wish to remove the Kaltura DBs? [n/Y]
Hit 'n' to keep it for debugging purposes.

EOF
	read REMOVE
	if [ "$REMOVE" = "Y" ];then
		`dirname $0`/kaltura-drop-db.sh
	fi
	exit 6
fi

echo "Cleaning cache.."
find $APP_DIR/cache/ -type f -exec rm {} \;
rm -f $LOG_DIR/installPlugins.log $LOG_DIR/insertDefaults.log $LOG_DIR/insertPermissions.log $LOG_DIR/insertContent.log

echo -e "${CYAN}Populating DB with data.. please wait..${NORMAL}"
echo -e "${CYAN}Output for $APP_DIR/deployment/base/scripts/installPlugins.php being logged into $LOG_DIR/installPlugins.log ${NORMAL}"
php $APP_DIR/deployment/base/scripts/installPlugins.php >> $LOG_DIR/installPlugins.log  2>&1
echo -e "${CYAN}Output for $APP_DIR/deployment/base/scripts/insertDefaults.php being logged into $LOG_DIR/insertDefaults.log ${NORMAL}"
php $APP_DIR/deployment/base/scripts/insertDefaults.php $APP_DIR/deployment/base/scripts/init_data >> $LOG_DIR/insertDefaults.log  2>&1
echo -e "${CYAN}Output for $APP_DIR/deployment/base/scripts/insertPermissions.php being logged into $LOG_DIR/insertPermissions.log ${NORMAL}"
php $APP_DIR/deployment/base/scripts/insertPermissions.php  >> $LOG_DIR/insertPermissions.log 2>&1
echo -e "${CYAN}Output for $APP_DIR/deployment/base/scripts/insertContent.php being logged into $LOG_DIR/insertContent.log ${NORMAL}"
php $APP_DIR/deployment/base/scripts/insertContent.php >> $LOG_DIR/insertContent.log  2>&1
if [ $? -ne 0 ];then
cat << EOF
Failed to run:
php $APP_DIR/deployment/base/scripts/insertContent.php >> $LOG_DIR/insertContent.log  2>&1
EOF
	echo -e "${BRIGHT_RED}Please check your setup and then run $0 again.${NORMAL}"
	exit 8
fi

if [ "$IS_SSL" = 'Y' -o "$IS_SSL" = 1 -o "$IS_SSL" = 'y' -o "$IS_SSL" = 'true' ];then
# force KMC login via HTTPs.
	php $APP_DIR/deployment/base/scripts/insertPermissions.php -d $APP_DIR/deployment/permissions/ssl/ > /dev/null 2>&1
fi

KMC_VERSION=`grep "^kmc_version" /opt/kaltura/app/configurations/local.ini|awk -F "=" '{print $2}'|sed 's@\s*@@g'`
echo -e "${BRIGHT_BLUE}Generating UI confs..${NORMAL}"
php $APP_DIR/deployment/uiconf/deploy_v2.php --ini=$WEB_DIR/flash/kmc/$KMC_VERSION/config.ini >> $LOG_DIR/deploy_v2.log  2>&1
#for i in $APP_DIR/deployment/updates/scripts/patches/*.sh;do
#	$i
#done
HTML5_STUDIO_VERSION=`rpm -q kaltura-html5-studio --queryformat %{version}`
if [ -r $BASE_DIR/apps/studio/$HTML5_STUDIO_VERSION/studio.ini ];then
	php $BASE_DIR/app/deployment/uiconf/deploy_v2.php --ini=$BASE_DIR/apps/studio/$HTML5_STUDIO_VERSION/studio.ini >> /dev/null
	sed -i "s@^\(studio_version\s*=\)\(.*\)@\1 $HTML5_STUDIO_VERSION@g" -i $BASE_DIR/app/configurations/local.ini
fi
find  $WEB_DIR/content/generatedUiConf -type d -exec chmod 775 {} \;

set +e


if [ "$DB1_HOST" = `hostname` -o "$DB1_HOST" = '127.0.0.1' -o "$DB1_HOST" = 'localhost' ];then
	if [ `rpm -qa "Percona-Server-server*"` ]; then 
		ln -sf $BASE_DIR/app/configurations/monit/monit.avail/percona.rc $BASE_DIR/app/configurations/monit/monit.d/enabled.mysqld.rc
	else
		ln -sf $BASE_DIR/app/configurations/monit/monit.avail/mysqld.rc $BASE_DIR/app/configurations/monit/monit.d/enabled.mysqld.rc
	fi
	service kaltura-monit stop >> /dev/null 2>&1
	service kaltura-monit restart
fi
send_install_becon "`basename $0`" "install_success" 0 
