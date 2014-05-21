#!/bin/bash -e 
#===============================================================================
#          FILE: package_red5_source.sh
#         USAGE: ./package_red5_source.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 12/29/13 05:24:47 EST
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error

if [ ! -x `which svn 2>/dev/null` ];then
	echo "Need to install subversion."
	exit 2
fi

SOURCES_RC=`dirname $0`/sources.rc
if [ ! -r $SOURCES_RC ];then
	echo "Could not find $SOURCES_RC"
	exit 1
fi
. $SOURCES_RC 
cd $SOURCE_PACKAGING_DIR 
rm -rf $RED5_RPM_PACKAGE_NAME-flash-$RED5_VERSION $RED5_RPM_PACKAGE_NAME-$RED5_VERSION
svn export $RED5_JAVA_URI $RED5_RPM_PACKAGE_NAME-$RED5_VERSION --force
svn export $RED5_FLASH_URI $RED5_RPM_PACKAGE_NAME-flash-$RED5_VERSION --force
tar jcf $RPM_SOURCES_DIR/$RED5_RPM_PACKAGE_NAME-$RED5_VERSION.tar.bz2 $RED5_RPM_PACKAGE_NAME-$RED5_VERSION
cd $RED5_RPM_PACKAGE_NAME-flash-$RED5_VERSION
mv deploy demos
cd ..
tar jcf $RPM_SOURCES_DIR/$RED5_RPM_PACKAGE_NAME-flash-$RED5_VERSION.tar.bz2 $RED5_RPM_PACKAGE_NAME-flash-$RED5_VERSION

echo "written to: $RPM_SOURCES_DIR/$RED5_RPM_PACKAGE_NAME-$RED5_VERSION.tar.bz2"
echo "written to: $RPM_SOURCES_DIR/$RED5_RPM_PACKAGE_NAME-flash-$RED5_VERSION.tar.bz2"
rpmbuild -ba $RPM_SPECS_DIR/$RED5_RPM_PACKAGE_NAME.spec

