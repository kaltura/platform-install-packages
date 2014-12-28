#!/bin/bash -e 
#===============================================================================
#          FILE: package_red5_source.sh
#         USAGE: ./package_red5_source.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 12/29/13 05:24:47 EST
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error

if [ ! -x "`which unzip 2>/dev/null`" ];then
	echo "Need to install unzip."
	exit 2
fi
if [ ! -x "`which wget 2>/dev/null`" ];then
	echo "Need to install wget."
	exit 2
fi
if [ ! -x "`which mvn 2>/dev/null`" ];then
	echo "Need to install maven."
	exit 2
fi

SOURCES_RC=`dirname $0`/sources.rc
if [ ! -r $SOURCES_RC ];then
	echo "Could not find $SOURCES_RC"
	exit 1
fi
. $SOURCES_RC 
cd $SOURCE_PACKAGING_DIR 
wget $RED5_JAVA_URI -O $RPM_SOURCES_DIR/$RED5_RPM_PACKAGE_NAME-$RED5_VERSION.zip 

echo "written to: $RPM_SOURCES_DIR/$RED5_RPM_PACKAGE_NAME-$RED5_VERSION.zip"
rpmbuild -ba $RPM_SPECS_DIR/$RED5_RPM_PACKAGE_NAME.spec

