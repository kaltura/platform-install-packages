#!/bin/bash -e 
#===============================================================================
#          FILE: package_kaltura_monit.sh
#         USAGE: ./package_kaltura_monit.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Tan-Tan, <jonathan.kanarek@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 29/12/14
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

wget $MONIT_URI -O$RPM_SOURCES_DIR/monit-$MONIT_VERSION.tar.gz
if [ $? -eq 0 ];then
	echo "Packaged to monit-$MONIT_VERSION.tar.gz"
else
	echo "Unable to download $MONIT_URI" >&2
	exit 1
fi

echo "Packaged into $RPM_SOURCES_DIR/monit-$MONIT_VERSION.tar.gz"
if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -ba $RPM_SPECS_DIR/kaltura-monit.spec
fi
