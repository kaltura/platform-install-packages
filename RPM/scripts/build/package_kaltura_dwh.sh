#!/bin/bash -e 
#===============================================================================
#          FILE: package_kaltura_web.sh
#         USAGE: ./package_kaltura_web.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
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
if [ ! -x `which svn 2>/dev/null` ];then
	echo "Need to install svn."
	exit 2
fi

svn export --force --quiet $DWH_URI $SOURCE_PACKAGING_DIR/$DWH_RPM_NAME-$KALTURA_SERVER_VERSION 
cd $SOURCE_PACKAGING_DIR
tar jcf $RPM_SOURCES_DIR/$DWH_RPM_NAME-$KALTURA_SERVER_VERSION.tar.bz2 $DWH_RPM_NAME-$KALTURA_SERVER_VERSION
echo "Packaged into $RPM_SOURCES_DIR/$DWH_RPM_NAME-$KALTURA_SERVER_VERSION.tar.bz2"
rpmbuild -ba $RPM_SPECS_DIR/$DWH_RPM_NAME.spec
