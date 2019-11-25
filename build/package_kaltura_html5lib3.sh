#!/bin/bash -e 
#===============================================================================
#          FILE: package_kaltura_html5lib3.sh
#         USAGE: ./package_kaltura_html5lib3.sh 
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
if [ ! -x "`which curl 2>/dev/null`" ];then
	echo "Need to install curl."
	exit 2
fi
mkdir -p $SOURCE_PACKAGING_DIR/html5lib3_tmp/$HTML5LIB3_VERSION
cd $SOURCE_PACKAGING_DIR/html5lib3_tmp/
GITHUB_BASE_URI="https://github.com/kaltura"
for SOURCE in HTML5LIB3 PLAYKIT_IMA PLAYKIT_YOUBORA PLAYKIT_GOOGLE_ANALYTICS PLAYKIT_OFFLINE_MANAGER PLAYKIT_CAST_SENDER PLAYKIT_CAST_RECEIVER PLAYKIT_VR PLAYKIT_FLASH PLAYKIT_YOUTUBE PLAYKIT_BUMPER;do
	URI=${SOURCE}_URI
	REPO_NAME=${SOURCE}_REPO_NAME
	VERSION=${SOURCE}_VERSION
	echo ${!URI} ${!REPO_NAME}
	SHORT_NAME=`echo ${!REPO_NAME}|sed 's@-js@@'`
	set +e
	curl -f -L "$GITHUB_BASE_URI/${!REPO_NAME}/releases/download/v${!VERSION}/$SHORT_NAME.js" > $SOURCE_PACKAGING_DIR/html5lib3_tmp/$HTML5LIB3_VERSION/$SHORT_NAME.js
	if [ $? -eq 0 ];then
		set -e
		curl -L "$GITHUB_BASE_URI/kaltura/${!REPO_NAME}/releases/download/v${!VERSION}/$SHORT_NAME.js.map" > $SOURCE_PACKAGING_DIR/html5lib3_tmp/$HTML5LIB3_VERSION/$SHORT_NAME.js.map
	else
		curl -L ${!URI} > ${!VERSION}.tar.gz
		tar xf ${!VERSION}.tar.gz
		cp ${!REPO_NAME}-${!VERSION}/dist/*js* $SOURCE_PACKAGING_DIR/html5lib3_tmp/$HTML5LIB3_VERSION
	fi
	# that's OTT and we don't want it
done 
$BASE_CHECKOUT_DIR/build/gh_download_asset.sh $GITHUB_TOKEN kaltura/kaltura-interactive-player path-kaltura-player.js v$PLAYKIT_INTERACTIVE_VERSION $SOURCE_PACKAGING_DIR/html5lib3_tmp/$HTML5LIB3_VERSION
$BASE_CHECKOUT_DIR/build/gh_download_asset.sh $GITHUB_TOKEN kaltura/kaltura-interactive-player path-kaltura-player.js.map v$PLAYKIT_INTERACTIVE_VERSION $SOURCE_PACKAGING_DIR/html5lib3_tmp/$HTML5LIB3_VERSION

rm $SOURCE_PACKAGING_DIR/html5lib3_tmp/$HTML5LIB3_VERSION/kaltura-tv-player.js*
cd $SOURCE_PACKAGING_DIR/html5lib3_tmp/
tar zcf $RPM_SOURCES_DIR/$HTML5LIB3_RPM_NAME-$HTML5LIB3_VERSION.tar.gz $HTML5LIB3_VERSION
cd $SOURCE_PACKAGING_DIR
rm -rf $SOURCE_PACKAGING_DIR/html5lib3_tmp
echo "Packaged into $RPM_SOURCES_DIR/$HTML5LIB3_RPM_NAME-$HTML5LIB3_VERSION.tar.gz"
if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -bb $RPM_SPECS_DIR/$HTML5LIB3_RPM_NAME.spec
fi
