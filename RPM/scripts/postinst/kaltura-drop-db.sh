#set -o nounset                              # Treat unset variables as an error
#!/bin/bash - 
#===============================================================================
#          FILE: kaltura-drop-db.sh
#         USAGE: ./kaltura-drop-db.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy (), <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 01/24/14 12:50:13 EST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error
if [ ! -r /opt/kaltura/bin/db_actions.rc ];then
        echo "I can't drop without /opt/kaltura/bin/db_actions.rc"
        exit 1
fi
. /opt/kaltura/bin/db_actions.rc
RC_FILE=/etc/kaltura.d/system.ini
if [ ! -r "$RC_FILE" ];then
        echo "Could not find $RC_FILE so, exiting.."
        exit 1 
fi
. $RC_FILE
echo "This will drop the following DBs: 
$DBS 
and remove users:
$DB_USERS

Are you absolutely certain you want this? [n/Y]
"
read AN
if [ "$AN" != 'Y' ];then
        exit 1
fi
echo "root DB passwd:"
read -s DBPASSWD
for i in $DBS;do echo "drop database $i" | mysql -h$DB1_HOST -p$DBPASSWD -u$DB1_USER -P$DB1_PORT ;done
for i in $DB_USERS;do echo "drop user $i" | mysql -h$DB1_HOST -p$DBPASSWD -u$DB1_USER -P$DB1_PORT ;done

