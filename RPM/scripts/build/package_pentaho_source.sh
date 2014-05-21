#!/bin/bash -e 
#===============================================================================
#          FILE: package_pentaho_source.sh
#         USAGE: ./package_pentaho_source.sh 
#   DESCRIPTION: Retrieve Pentaho source
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy, <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 12/29/13 03:15:11 EST
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error
if [ ! -x `which wget 2>/dev/null` ];then
	echo "Need to install subversion."
	exit 2
fi

SOURCES_RC=`dirname $0`/sources.rc
if [ ! -r $SOURCES_RC ];then
	echo "Could not find $SOURCES_RC"
	exit 1
fi
. $SOURCES_RC 
wget $PENTAHO_URI -O $RPM_SOURCES_DIR/pdi-ce-$PENTAHO_VERSION-stable.tar.gz
echo "Packaged to pdi-ce-$PENTAHO_VERSION-stable.tar.gz"
rpmbuild -ba $RPM_SPECS_DIR/$PENTAHO_RPM_PACKAGE_NAME.spec

