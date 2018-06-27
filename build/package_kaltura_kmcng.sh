#!/bin/bash -e 
#===============================================================================
#          FILE: package_kaltura_kmcng.sh
#         USAGE: ./package_kaltura_kmcng.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy (), <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 06/27/18 08:46:43 EST
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error
SOURCES_RC=`dirname $0`/sources.rc
if [ ! -r $SOURCES_RC ];then
	echo "Could not find $SOURCES_RC"
	exit 1
fi
. $SOURCES_RC 
for UTIL in wget unzip ;do
	if [ ! -x "`which $UTIL 2>/dev/null`" ];then
		echo "Need to install $UTIL."
		exit 2
	fi
done

set -x
cd $SOURCE_PACKAGING_DIR
wget $KMCNG_URI -O $KMCNG_RPM_NAME-$KMCNG_VERSION.zip
unzip -qo $KMCNG_RPM_NAME-$KMCNG_VERSION.zip
rm -rf $KMCNG_RPM_NAME-$KMCNG_VERSION
mv $KMCNG_VERSION $KMCNG_RPM_NAME-$KMCNG_VERSION
set +x
mv deploy server-config-example.json $KMCNG_RPM_NAME-$KMCNG_VERSION
rm -rf __MACOSX
find $KMCNG_RPM_NAME-$KMCNG_VERSION -type f -exec chmod -x {} \;
tar jcf $RPM_SOURCES_DIR/$KMCNG_RPM_NAME-$KMCNG_VERSION.tar.bz2 $KMCNG_RPM_NAME-$KMCNG_VERSION
echo "Packaged into $RPM_SOURCES_DIR/$KMCNG_RPM_NAME-$KMCNG_VERSION.tar.bz2"

if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -bb $RPM_SPECS_DIR/$KMCNG_RPM_NAME.spec
fi
