#!/bin/bash -e 
#===============================================================================
#          FILE: push_rpm.sh
#         USAGE: ./push_rpm.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy (), <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 03/30/14 07:00:55 EDT
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error
if [ $# -lt 2 ];then
	echo "Usage: $0 /path/to/rpm ver"
	exit 1
fi
RPM=`basename $1`
BASE_RPM_DIR=`dirname $1`
REPO_VER=$2
if echo $RPM|grep -q noarch;then
	SUB_PATH=noarch
else
	SUB_PATH=x86_64
fi
scp $BASE_RPM_DIR/$RPM root@54.211.235.1421:/var/www/html/releases/$REPO_VER/RPMS/$SUB_PATH
ssh root@54.211.235.1421 rpm --addsign  /var/www/html/releases/$REPO_VER/RPMS/$SUB_PATH/$RPM
ssh root@54.211.235.1421 createrepo /var/www/html/releases/$REPO_VER/RPMS/$SUB_PATH

