#!/bin/bash -e 
#===============================================================================
#          FILE: package_x264_source.sh
#         USAGE: ./package_x264_source.sh 
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
cd $RPM_SOURCES_DIR
wget $X264_URI -O $X264_DEST_ARCHIVE_NAME
cd $SOURCE_PACKAGING_DIR 
echo "written to: $RPM_SOURCES_DIR/$X264_DEST_ARCHIVE_NAME"
if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -ba $RPM_SPECS_DIR/$X264_RPM_PACKAGE_NAME.spec
fi

