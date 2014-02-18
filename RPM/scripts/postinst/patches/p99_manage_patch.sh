#!/bin/bash - 
#===============================================================================
#          FILE: p99_manage_patch.sh
#         USAGE: ./p99_manage_patch.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy (), <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 02/18/14 10:45:12 EST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error
# this is to fix https://github.com/kaltura/platform-install-packages/issues/28
. /etc/kaltura.d/system.ini
echo "update kuser set is_Admin=1  where partner_id=99;"|mysql -N -h$DB1_HOST -u $DB1_USER -p$DB1_PASS $DB1_NAME
echo "insert into user_login_data values (NULL,'templi@temply.ll','ninty','nine','7e9734338063249e3d1d628bcc2ece2c032f78c3','673d2cbecbdbc3916c1f5f1a54a10b7a',99,NULL,CURDATE(),CURDATE(),'')" | mysql  -N -h$DB1_HOST -u $DB1_USER -p$DB1_PASS $DB1_NAME
USER_LOGIN_ID=`echo "select id from user_login_data where first_name = 'ninty' and last_name = 'nine';"|mysql -N -h$DB1_HOST -u $DB1_USER -p$DB1_PASS $DB1_NAME`
echo "update kuser set login_data_id=$USER_LOGIN_ID where partner_id=99;"|mysql -N -h$DB1_HOST -u $DB1_USER -p$DB1_PASS $DB1_NAME
USER_ROLE_ID=`echo "select id from user_role where name='manager' and partner_id=99;"|mysql -N -h$DB1_HOST -u $DB1_USER -p$DB1_PASS $DB1_NAME`
echo "insert into kuser_to_user_role values (NULL,7,17,CURDATE(),CURDATE());"|mysql -N -h$DB1_HOST -u $DB1_USER -p$DB1_PASS $DB1_NAME


