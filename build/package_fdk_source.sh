#!/bin/bash -e 
#===============================================================================
#          FILE: package_fdk_source.sh
#         USAGE: ./package_fdk_source.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy (), <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 12/29/13 05:24:47 EST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error

if [ ! -x "`which wget 2>/dev/null`" ];then
	echo "Need to install wget."
	exit 2
fi

SOURCES_RC=`dirname $0`/sources.rc
if [ ! -r $SOURCES_RC ];then
	echo "Could not find $SOURCES_RC"
	exit 1
fi
. $SOURCES_RC 
cd $SOURCE_PACKAGING_DIR 

wget $FDK_URI -O $RPM_SOURCES_DIR/v$FDK_VERSION.zip
if [ $? -eq 0 ];then
	echo "Packaged to v$FDK_VERSION.zip"
else
	echo "Unable to download $FDK_URI" >&2
	exit 1
fi

if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -ba $RPM_SPECS_DIR/kaltura-fdk-aac.spec
fi

