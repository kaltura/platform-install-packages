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
if [ "$3" = 'copy-only' ];then
	JUST_COPY=1
fi
if echo $RPM|grep -q noarch;then
	SUB_PATH=noarch
else
	SUB_PATH=x86_64
fi
#REPO_IP=54.211.235.142
REPO_IP=192.168.70.100
REPO_PREFIX=/opt/vhosts/repo

scp $BASE_RPM_DIR/$RPM root@$REPO_IP:$REPO_PREFIX/releases/$REPO_VER/RPMS/$SUB_PATH
if [ -z $JUST_COPY ];then
	ssh root@$REPO_IP /usr/local/bin/signrpm.ex  $REPO_PREFIX/releases/$REPO_VER/RPMS/$SUB_PATH/$RPM
	ssh root@$REPO_IP createrepo $REPO_PREFIX/releases/$REPO_VER/RPMS/$SUB_PATH
fi
