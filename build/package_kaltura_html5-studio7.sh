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
ARCHIVE_NAME=$RPM_SOURCES_DIR/$HTML5_APP_STUDIO7_RPM_NAME-$HTML5_APP_STUDIO7_VERSION.tar.gz
wget -q -O$ARCHIVE_NAME --header="Authorization: token ${GITHUB_TOKEN}" $HTML5_APP_STUDIO7_URI
echo "Packaged into $ARCHIVE_NAME"
if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -ba $RPM_SPECS_DIR/$HTML5_APP_STUDIO7_RPM_NAME.spec
fi
