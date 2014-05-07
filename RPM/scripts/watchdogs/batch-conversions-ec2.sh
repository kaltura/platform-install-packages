#!/bin/bash - 
#===============================================================================
#          FILE: batch-conversions-ec2.sh
#         USAGE: ./batch-conversions-ec2.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 05/07/14 08:23:48 EDT
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error
#!/bin/sh
SYSTEM_INI=/etc/kaltura.d/system.ini
if [ -r "$SYSTEM_INI" ];then
        . /etc/kaltura.d/system.ini
else
        echo "Could not source $SYSTEM_INI:("
        exit 1
fi
if [ $# -lt 3 ];then
        echo "Usage: $0 <AMI id> <warning threshold> <critical threshold>"
        exit 2
fi
AMI_IMG=$1
LOWER_THRESHOLD=$2
UPPER_THRESHOLD=$3
OUT=`php /opt/kaltura/app/plugins/monitor/nagios/exec.php --warning-threshold $LOWER_THRESHOLD --error-threshold $UPPER_THRESHOLD --script "/opt/kaltura/app/tests/monitoring/api_v3/getBatchQueueSize.php --service-url $KALTURA_VIRTUAL_HOST_NAME --job-type CONVERT"`
RC=$?
if [ $RC -eq 1 ];then
echo "Reached WARNING threshold"
# here you can do some actions, for example:
# send yourself an email
# launch instances
fi

# we are at CRITICAL, lets launch

if [ $RC -eq 2 ];then
echo "$OUT
Lunching another batch instance ..
"
knife ec2 server create --availability-zone us-east-1d --flavor m3.medium --image $AMI_IMG --identity-file ~/csi.pem --run-list "recipe[nfs],recipe[kaltura::batch]" --ssh-user ec2-user 2>&1 | tee /tmp/log
fi


