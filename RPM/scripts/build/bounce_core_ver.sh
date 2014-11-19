#!/bin/bash - 
#===============================================================================
#          FILE: bounce_core_ver.sh
#         USAGE: ./bounce_core_ver.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy , <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 03/09/14 06:59:26 EDT
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error

if [ $# -lt 1 ];then
	echo "Usage $0 <new core ver>"
	exit 1
fi
NEWVER=$1
SOURCES_RC=`dirname $0`/sources.rc
if [ ! -r $SOURCES_RC ];then
	echo "Could not find $SOURCES_RC"
	exit 1
fi
. $SOURCES_RC 
STAMP=`date "+%-a %b %-d %Y"`
cd $RPM_SPECS_DIR

sed -i "s@\(^Version:\)\s*.*\$@\1 $NEWVER@g" kaltura-base.spec kaltura-batch.spec kaltura-front.spec kaltura-release.spec kaltura-server.spec
sed -i "s@\(^Release:\)\s*.*\$@\1 1@g" kaltura-base.spec kaltura-batch.spec kaltura-front.spec kaltura-release.spec kaltura-server.spec
sed -i "s^\(%changelog\)^\1\n* $STAMP $PACKAGER_NAME <$PACKAGER_MAIL> - $NEWVER-1\n- Ver Bounce to $NEWVER\n^" kaltura-base.spec kaltura-batch.spec kaltura-front.spec kaltura-release.spec kaltura-server.spec

rpmbuild -ba kaltura-batch.spec
rpmbuild -ba kaltura-front.spec
rpmbuild -ba kaltura-release.spec
rpmbuild -ba kaltura-server.spec

