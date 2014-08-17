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
for i in svn ;do
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

for CLIPAPP_VERSION in $CLIPAPP_VERSIONS;do
	svn export --force --quiet $CLIPAPP_URI/$CLIPAPP_VERSION $SOURCE_PACKAGING_DIR/$CLIPAPP_RPM_NAME/$CLIPAPP_VERSION 
done
cd $SOURCE_PACKAGING_DIR
tar jcf $RPM_SOURCES_DIR/$CLIPAPP_RPM_NAME.tar.bz2 $CLIPAPP_RPM_NAME
echo "Packaged into $RPM_SOURCES_DIR/$CLIPAPP_RPM_NAME.tar.bz2"
rpmbuild -ba $RPM_SPECS_DIR/$CLIPAPP_RPM_NAME.spec
