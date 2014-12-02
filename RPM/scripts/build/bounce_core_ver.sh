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
BASE_DIR=`dirname $0`


for i in $RPM_SPECS_DIR/kaltura-batch.spec $RPM_SPECS_DIR/kaltura-front.spec $RPM_SPECS_DIR/kaltura-release.spec $RPM_SPECS_DIR/kaltura-server.spec;do
	$BASE_DIR/bounce_rpm_ver.sh $i $NEWVER 1
	rpmbuild -ba $i
done

# we run this one of the loop because we don't want to build it yet since we need to manually add the changelog to it.
# the rest can do with the default "bounce to $VER" message since they'e just meta packages.
`dirname $0`/bounce_rpm_ver.sh $RPM_SPECS_DIR/kaltura-base.spec $NEWVER 1

