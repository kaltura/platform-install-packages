#!/bin/bash -e 
#===============================================================================
#          FILE: package_kaltura_wrapper.sh
#         USAGE: ./package_kaltura_wrapper.sh 
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
if [ ! -x "`which svn 2>/dev/null`" ];then
	echo "Need to install svn."
	exit 2
fi

kaltura_svn export --force --quiet $KDPWRAPPER_URI/$KDPWRAPPER_VERSION $SOURCE_PACKAGING_DIR/$KDPWRAPPER_RPM_NAME/$KDPWRAPPER_VERSION 
cd $SOURCE_PACKAGING_DIR
# flash things DO NOT need exec perms.
find $KDPWRAPPER_RPM_NAME -type f -exec chmod -x {} \;
tar jcf $RPM_SOURCES_DIR/$KDPWRAPPER_RPM_NAME.tar.bz2 $KDPWRAPPER_RPM_NAME
echo "Packaged into $RPM_SOURCES_DIR/$KDPWRAPPER_RPM_NAME.tar.bz2"
rpmbuild -ba $RPM_SPECS_DIR/$KDPWRAPPER_RPM_NAME.spec
