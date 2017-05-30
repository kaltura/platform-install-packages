#!/bin/bash -e 
#===============================================================================
#          FILE: package_kaltura_async_api_proxy.sh
#         USAGE: ./package_kaltura_async_api_proxy.sh
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
wget $ASYNC_API_PROXY_URI -O$RPM_SOURCES_DIR/$ASYNC_API_PROXY_RPM_NAME-v$ASYNC_API_PROXY_VERSION.tar.gz
echo "Packaged into $ASYNC_API_PROXY_RPM_NAME-v$ASYNC_API_PROXY_VERSION.tar.gz"
if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -bb $RPM_SPECS_DIR/$ASYNC_API_PROXY_RPM_NAME.spec
fi
