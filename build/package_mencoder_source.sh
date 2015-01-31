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

wget $MENCODER_URI -O $RPM_SOURCES_DIR/mencoder-$MENCODER_VERSION.tar.bz2
if [ $? -eq 0 ];then
	echo "Packaged to mencoder-$MENCODER_VERSION.tar.bz2"
else
	echo "Unable to download $MENCODER_URI" >&2
	exit 1
fi

if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -ba $RPM_SPECS_DIR/kaltura-mencoder.spec
fi
