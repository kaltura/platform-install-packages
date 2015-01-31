#!/bin/bash -e 
#===============================================================================
#          FILE: package_kaltura_kcw.sh
#         USAGE: ./package_kaltura_kcw.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy (), <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 01/10/14 08:46:43 EST
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
	echo "Need to install svn."
	exit 2
fi
if [ ! -x "`which unzip 2>/dev/null`" ];then
	echo "Need to install svn."
	exit 2
fi

# remove left overs:
rm -rf $SOURCE_PACKAGING_DIR/$KUPLOAD_RPM_NAME/*
mkdir -p $SOURCE_PACKAGING_DIR/$KUPLOAD_RPM_NAME/
wget $KUPLOAD_URI -O $RPM_SOURCES_DIR/$KUPLOAD_RPM_NAME-$KUPLOAD_VERSION.zip
echo "Packaged into $RPM_SOURCES_DIR/$KUPLOAD_RPM_NAME-$KUPLOAD_VERSION.zip"
if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -ba $RPM_SPECS_DIR/$KUPLOAD_RPM_NAME.spec
fi
