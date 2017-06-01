#!/bin/bash -e 
#===============================================================================
#          FILE: package_kaltura_push_server.sh
#         USAGE: ./package_kaltura_push_server.sh
#   DESCRIPTION: 
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy (), <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 30/05/17 08:46:43 EST
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
wget $PUSH_SERVER_URI -O$RPM_SOURCES_DIR/$PUSH_SERVER_RPM_NAME-v$PUSH_SERVER_VERSION.tar.gz
echo "Packaged into $PUSH_SERVER_RPM_NAME-v$PUSH_SERVER_VERSION.tar.gz"
if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -bb $RPM_SPECS_DIR/$PUSH_SERVER_RPM_NAME.spec
fi
