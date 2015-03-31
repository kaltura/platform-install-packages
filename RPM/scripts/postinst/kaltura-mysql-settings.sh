#!/bin/bash - 
#===============================================================================
#          FILE: kaltura-mysql-settings.sh
#         USAGE: ./kaltura-mysql-settings.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy (), <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 01/24/14 12:48:32 EST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error
MY_CNF=/etc/my.cnf
cp $MY_CNF $MY_CNF.orig
sed -i '/^lower_case_table_names = 1$/d' $MY_CNF
sed -i '/^open_files_limit.*$/d' $MY_CNF
sed -i '/^max_allowed_packet.*$/d' $MY_CNF
sed -i 's@^\[mysqld\]$@[mysqld]\nlower_case_table_names = 1\n@' $MY_CNF
sed -i 's@^\[mysqld\]$@[mysqld]\ninnodb_file_per_table\n@' $MY_CNF
sed -i 's@^\[mysqld\]$@[mysqld]\ninnodb_log_file_size=32M\n@' $MY_CNF
sed -i 's@^\[mysqld\]$@[mysqld]\nopen_files_limit = 20000\n@' $MY_CNF
sed -i 's@^\[mysqld\]$@[mysqld]\nmax_allowed_packet = 16M\n@' $MY_CNF
mv /var/lib/mysql/ib_logfile0 /var/lib/mysql/ib_logfile0.old
mv /var/lib/mysql/ib_logfile1 /var/lib/mysql/ib_logfile1.old

if rpm -q mysql-server 2>/dev/null;then
        service mysqld restart
elif rpm -q mariadb-server 2>/dev/null;then
        service mariadb restart
fi
