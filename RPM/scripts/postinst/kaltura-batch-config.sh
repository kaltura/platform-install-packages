#!/bin/bash - 
#===============================================================================
#          FILE: kaltura-batch-config.sh
#         USAGE: ./kaltura-batch-config.sh 
#   DESCRIPTION: configure server as a batch node.
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 01/02/14 09:23:34 EST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error

BATCH_SCHEDULER_ID=`< /dev/urandom tr -dc 0-9 | head -c5`
BATCH_PARTNER_ADMIN_SECRET=`echo "select admin_secret from partner where id=-1"|mysql -N -h$DB1_HOST -u$DB1_USER -p$DB1_PASS $DB1_NAME`
#@BATCH_PARTNER_ADMIN_SECRET@
#@BATCH_SCHEDULER_ID@
#@BATCH_URL@
#@CDN_HOST@
#@DB1_HOST@
#@DB1_NAME@
#@DB1_PASS@
#@DB1_USER@
#@DB2_HOST@
#@DB2_NAME@
#@DB3_HOST@
#@INSTALLED_HOSNAME@
#@KALTURA_FULL_VIRTUAL_HOST_NAME@
#@KALTURA_VIRTUAL_HOST_NAME@
#@REPORT_ADMIN_EMAIL@
#@TIME_ZONE@
