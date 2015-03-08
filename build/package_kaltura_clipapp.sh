#!/bin/bash -e 
#===============================================================================
#          FILE: package_kaltura_clipapp.sh
#         USAGE: ./package_kaltura_clipapp.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy <jess.portnoy@kaltura.com>
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
if [ ! -x "`which unzip 2>/dev/null`" ];then
	echo "Need to install unzip."
	exit 2
fi

wget $CLIPAPP_URI -O $RPM_SOURCES_DIR/$CLIPAPP_RPM_NAME-$CLIPAPP_VERSION.zip 
echo "Packaged into $RPM_SOURCES_DIR/$CLIPAPP_RPM_NAME-$CLIPAPP_VERSION.zip "

if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -ba $RPM_SPECS_DIR/$CLIPAPP_RPM_NAME.spec
fi
