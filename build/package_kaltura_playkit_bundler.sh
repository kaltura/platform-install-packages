#!/bin/bash -e 
#===============================================================================
#          FILE: package_kaltura_playkit_bundler.sh
#         USAGE: ./package_kaltura_playkit_bundler.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 01/14/14 11:46:43 EST
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
	echo "Need to install curl."
	exit 2
fi

curl -H "Authorization: token $GITHUB_TOKEN" -H 'Accept: application/vnd.github.v3.raw' -s $KALTURA_PLAYKIT_BUNDLER_URI -L > $RPM_SOURCES_DIR/${KALTURA_PLAYKIT_BUNDLER_RPM_NAME}-${KALTURA_PLAYKIT_BUNDLER_VERSION}.tar.gz
echo "Packaged into $RPM_SOURCES_DIR/${KALTURA_PLAYKIT_BUNDLER_RPM_NAME}-${KALTURA_PLAYKIT_BUNDLER_VERSION}.tar.gz"
if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -bb $RPM_SPECS_DIR/$KALTURA_PLAYKIT_BUNDLER_RPM_NAME.spec
fi
