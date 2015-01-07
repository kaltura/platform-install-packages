#!/bin/bash -e 
#===============================================================================
#          FILE: package_kaltura_postinst.sh
#         USAGE: ./package_kaltura_postinst.sh 
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
cd $BASE_CHECKOUT_DIR/RPM/scripts 
tar zcf $RPM_SOURCES_DIR/kaltura-postinst-$KALTURA_POSTINST_VERSION.tar.gz postinst/
echo "Packaged into $RPM_SOURCES_DIR/kaltura-postinst-$KALTURA_POSTINST_VERSION.tar.gz"
if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -ba $RPM_SPECS_DIR/kaltura-postinst.spec
fi
