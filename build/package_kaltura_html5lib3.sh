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
for SOURCE in HTML5LIB3 PLAYKIT_IMA PLAYKIT_YOUBORA PLAYKIT_GOOGLE_ANALYTICS PLAYKIT_GOOGLE_TAG_MANAGER PLAYKIT_OFFLINE_MANAGER PLAYKIT_CAST_SENDER PLAYKIT_CAST_RECEIVER PLAYKIT_VR PLAYKIT_FLASH PLAYKIT_YOUTUBE PLAYKIT_BUMPER PLAYKIT_KAVA PLAYKIT_KALTURA_LIVE PLAYKIT_QNA PLAYKIT_NAVIGATION PLAYKIT_HOTSPOTS PLAYKIT_TRANSCRIPT PLAYKIT_DUAL_SCREEN PLAYKIT_TIMELINE PLAYKIT_CUEPOINTS PLAYKIT_INFO PLAYKIT_PLAYLIST PLAYKIT_AIRPLAY PLAYKIT_MODERATION PLAYKIT_RELATED;do
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
for i in path-kaltura-player.js path-kaltura-player.js.map;do
	$BASE_CHECKOUT_DIR/build/gh_download_asset.sh $GITHUB_TOKEN kaltura/kaltura-interactive-player $i v$PLAYKIT_INTERACTIVE_VERSION $SOURCE_PACKAGING_DIR/html5lib3_tmp/$HTML5LIB3_VERSION
done

curl -L $PLAYKIT_UI_URI > playkit-ui_$PLAYKIT_UI_VERSION.tar.gz
tar zxf playkit-ui_$PLAYKIT_UI_VERSION.tar.gz
cp -r playkit-js-ui-$PLAYKIT_UI_VERSION/translations $SOURCE_PACKAGING_DIR/html5lib3_tmp/$HTML5LIB3_VERSION

# Fetch Brand3d from Bitbucket:
BRAND3D_ARCHIVE=$SOURCE_PACKAGING_DIR/playkit_brand3d_${PLAYKIT_BRAND3D_VERSION}.tar.bz2
curl -L $PLAYKIT_BRAND3D_URI --output $BRAND3D_ARCHIVE
tar jxf $BRAND3D_ARCHIVE -C $SOURCE_PACKAGING_DIR/ 
cp $SOURCE_PACKAGING_DIR/brand3d-brand3d-overlay-c3a7824dcfdf/dist/brand3d-overlay.js $SOURCE_PACKAGING_DIR/html5lib3_tmp/$HTML5LIB3_VERSION/plugin-marketplace-brand3d-overlay.js
cp $SOURCE_PACKAGING_DIR/brand3d-brand3d-overlay-c3a7824dcfdf/dist/brand3d-overlay.js.map $SOURCE_PACKAGING_DIR/html5lib3_tmp/$HTML5LIB3_VERSION/plugin-marketplace-brand3d-overlay.js.map

# remove OTT player
rm $SOURCE_PACKAGING_DIR/html5lib3_tmp/$HTML5LIB3_VERSION/kaltura-tv-player*
rm $SOURCE_PACKAGING_DIR/html5lib3_tmp/$HTML5LIB3_VERSION/*.cjs.js*
# sometimes the plugin archives include empty files or do not have the files we expect so, let's remove zero sized files
find $SOURCE_PACKAGING_DIR/html5lib3_tmp/$HTML5LIB3_VERSION -size 0 -exec rm {} \;

cd $SOURCE_PACKAGING_DIR/html5lib3_tmp/$HTML5LIB3_VERSION
cd ..
tar zcf $RPM_SOURCES_DIR/$HTML5LIB3_RPM_NAME-$HTML5LIB3_VERSION.tar.gz $HTML5LIB3_VERSION
cd $SOURCE_PACKAGING_DIR
rm -rf $SOURCE_PACKAGING_DIR/html5lib3_tmp
echo "Packaged into $RPM_SOURCES_DIR/$HTML5LIB3_RPM_NAME-$HTML5LIB3_VERSION.tar.gz"
if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -bb $RPM_SPECS_DIR/$HTML5LIB3_RPM_NAME.spec
fi
