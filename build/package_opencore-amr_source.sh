#!/bin/bash -e 
#===============================================================================
#          FILE: package_opencore-amr_source.sh
#         USAGE: ./package_opencore-amr_source.sh 
#   DESCRIPTION: Retrieve opencore-amr source
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Tan-Tan, <jonathan.kanarek@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 12/25/14
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error
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
 
wget $OPENCORE_AMR_URI -O $RPM_SOURCES_DIR/opencore-amr-$OPENCORE_AMR_VERSION.tar.gz
if [ $? -eq 0 ];then
	echo "Packaged to opencore-amr-$OPENCORE_AMR_VERSION.tar.gz"
else
	echo "Unable to download $OPENCORE_AMR_URI" >&2
	exit 1
fi

rpmbuild -ba $RPM_SPECS_DIR/kaltura-opencore-amr.spec

