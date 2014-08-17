#!/bin/bash -e 
#===============================================================================
#          FILE: package_kaltura_kvpm.sh
#         USAGE: ./package_kaltura_kvpm.sh 
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
svn export --force --quiet $KCLIP_URI $SOURCE_PACKAGING_DIR/$KCLIP_RPM_NAME

cd $SOURCE_PACKAGING_DIR
# flash things DO NOT need exec perms.
find $KCLIP_RPM_NAME -type f -exec chmod -x {} \;
tar jcf $RPM_SOURCES_DIR/$KCLIP_RPM_NAME.tar.bz2 $KCLIP_RPM_NAME
echo "Packaged into $RPM_SOURCES_DIR/$KCLIP_RPM_NAME.tar.bz2"
rpmbuild -ba $RPM_SPECS_DIR/$KCLIP_RPM_NAME.spec
