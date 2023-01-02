#!/bin/bash -e 
#===============================================================================
#          FILE: package_kaltura_html5-studio7.sh
#         USAGE: ./package_kaltura_html5-studio7.sh 
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
	echo "Need to install wget."
	exit 2
fi
TMP_ARCHIVE_NAME=$SOURCE_PACKAGING_DIR/$HTML5_APP_STUDIO7_RPM_NAME-$HTML5_APP_STUDIO7_VERSION.tar.gz
ARCHIVE_NAME=$RPM_SOURCES_DIR/$HTML5_APP_STUDIO7_RPM_NAME-$HTML5_APP_STUDIO7_VERSION.tar.gz
wget -q -O$TMP_ARCHIVE_NAME --header="Authorization: token ${GITHUB_TOKEN}" $HTML5_APP_STUDIO7_URI
tar zxf $TMP_ARCHIVE_NAME
mv kaltura-player-studio-v7-* $HTML5_APP_STUDIO7_RPM_NAME-$HTML5_APP_STUDIO7_VERSION
tar zcf $ARCHIVE_NAME $HTML5_APP_STUDIO7_RPM_NAME-$HTML5_APP_STUDIO7_VERSION
rm -rf $HTML5_APP_STUDIO7_RPM_NAME-$HTML5_APP_STUDIO7_VERSION
echo "Packaged into $ARCHIVE_NAME"
if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -ba $RPM_SPECS_DIR/$HTML5_APP_STUDIO7_RPM_NAME.spec
fi
