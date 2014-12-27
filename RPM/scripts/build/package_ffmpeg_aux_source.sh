#!/bin/bash -e 
#===============================================================================
#          FILE: package_ffmpeg_aux_source.sh
#         USAGE: ./package_ffmpeg_aux_source.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Tan-Tan, <Jonathan.Kanarek@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 12/24/14
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error

if [ ! -x "`which curl 2>/dev/null`" ];then
	echo "Need to install curl."
	exit 2
fi

SOURCES_RC=`dirname $0`/sources.rc
if [ ! -r $SOURCES_RC ];then
	echo "Could not find $SOURCES_RC"
	exit 1
fi
. $SOURCES_RC 

cd $RPM_SOURCES_DIR
curl $FFMPEG_AUX_URI > ffmpeg-$FFMPEG_AUX_VERSION.tar.bz2
cd $SOURCE_PACKAGING_DIR 
echo "Written to: $RPM_SOURCES_DIR/ffmpeg-$FFMPEG_AUX_VERSION.tar.bz2."

rpmbuild -ba $RPM_SPECS_DIR/$FFMPEG_AUX_RPM_PACKAGE_NAME.spec

