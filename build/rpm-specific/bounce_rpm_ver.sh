#!/bin/bash - 
#===============================================================================
#          FILE: bounce_ver.sh
#         USAGE: ./bounce_ver.sh 
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
	echo "Usage $0 <path/to/spec> <new ver> <new rev>"
	exit 1
fi
SPEC_FILE=$1
NEWVER=$2
if [ -n "$3" ];then
	REV=$3
else
	REV=1
fi
SOURCES_RC=~/sources/platform-install-packages/build/sources.rc
if [ ! -r $SOURCES_RC ];then
	echo "Could not find $SOURCES_RC"
	exit 1
fi
. $SOURCES_RC 
STAMP=`date "+%-a %b %-d %Y"`
cd $RPM_SPECS_DIR

sed -i "s@\(^Version:\)\s*.*\$@\1 $NEWVER@g" $SPEC_FILE
sed -i "s@\(^Release:\)\s*.*\$@\1 $REV@g" $SPEC_FILE
sed -i "s^\(%changelog\)^\1\n* $STAMP $PACKAGER_NAME <$PACKAGER_MAIL> - $NEWVER-1\n- Ver Bounce to $NEWVER\n^" $SPEC_FILE


