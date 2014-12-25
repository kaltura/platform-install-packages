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
if [ ! -x "`which svn 2>/dev/null`" ];then
	echo "Need to install svn."
	exit 2
fi

# remove left overs:
rm -rf $SOURCE_PACKAGING_DIR/$KSE_RPM_NAME/*

for KSE_VERSION in $KSE_VERSIONS;do
	svn export --force --quiet $KSE_URI/$KSE_VERSION $SOURCE_PACKAGING_DIR/$KSE_RPM_NAME/$KSE_VERSION 
done

for KSE_UICONF_VERSION in $KSE_UICONF_VERSIONS;do
	svn export --force --quiet $KSE_UICONF_URI/$KSE_UICONF_VERSION $SOURCE_PACKAGING_DIR/$KSE_RPM_NAME/uiconf/kaltura/kmc/kcw
done
svn export --force --quiet $KSE_UICONF_GENERIC_URI $SOURCE_PACKAGING_DIR/$KSE_RPM_NAME/uiconf/kaltura/kmc/generic
svn export --force --quiet $KSE_UICONF_EDITOR_URI $SOURCE_PACKAGING_DIR/$KSE_RPM_NAME/uiconf/kcweditor/locales/en_US
cd $SOURCE_PACKAGING_DIR

# flash things DO NOT need exec perms.
find $KSE_RPM_NAME -type f -exec chmod -x {} \;

tar jcf $RPM_SOURCES_DIR/$KSE_RPM_NAME.tar.bz2 $KSE_RPM_NAME
echo "Packaged into $RPM_SOURCES_DIR/$KSE_RPM_NAME.tar.bz2"
rpmbuild -ba $RPM_SPECS_DIR/$KSE_RPM_NAME.spec
