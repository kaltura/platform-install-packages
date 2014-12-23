#!/bin/bash -e 
#===============================================================================
#          FILE: package_libass_source.sh
#         USAGE: ./package_libass_source.sh 
#   DESCRIPTION: Retrieve libass source
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
 
wget $LIBASS_URI -O $RPM_SOURCES_DIR/libass-$LIBASS_VERSION.tar.bz2
if [ $? -eq 0 ];then
	echo "Packaged to libass-$LIBASS_VERSION.tar.bz2"
else
	echo "Unable to download $LIBASS_URI" >&2
	exit -1
fi

rpmbuild -ba $RPM_SPECS_DIR/kaltura-libass.spec

