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
if [ ! -x `which wget 2>/dev/null` ];then
	echo "Need to install wget."
	exit 2
fi
mkdir -p $SOURCE_PACKAGING_DIR/$KDP3_RPM_NAME
set -x
for KDP3_VERSION in $KDP3_VERSIONS;do
	wget $KDP3_BASE_URI/$KDP3_VERSION/$KDP3_VERSION.zip -O$SOURCE_PACKAGING_DIR/$KDP3_RPM_NAME/$KDP3_RPM_NAME-$KDP3_VERSION.zip
	cd $SOURCE_PACKAGING_DIR/$KDP3_RPM_NAME
	unzip -o $SOURCE_PACKAGING_DIR/$KDP3_RPM_NAME/$KDP3_RPM_NAME-$KDP3_VERSION.zip
	rm -rf $KDP3_VERSION/__MACOSX $KDP3_VERSION/.DS_Store
	cd $SOURCE_PACKAGING_DIR/$KDP3_RPM_NAME/
	tar zcf  $RPM_SOURCES_DIR/$KDP3_RPM_NAME-$KDP3_VERSION.tar.gz $KDP3_VERSION
set +x
	echo "Packaged into $RPM_SOURCES_DIR/$KDP3_RPM_NAME-$KDP3_VERSION.tar.gz"
done
rpmbuild -ba $RPM_SPECS_DIR/$KDP3_RPM_NAME.spec
