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

if [ -x "`which yum 2>/dev/null`" ];then
	sudo yum localinstall -y $SOURCE_PACKAGING_DIR/RPMS/x86_64/kaltura-lame-*.x86_64.rpm
	sudo yum localinstall -y $SOURCE_PACKAGING_DIR/RPMS/x86_64/kaltura-a52dec-*.x86_64.rpm
	sudo yum localinstall -y $SOURCE_PACKAGING_DIR/RPMS/x86_64/kaltura-libfaac-*.x86_64.rpm
	sudo yum localinstall -y $SOURCE_PACKAGING_DIR/RPMS/x86_64/kaltura-x264-*.x86_64.rpm
	sudo yum localinstall -y $SOURCE_PACKAGING_DIR/RPMS/x86_64/kaltura-libopencore-amr-*.x86_64.rpm
	sudo yum localinstall -y $SOURCE_PACKAGING_DIR/RPMS/x86_64/kaltura-fdk-aac-*.x86_64.rpm
fi


cd $RPM_SOURCES_DIR
curl $FFMPEG_URI > ffmpeg-$FFMPEG_VERSION.tar.bz2
cd $SOURCE_PACKAGING_DIR 
echo "Written to: $RPM_SOURCES_DIR/ffmpeg-$FFMPEG_VERSION.tar.bz2."


if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -ba $RPM_SPECS_DIR/$FFMPEG_RPM_PACKAGE_NAME.spec
fi
