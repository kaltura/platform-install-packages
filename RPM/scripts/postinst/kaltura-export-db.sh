#!/bin/bash - 
#===============================================================================
#          FILE: ./export_db.sh
#         USAGE: ./export_db.sh <schema> <user> <passwd> <port> <host> <output/path> [verbose]
#   DESCRIPTION: 
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy (), jess.portnoy@kaltura.com
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 08/10/12 18:07:22 IDT
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error


if [ $# -lt 6 ]; then
    echo "Usage: $0 <schema> <user> <passwd> <port> <host> <output/path> [verbose]"
    exit 1
fi
TABLE_SCHEMA=$1
DBUSER=$2
DBPASSWD=$3
DBPORT=$4
DBHOST=$5
OUT="$6"
TABLES=`mysql -h$DBHOST -u$DBUSER -p$DBPASSWD -P$DBPORT -B -N -e "select TABLE_NAME from information_schema.TABLES where TABLE_SCHEMA='$TABLE_SCHEMA'"`


if [ ! -d $OUT ]; then
	mkdir -p "$OUT"
fi

for TABLE in $TABLES; do
	if [ -n "$7" ];then
		echo -n "dumping $TABLE_SCHEMA.$TABLE... to $OUT"
	fi
    	mysqldump -h$DBHOST -u$DBUSER -p$DBPASSWD -P$DBPORT --routines --single-transaction $TABLE_SCHEMA $TABLE | gzip > $OUT/$TABLE_SCHEMA.$TABLE.sql.gz
done
