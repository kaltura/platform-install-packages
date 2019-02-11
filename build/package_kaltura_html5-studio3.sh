#!/bin/bash -e 
#===============================================================================
#          FILE: package_kaltura_html5-studio3.sh
#         USAGE: ./package_kaltura_html5-studio3.sh 
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
mkdir -p $SOURCE_PACKAGING_DIR/$HTML5_APP_STUDIO3_RPM_NAME-$HTML5_APP_STUDIO3_VERSION
rm -rf $SOURCE_PACKAGING_DIR/$HTML5_APP_STUDIO3_RPM_NAME-$HTML5_APP_STUDIO3_VERSION/*
wget -q $HTML5_APP_STUDIO3_URI -O$SOURCE_PACKAGING_DIR/$HTML5_APP_STUDIO3_RPM_NAME-$HTML5_APP_STUDIO3_VERSION/$HTML5_APP_STUDIO3_NORMALIZED_ARCHIVE_NAME
cd $SOURCE_PACKAGING_DIR/$HTML5_APP_STUDIO3_RPM_NAME-$HTML5_APP_STUDIO3_VERSION
unzip -qq $HTML5_APP_STUDIO3_NORMALIZED_ARCHIVE_NAME
rm $HTML5_APP_STUDIO3_NORMALIZED_ARCHIVE_NAME
cd ../
tar jcf  $RPM_SOURCES_DIR/$HTML5_APP_STUDIO3_RPM_NAME-$HTML5_APP_STUDIO3_VERSION.tar.bz2 $HTML5_APP_STUDIO3_RPM_NAME-$HTML5_APP_STUDIO3_VERSION
echo "Packaged into $RPM_SOURCES_DIR/$HTML5_APP_STUDIO3_RPM_NAME-$HTML5_APP_STUDIO3_VERSION.tar.bz2"
if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -ba $RPM_SPECS_DIR/$HTML5_APP_STUDIO3_RPM_NAME.spec
fi
