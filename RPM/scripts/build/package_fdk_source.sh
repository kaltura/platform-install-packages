#!/bin/bash -e 
#===============================================================================
#          FILE: package_ffmpeg_source.sh
#         USAGE: ./package_ffmpeg_source.sh 
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

for i in git;do
	EX_PATH=`which $i 2>/dev/null`
	if [ -z "$EX_PATH" -o ! -x "$EX_PATH" ];then
		echo "Need to install $i."
		exit 2
	fi
done

SOURCES_RC=`dirname $0`/sources.rc
if [ ! -r $SOURCES_RC ];then
	echo "Could not find $SOURCES_RC"
	exit 1
fi
. $SOURCES_RC 
cd $RPM_SOURCES_DIR
cd $SOURCE_PACKAGING_DIR 
git clone $FDK_URI 
tar jcvf  $RPM_SOURCES_DIR/kaltura-fdk-acc-$FDK_VERSION.tar.bz2 fdk-aac 
echo "written to: $RPM_SOURCES_DIR/kaltura-fdk-aac-$FDK_VERSION.tar.bz2"
rpmbuild -ba $RPM_SPECS_DIR/$FDK_RPM_PACKAGE_NAME.spec

