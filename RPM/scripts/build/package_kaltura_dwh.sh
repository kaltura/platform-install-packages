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

for i in wget ;do
	EX_PATH=`which $i 2>/dev/null`
	if [ -z "$EX_PATH" -o ! -x "$EX_PATH" ];then
		echo "Need to install $i."
		exit 2
	fi
done

SOURCES_RC=`dirname $0`/sources.rc
if [ ! -r $SOURCES_RC ];then
	echo "Could not find $SOURCES_RC"
	exit 1
fi
. $SOURCES_RC 

wget $DWH_URI -O$RPM_SOURCES_DIR/$DWH_RPM_NAME-$DWH_VERSION.zip 
echo "Packaged into $RPM_SOURCES_DIR/$DWH_RPM_NAME-$DWH_VERSION.zip"
#rpmbuild -ba $RPM_SPECS_DIR/$DWH_RPM_NAME.spec
