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

rm -rf $SOURCE_PACKAGING_DIR/$KMC_RPM_NAME-$KMC_VERSION
kaltura_svn export --force --quiet $KMC_UICONF_URI $SOURCE_PACKAGING_DIR/$KMC_RPM_NAME-$KMC_VERSION/uiconf/kaltura/kmc
cd $SOURCE_PACKAGING_DIR
wget $KMC_URI -O $KMC_RPM_NAME-$KMC_VERSION.zip
unzip -qo $KMC_RPM_NAME-$KMC_VERSION.zip
wget $KMC_LOGIN_URI -O $KMC_RPM_NAME-$KMC_LOGIN_VERSION.zip
unzip -oq $KMC_RPM_NAME-$KMC_LOGIN_VERSION.zip
wget $KMC_DOC_URI -O $KMC_RPM_NAME-$KMC_DOC_VERSION.zip
unzip -oq $KMC_RPM_NAME-$KMC_DOC_VERSION.zip

rm -rf $SOURCE_PACKAGING_DIR/$KMC_RPM_NAME-$KMC_VERSION/login
mkdir -p $SOURCE_PACKAGING_DIR/$KMC_RPM_NAME-$KMC_VERSION/login
mv $KMC_LOGIN_VERSION $SOURCE_PACKAGING_DIR/$KMC_RPM_NAME-$KMC_VERSION/login
mv $KMC_VERSION $KMC_RPM_NAME-$KMC_VERSION
mv kmc-docs-$KMC_DOC_VERSION $SOURCE_PACKAGING_DIR/$KMC_RPM_NAME-$KMC_VERSION/doc

find $KMC_RPM_NAME-$KMC_VERSION -type f -exec chmod -x {} \;
tar jcf $RPM_SOURCES_DIR/$KMC_RPM_NAME-$KMC_VERSION.tar.bz2 $KMC_RPM_NAME-$KMC_VERSION
# flash things DO NOT need exec perms.
echo "Packaged into $RPM_SOURCES_DIR/$KMC_RPM_NAME-$KMC_VERSION.tar.bz2"

if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -ba $RPM_SPECS_DIR/$KMC_RPM_NAME.spec
fi
