#!/bin/bash -e 
#===============================================================================
#          FILE: package_fdk_source.sh
#         USAGE: ./package_fdk_source.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy (), <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 12/29/13 05:24:47 EST
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error

if [ ! -x `which git 2>/dev/null` ];then
	echo "Need to install git."
	exit 2
fi

SOURCES_RC=`dirname $0`/sources.rc
if [ ! -r $SOURCES_RC ];then
	echo "Could not find $SOURCES_RC"
	exit 1
fi
. $SOURCES_RC 
cd $SOURCE_PACKAGING_DIR 

git clone $FDK_URI 
tar jcvf  $RPM_SOURCES_DIR/kaltura-fdk-aac-$FDK_VERSION.tar.bz2 fdk-aac 
echo "Written to: $RPM_SOURCES_DIR/kaltura-fdk-aac-$FDK_VERSION.tar.bz2"

rpmbuild -ba $RPM_SPECS_DIR/kaltura-fdk-aac.spec

