#!/bin/bash -e 
#===============================================================================
#          FILE: package_kaltura_html5lib.sh
#         USAGE: ./package_kaltura_html5lib.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
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
if [ ! -x `which wget 2>/dev/null` ];then
	echo "Need to install wget."
	exit 2
fi

wget -q $HTML5_APP_STUDIO_URI -O $RPM_SOURCES_DIR/$HTML5_APP_STUDIO_NORMALIZED_ARCHIVE_NAME
echo "Packaged into $RPM_SOURCES_DIR/$HTML5_APP_STUDIO_NORMALIZED_ARCHIVE_NAME"
#rpmbuild -ba $RPM_SPECS_DIR/$HTML5_APP_STUDIO_RPM_NAME.spec
