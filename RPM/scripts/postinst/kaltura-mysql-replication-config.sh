#!/bin/sh
#         USAGE: ./kaltura-mysql-replication-config.sh 
#   DESCRIPTION:
#       OPTIONS: rep_user rep_user_passw master_ip operation <master||slave> 
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy (), jess.portnoy@kaltura.com
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 11/29/2013 03:26:51 PM IST
#      REVISION:  ---
#===============================================================================

if [ $# -lt 4 ];then
	echo "Usage: $0 rep_user rep_user_passw master_ip operation <master||slave>"
	exit 1
fi

if grep -q '^#.*configured by Kaltura' /etc/my.cnf ;then
	echo -en "$0 already ran here.\nIf you want to re-run, please edit /etc/my.cnf and remove the comment: 'configured by Kaltura' and re-run $0.\n"
	exit 1
fi
KALT_REP_USER=$1
KALT_REP_PASSWD=$2
MASTER=$3
OPERATION=$4
DATE=`date`
if [ $OPERATION = 'master' ];then
	# master:
	sed -i "s@^\[mysqld\]@[mysqld]\n#Master configured by Kaltura on: $DATE\nlog-bin=mysql-bin\nserver-id = 1\nauto_increment_increment = 10\nauto_increment_offset = 1\n@" /etc/my.cnf
	SQL=`cat <<EOF
	create user $KALT_REP_USER@'%' identified by '$KALT_REP_PASSWD';
	GRANT SELECT, PROCESS, FILE, SUPER, REPLICATION CLIENT, REPLICATION SLAVE, RELOAD ON kaltura.* TO $KALT_REP_USER@'%';
	Flush Privileges;
	FLUSH TABLES WITH READ LOCK;
EOF`

elif [ $OPERATION = 'slave' ];then
	# slave:
	sed -i "s@^\[mysqld\]@[mysqld]\n#Slave configured by Kaltura on: $DATE\nserver-id = 2\n@" /etc/my.cnf
	SQL=`cat <<EOF
	CHANGE MASTER TO
	MASTER_HOST='$MASTER',
	MASTER_USER='$KALT_REP_USER',
	MASTER_PASSWORD='$KALT_REP_PASSWD';
EOF`
else
	echo "$OPERATION can be master or slave only"
	exit 1
fi
echo "$SQL" |mysql -uroot -p
if [ $? -ne 0 ];then
	echo "Something happened to me, please check this :("
else
	echo "Replication setup is complete :) I shall be restarting MySQL now."
	/etc/init.d/mysqld restart
fi
