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
rm -rf $SOURCE_PACKAGING_DIR/$KCW_RPM_NAME/*

#kaltura_svn export --force --quiet $KCW_URI/$KCW_VERSION $SOURCE_PACKAGING_DIR/$KCW_RPM_NAME/$KCW_VERSION 
wget $KCW_URI -O $SOURCE_PACKAGING_DIR/kcw-$KCW_VERSION 
mkdir $SOURCE_PACKAGING_DIR/$KCW_RPM_NAME/
cd $SOURCE_PACKAGING_DIR/$KCW_RPM_NAME
unzip $SOURCE_PACKAGING_DIR/kcw-$KCW_VERSION


for KCW_UICONF_VERSION in $KCW_UICONF_VERSIONS;do
	kaltura_svn export --force --quiet $KCW_UICONF_URI/$KCW_UICONF_VERSION $SOURCE_PACKAGING_DIR/$KCW_RPM_NAME/uiconf/kaltura/kmc/kcw
done
kaltura_svn export --force --quiet $KCW_UICONF_GENERIC_URI $SOURCE_PACKAGING_DIR/$KCW_RPM_NAME/uiconf/kaltura/generic/kcw_2.1.5
kaltura_svn export --force --quiet $KCW_UICONF_EDITOR_URI $SOURCE_PACKAGING_DIR/$KCW_RPM_NAME/uiconf/kcweditor/locales/en_US
cd $SOURCE_PACKAGING_DIR

# flash things DO NOT need exec perms.
find $KCW_RPM_NAME -type f -exec chmod -x {} \;

tar jcf $RPM_SOURCES_DIR/$KCW_RPM_NAME-$KCW_VERSION.tar.bz2 $KCW_RPM_NAME
echo "Packaged into $RPM_SOURCES_DIR/$KCW_RPM_NAME-$KCW_VERSION.tar.bz2"
if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -ba $RPM_SPECS_DIR/$KCW_RPM_NAME.spec
fi
