#!/bin/bash -e 
#===============================================================================
#          FILE: package.sh
#         USAGE: ./package.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Tan-Tan, <jonathan.kanarek@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 12/17/14
#      REVISION:  ---
#===============================================================================

#set -o nounset                              # Treat unset variables as an error

SOURCES_RC=`dirname $0`/sources.rc
if [ ! -r $SOURCES_RC ];then
	echo "Could not find $SOURCES_RC"
	exit 1
fi
. $SOURCES_RC

rm -rf $SOURCE_PACKAGING_DIR
mkdir $SOURCE_PACKAGING_DIR
cp -r $RPM_BASE_DIR/SOURCES $SOURCE_PACKAGING_DIR
ln -s $RPM_BASE_DIR/SPECS $SOURCE_PACKAGING_DIR/SPECS

cd $BUILD_DIR

./package_php_source.sh
./package_a52dec_source.sh
./package_fdk_source.sh
./package_x264_source.sh
./package_lame_source.sh
./package_libass_source.sh
./package_faac_source.sh
./package_ffmpeg_source.sh
./package_pentaho_source.sh
./package_red5_source.sh
./package_sphinx_source.sh

./package_kaltura.sh


