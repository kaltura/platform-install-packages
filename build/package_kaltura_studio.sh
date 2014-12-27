#!/bin/bash -e 
#===============================================================================
#          FILE: package_kaltura_web.sh
#         USAGE: ./package_kaltura_web.sh 
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
# clean the source dir.
rm -rf $SOURCE_PACKAGING_DIR/$KDP3_RPM_NAME/*

kaltura_svn export --force --quiet $KDP3PLUGINS_URI $SOURCE_PACKAGING_DIR/$KDP3PLUGINS_RPM_NAME
mkdir -p $SOURCE_PACKAGING_DIR/uiconf/kaltura/kmc/appstudio/kdp3 
kaltura_svn export --force --quiet $KDP3_UICONF_URI $SOURCE_PACKAGING_DIR/$KDP3_RPM_NAME/uiconf/kaltura/kmc/appstudio/kdp3
for KDP3_VERSION in $KDP3_VERSIONS;do
	kaltura_svn export --force --quiet $KDP3_URI/$KDP3_VERSION $SOURCE_PACKAGING_DIR/$KDP3_RPM_NAME/$KDP3_VERSION 
	cp -r $SOURCE_PACKAGING_DIR/$KDP3PLUGINS_RPM_NAME $SOURCE_PACKAGING_DIR/$KDP3_RPM_NAME/$KDP3_VERSION/plugins 
done
cd $SOURCE_PACKAGING_DIR
# flash things DO NOT need exec perms.
find $KDP3_RPM_NAME -type f -exec chmod -x {} \;
tar jcf $RPM_SOURCES_DIR/$KDP3_RPM_NAME.tar.bz2 $KDP3_RPM_NAME
echo "Packaged into $RPM_SOURCES_DIR/$KDP3_RPM_NAME.tar.bz2"
rpmbuild -ba $RPM_SPECS_DIR/$KDP3_RPM_NAME.spec
