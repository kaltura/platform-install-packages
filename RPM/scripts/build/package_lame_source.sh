#!/bin/bash -e 
#===============================================================================
#          FILE: package_lame_source.sh
#         USAGE: ./package_lame_source.sh 
#   DESCRIPTION: Retrieve lame source
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Tan-Tan, <jonathan.kanarek@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 12/21/14
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error
if [ ! -x `which wget 2>/dev/null` ];then
	echo "Need to install subversion."
	exit 2
fi

SOURCES_RC=`dirname $0`/sources.rc
if [ ! -r $SOURCES_RC ];then
	echo "Could not find $SOURCES_RC"
	exit 1
fi
. $SOURCES_RC
 
wget $LAME_URI -O $RPM_SOURCES_DIR/lame-$LAME_VERSION.tar.gz
if [ $? -eq 0 ];then
	echo "Packaged to lame-$LAME_VERSION.tar.gz"
else
	echo "Unable to download $LAME_URI" >&2
	exit 1
fi

rpmbuild -ba $RPM_SPECS_DIR/kaltura-lame.spec

