#!/bin/bash -e 
#===============================================================================
#          FILE: package_kaltura_media-server.sh
#         USAGE: ./package_kaltura_play-server.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy (), <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 31/05/15 14:46:43 EST
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error
SOURCES_RC=`dirname $0`/sources.rc
if [ ! -r $SOURCES_RC ];then
	echo "Could not find $SOURCES_RC"
	exit 1
fi
. $SOURCES_RC 
if [ ! -x "`which wget 2>/dev/null`" ];then
	echo "Need to install wget."
	exit 2
fi
mkdir -p $RPM_SOURCES_DIR/$KALTURA_PLAYSERVER_RPM_NAME

wget $KALTURA_PLAYSERVER_URI -O$RPM_SOURCES_DIR/$KALTURA_PLAYSERVER_RPM_NAME-$KALTURA_PLAYSERVER_VERSION.zip
echo "Packaged into $RPM_SOURCES_DIR/$KALTURA_PLAYSERVER_RPM_NAME-$KALTURA_PLAYSERVER_VERSION.zip"

if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -ba $RPM_SPECS_DIR/$KALTURA_PLAYSERVER_RPM_NAME.spec
fi
