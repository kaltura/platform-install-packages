#!/bin/bash -e 
#===============================================================================
#          FILE: package_kaltura_html5lib.sh
#         USAGE: ./package_kaltura_html5lib.sh 
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
mkdir -p $SOURCE_PACKAGING_DIR/$LIVE_ANALYTICS_FRONT_END_PACKAGE_NAME-$LIVE_ANALYTICS_FRONT_END_VERSION
rm -rf $SOURCE_PACKAGING_DIR/$LIVE_ANALYTICS_FRONT_END_PACKAGE_NAME-$LIVE_ANALYTICS_FRONT_END_VERSION/*
wget -q $LIVE_ANALYTICS_FRONT_END_URI -O$SOURCE_PACKAGING_DIR/$LIVE_ANALYTICS_FRONT_END_PACKAGE_NAME-$LIVE_ANALYTICS_FRONT_END_VERSION/$LIVE_ANALYTICS_FRONT_END_PACKAGE_NAME-$LIVE_ANALYTICS_FRONT_END_VERSION.zip

cd $SOURCE_PACKAGING_DIR/$LIVE_ANALYTICS_FRONT_END_PACKAGE_NAME-$LIVE_ANALYTICS_FRONT_END_VERSION
unzip -qq $LIVE_ANALYTICS_FRONT_END_PACKAGE_NAME-$LIVE_ANALYTICS_FRONT_END_VERSION.zip
tar jcf  $RPM_SOURCES_DIR/$LIVE_ANALYTICS_FRONT_END_PACKAGE_NAME-$LIVE_ANALYTICS_FRONT_END_VERSION.tar.bz2 $LIVE_ANALYTICS_FRONT_END_VERSION
echo "Packaged into $RPM_SOURCES_DIR/$LIVE_ANALYTICS_FRONT_END_PACKAGE_NAME-$LIVE_ANALYTICS_FRONT_END_VERSION.tar.bz2"
if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -ba $RPM_SPECS_DIR/$LIVE_ANALYTICS_FRONT_END_PACKAGE_NAME.spec
fi
