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
mysql -h$MYSQL_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT
if [ $? -ne 0 ];then
cat << EOF
Failed to run mysql -h$MYSQL_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT."
Check your settings."
EOF
	exit 3
fi

# check whether the 'kaltura' already exists:
echo "show tables" | mysql -h$MYSQL_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT $KALTURA_DB
if [ $? -eq 0 ];then
cat << EOF
The $KALTURA_DB seems to already be installed.
Did you mean to perform an upgrade? if so, run with:
$MYSQL_HOST -u$MYSQL_SUPER_USER -p$MYSQL_SUPER_USER_PASSWD -P$MYSQL_PORT upgrade
EOF
	exit 4
fi 

# Create DBs, tables, users here:

# SQL files to run will reside in a text file

# kaltura
#@BASE_DIR@/app/deployment/base/sql/01.kaltura_ce_tables.sql
#@BASE_DIR@/app/deployment/base/sql/04.stored_procedures.sql
#user prives for $DB1_USER on $DB1_NAME:
#INSERT,UPDATE,DELETE,SELECT

#sphinx_log
# @BASE_DIR@/app/deployment/base/sql/01.kaltura_sphinx_ce_tables.sql
#user prives for $DB1_USER:
#SELECT,INSERT,UPDATE

# kalturadw
#user prives for $DWH_USER:
#INSERT,UPDATE,DELETE,SELECT,EXECUTE
# kalturadw_bisources

#user prives for $DWH_USER:
# kalturadw_ds
# INSERT,UPDATE,DELETE,SELECT,EXECUTE
# 
#user privs for $DWH_USER:
# kalturalog 
# INSERT,UPDATE,DELETE,SELECT,LOCK TABLES




