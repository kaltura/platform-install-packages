#!/bin/bash -e 
#===============================================================================
#          FILE: package_kaltura_html5lib.sh
#         USAGE: ./package_kaltura_html5lib.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 01/14/14 11:46:43 EST
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
	echo "Need to install wget."
	exit 2
fi
#HTML5LIB_VERSION=$1

cd $SOURCE_PACKAGING_DIR
for HTML5LIB_VERSION in $HTML5LIB_VERSIONS;do
	set +e
	if ! tar ztf  $RPM_SOURCES_DIR/$HTML5LIB_RPM_NAME-$HTML5LIB_VERSION.tar.gz >/dev/null ;then
		wget $HTML5LIB_BASE_URI/$HTML5LIB_VERSION -O $HTML5LIB_RPM_NAME-$HTML5LIB_VERSION.tar.gz
		tar zxf $HTML5LIB_RPM_NAME-$HTML5LIB_VERSION.tar.gz 
		rm -rf $HTML5LIB_RPM_NAME-$HTML5LIB_VERSION
		mv `ls -rtd kaltura-mwEmbed-* | tail -1` $HTML5LIB_RPM_NAME-$HTML5LIB_VERSION
		tar zcf $RPM_SOURCES_DIR/$HTML5LIB_RPM_NAME-$HTML5LIB_VERSION.tar.gz $HTML5LIB_RPM_NAME-$HTML5LIB_VERSION
		#rm $HTML5LIB_RPM_NAME-$HTML5LIB_VERSION.tar.gz
		echo "Packaged into $RPM_SOURCES_DIR/$HTML5LIB_RPM_NAME-$HTML5LIB_VERSION.tar.gz"
	fi
	set -e
done
if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -bb $RPM_SPECS_DIR/$HTML5LIB_RPM_NAME.spec
fi
